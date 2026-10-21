"""Worker interruption and retry contracts; storage and model calls stay offline."""
from __future__ import annotations

import asyncio
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Lock
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from azure.core import MatchConditions
from azure.core.exceptions import ResourceModifiedError
from fastapi import BackgroundTasks
from models.request_models import ProcessAnalyzeRequest
from routers import ai_router, storage_router
from services.processing_state import (
    INTERRUPTED_MESSAGE, STALE_AFTER_SECONDS, ProcessingStateStore,
)
from workflow_orchestrator import EWAWorkflowOrchestrator


class FakeBlob:
    def __init__(self, clock, metadata=None):
        self.clock = clock
        self.metadata = dict(metadata or {})
        self.modified = clock() - timedelta(hours=12)
        self.version = 0
        self.lock = Lock()
        self.before_write = None

    def get_blob_properties(self):
        with self.lock:
            return SimpleNamespace(metadata=dict(self.metadata), etag=str(self.version),
                                   last_modified=self.modified)

    def set_blob_metadata(self, metadata, *, etag, match_condition):
        assert match_condition == MatchConditions.IfNotModified
        if self.before_write:
            hook, self.before_write = self.before_write, None
            hook()
        with self.lock:
            if etag != str(self.version):
                raise ResourceModifiedError("Synthetic competing write")
            self.metadata = dict(metadata)
            self.version += 1
            self.modified = self.clock()

    def exists(self):
        return True


class ProcessingRecoveryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 21, tzinfo=timezone.utc)
        self.blob = FakeBlob(lambda: self.now, {"customer_name": "Synthetic", "system_id": "TST"})
        self.client = Mock()
        self.client.get_blob_client.return_value = self.blob
        self.container = self.client.get_container_client.return_value
        self.container.get_blob_client.return_value = self.blob
        self.container.list_blobs.return_value = []
        self.store = ProcessingStateStore(self.client, "synthetic")
        self.clock_patch = patch("services.processing_state._now", lambda: self.now)
        self.clock_patch.start()
        self.addCleanup(self.clock_patch.stop)

    def legacy_run(self):
        self.blob.metadata.update(processing="true", last_status="processing")

    async def test_legacy_interruption_becomes_failed_and_preserves_source_metadata(self):
        self.legacy_run()
        props = self.store.read("report.html")
        self.assertEqual(props.metadata["last_status"], "failed")
        self.assertNotIn("processing", props.metadata)
        self.assertEqual(props.metadata["last_error_hint"], INTERRUPTED_MESSAGE)
        self.assertEqual(props.metadata["system_id"], "TST")

    async def test_recent_legacy_run_is_not_reaped(self):
        self.legacy_run()
        self.blob.modified = self.now - timedelta(seconds=30)
        self.assertIsNone(self.store.claim("report.html"))
        self.assertEqual(self.store.read("report.html").metadata["processing"], "true")

    async def test_active_long_running_job_uses_heartbeat_not_total_age(self):
        run_id = self.store.claim("report.html")
        self.now += timedelta(hours=12)
        self.assertTrue(self.store.renew("report.html", run_id))
        self.assertEqual(self.store.read("report.html").metadata["processing"], "true")
        self.assertIsNone(self.store.claim("report.html"))

    async def test_expired_heartbeat_allows_retry_with_new_ownership(self):
        old = self.store.claim("report.html")
        self.now += timedelta(seconds=STALE_AFTER_SECONDS)
        new = self.store.claim("report.html")
        self.assertNotEqual(old, new)
        self.assertTrue(self.store.owns("report.html", new))
        self.assertNotIn("last_error_message", self.blob.metadata)

    async def test_stale_worker_cannot_renew_or_finish_new_run(self):
        old = self.store.claim("report.html")
        self.now += timedelta(seconds=STALE_AFTER_SECONDS)
        new = self.store.claim("report.html")
        self.assertFalse(self.store.renew("report.html", old))
        self.assertFalse(self.store.finish("report.html", old, "completed"))
        self.assertTrue(self.store.owns("report.html", new))

    async def test_polling_race_does_not_overwrite_a_worker_heartbeat(self):
        run_id = self.store.claim("report.html")
        self.now += timedelta(seconds=STALE_AFTER_SECONDS)
        self.blob.before_write = lambda: self.store.renew("report.html", run_id)
        self.assertEqual(self.store.read("report.html").metadata["processing"], "true")
        self.assertTrue(self.store.owns("report.html", run_id))

    async def test_concurrent_requests_claim_only_one_worker(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            claims = list(pool.map(lambda _: self.store.claim("report.html"), range(8)))
        self.assertEqual(sum(value is not None for value in claims), 1)

    async def test_completed_run_with_leftover_processing_flag_stays_completed(self):
        self.blob.metadata.update(processing="true", last_status="completed")
        metadata = self.store.read("report.html").metadata
        self.assertEqual(metadata["last_status"], "completed")
        self.assertNotIn("processing", metadata)

    async def test_invalid_heartbeat_is_recoverable(self):
        for timestamp in ("broken", "2026-10-20T00:00:00"):
            with self.subTest(timestamp=timestamp):
                self.legacy_run()
                self.blob.modified = self.now - timedelta(hours=12)
                self.blob.metadata["processing_heartbeat_at"] = timestamp
                self.assertEqual(self.store.read("report.html").metadata["last_status"], "failed")

    async def test_completion_clears_ownership_and_errors_atomically(self):
        run_id = self.store.claim("report.html")
        self.assertTrue(self.store.finish("report.html", run_id, "completed"))
        self.assertEqual(self.blob.metadata, {"customer_name": "Synthetic", "system_id": "TST",
                                             "last_status": "completed"})

    async def test_failure_metadata_retains_rate_limit_and_timeout_hints(self):
        for error, code in (("rate limit 429", "429"), ("request timeout", "504"),
                            ("unexpected \u2014 error\nwith newline", "500")):
            with self.subTest(error=error):
                run_id = self.store.claim("report.html")
                self.assertTrue(self.store.finish("report.html", run_id, "failed", error))
                self.assertEqual(self.blob.metadata["last_error_status_code"], code)
                self.blob.metadata["last_error_message"].encode("ascii")
                self.assertNotIn("\n", self.blob.metadata["last_error_message"])

    async def test_status_poll_returns_failed_for_legacy_orphan(self):
        self.legacy_run()
        self.container.list_blobs.return_value = [SimpleNamespace(name="TST_06_Sep_26.html",
                last_modified=self.blob.modified, size=42)]
        with patch.object(storage_router, "blob_service_client", self.client):
            response = await storage_router.list_files(_user={})
        item, = response["files"]
        self.assertFalse(item["processing"])
        self.assertEqual(item["last_status"], "failed")
        self.assertEqual(item["last_error_hint"], INTERRUPTED_MESSAGE)

    async def test_repeated_polling_does_not_rewrite_terminal_status(self):
        self.legacy_run()
        self.store.read("report.html")
        version = self.blob.version
        self.store.read("report.html")
        self.assertEqual(self.blob.version, version)

    async def test_storage_failure_does_not_enqueue_untracked_work(self):
        background = BackgroundTasks()
        with patch.object(ai_router, "blob_service_client", self.client), \
                patch.object(ai_router.ewa_orchestrator, "processing_state", self.store), \
                patch.object(self.store, "claim", side_effect=RuntimeError("Synthetic storage outage")):
            with self.assertRaises(ai_router.HTTPException):
                await ai_router.process_and_analyze_document_endpoint(
                    ProcessAnalyzeRequest(blob_name="report.html"), background, _user={})
        self.assertEqual(background.tasks, [])

    async def test_both_start_endpoints_recover_orphans_and_enqueue_once(self):
        for endpoint in (ai_router.process_and_analyze_document_endpoint,
                         ai_router.reprocess_document_with_ai):
            with self.subTest(endpoint=endpoint.__name__):
                self.blob.metadata = {"customer_name": "Synthetic", "system_id": "TST"}
                self.legacy_run()
                self.blob.modified = self.now - timedelta(hours=12)
                background = BackgroundTasks()
                with patch.object(ai_router, "blob_service_client", self.client), \
                        patch.object(ai_router.ewa_orchestrator, "processing_state", self.store):
                    response = await endpoint(ProcessAnalyzeRequest(blob_name="report.html"), background, _user={})
                    duplicate = await endpoint(ProcessAnalyzeRequest(blob_name="report.html"), background, _user={})
                self.assertTrue(response["started"])
                self.assertFalse(duplicate["started"])
                self.assertEqual(len(background.tasks), 1)
                self.assertEqual(background.tasks[0].args, ("report.html", self.blob.metadata["processing_run_id"]))

    async def run_flow(self, result=None, error=None):
        run_id = self.store.claim("report.html")
        execute = AsyncMock(return_value=result, side_effect=error)
        with patch.object(ai_router, "blob_service_client", self.client), \
                patch.object(ai_router.ewa_orchestrator, "processing_state", self.store), \
                patch.object(ai_router.ewa_orchestrator, "execute_workflow", execute):
            return await ai_router._run_processing_flow("report.html", run_id)

    async def test_worker_success_clears_processing(self):
        await self.run_flow(result={"success": True})
        self.assertEqual(self.blob.metadata["last_status"], "completed")
        self.assertNotIn("processing", self.blob.metadata)

    async def test_worker_failed_result_and_exception_clear_processing(self):
        await self.run_flow(result={"success": False, "message": "Synthetic failure"})
        self.assertEqual(self.blob.metadata["last_status"], "failed")
        self.assertEqual(self.blob.metadata["last_error_message"], "Synthetic failure")
        with self.assertRaisesRegex(RuntimeError, "Synthetic exception"):
            await self.run_flow(error=RuntimeError("Synthetic exception"))
        self.assertEqual(self.blob.metadata["last_status"], "failed")
        self.assertNotIn("processing", self.blob.metadata)

    async def test_worker_cancellation_records_retryable_interruption(self):
        with self.assertRaises(asyncio.CancelledError):
            await self.run_flow(error=asyncio.CancelledError())
        self.assertEqual(self.blob.metadata["last_status"], "failed")
        self.assertEqual(self.blob.metadata["last_error_hint"], INTERRUPTED_MESSAGE)
        self.assertNotIn("processing", self.blob.metadata)

    async def test_heartbeat_is_renewed_while_worker_waits(self):
        run_id = self.store.claim("report.html")
        renewed = asyncio.Event()
        renew = self.store.renew

        def observe(*args):
            value = renew(*args)
            loop.call_soon_threadsafe(renewed.set)
            return value

        loop = asyncio.get_running_loop()
        with patch.object(self.store, "renew", side_effect=observe), \
                patch.object(ai_router.ewa_orchestrator, "processing_state", self.store), \
                patch.object(ai_router, "HEARTBEAT_INTERVAL_SECONDS", 0.001):
            heartbeat = asyncio.create_task(ai_router._heartbeat_processing("report.html", run_id,
                                                                           asyncio.current_task()))
            try:
                await asyncio.wait_for(renewed.wait(), 2)
            finally:
                heartbeat.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await heartbeat
        self.assertTrue(self.store.owns("report.html", run_id))

    async def test_retired_run_cannot_publish_workbook(self):
        orchestrator = EWAWorkflowOrchestrator()
        orchestrator.processing_state = self.store
        run_id = self.store.claim("report.html")
        self.now += timedelta(seconds=STALE_AFTER_SECONDS)
        self.store.read("report.html")
        with patch("workflow_orchestrator.storage_service.get_text_content", return_value="<p>Synthetic</p>"), \
                patch.object(orchestrator, "_run_pipeline_sync", return_value={"success": True}), \
                patch.object(orchestrator, "_upload_artifacts", new_callable=AsyncMock) as upload:
            with self.assertRaises(asyncio.CancelledError):
                await orchestrator.execute_workflow("report.html", processing_run_id=run_id)
        upload.assert_not_called()

    async def test_heartbeat_cancels_worker_that_lost_ownership(self):
        worker = asyncio.create_task(asyncio.Event().wait())
        with patch.object(ai_router.ewa_orchestrator, "processing_state", self.store), \
                patch.object(ai_router, "HEARTBEAT_INTERVAL_SECONDS", 0.001):
            await ai_router._heartbeat_processing("report.html", "retired-run", worker)
        with self.assertRaises(asyncio.CancelledError):
            await worker


if __name__ == "__main__":
    unittest.main()
