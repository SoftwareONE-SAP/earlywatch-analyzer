"""Recoverable ownership of in-process analysis jobs, persisted on source blobs."""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from azure.core import MatchConditions
from azure.core.exceptions import ResourceModifiedError


HEARTBEAT_INTERVAL_SECONDS = 30
STALE_AFTER_SECONDS = 300
INTERRUPTED_MESSAGE = (
    "Analysis was interrupted because its worker stopped reporting progress. "
    "Please run the analysis again."
)
_RUN_KEYS = ("processing", "processing_run_id", "processing_started_at",
             "processing_heartbeat_at", "processing_revision")
_ERROR_KEYS = ("last_error_message", "last_error_hint", "last_error_status_code")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _clear_run(metadata: dict) -> None:
    for key in _RUN_KEYS:
        metadata.pop(key, None)


def _recover(metadata: dict, last_modified: datetime, now: datetime) -> bool:
    """Expire missing heartbeats; legacy runs use their blob modification time."""
    if metadata.get("processing") != "true" and metadata.get("last_status") != "processing":
        return False
    if metadata.get("last_status") in {"completed", "failed"}:
        _clear_run(metadata)
        return True
    try:
        heartbeat = datetime.fromisoformat(metadata["processing_heartbeat_at"])
        if heartbeat.tzinfo is None:
            raise ValueError("Heartbeat requires a timezone")
    except (KeyError, TypeError, ValueError):
        heartbeat = last_modified
    if now - heartbeat < timedelta(seconds=STALE_AFTER_SECONDS):
        return False
    _clear_run(metadata)
    metadata.update(last_status="failed", last_error_status_code="503",
                    last_error_message=INTERRUPTED_MESSAGE,
                    last_error_hint=INTERRUPTED_MESSAGE)
    return True


class ProcessingStateStore:
    def __init__(self, blob_service_client, container_name):
        self.client = blob_service_client
        self.container = container_name

    def _blob(self, name):
        return self.client.get_blob_client(container=self.container, blob=name)

    @staticmethod
    def _write(blob, props, metadata):
        # A heartbeat or a new claim must not be overwritten by stale polling.
        blob.set_blob_metadata(metadata, etag=props.etag,
                               match_condition=MatchConditions.IfNotModified)

    def read(self, name):
        """Return current properties, marking an abandoned run retryable."""
        blob = self._blob(name)
        for attempt in range(3):
            props = blob.get_blob_properties()
            metadata = dict(props.metadata or {})
            if not _recover(metadata, props.last_modified, _now()):
                return props
            try:
                self._write(blob, props, metadata)
                return blob.get_blob_properties()
            except ResourceModifiedError:
                if attempt == 2:
                    raise

    def claim(self, name):
        """Atomically claim a new run, or return None for a live owner."""
        blob = self._blob(name)
        for attempt in range(3):
            props = blob.get_blob_properties()
            metadata = dict(props.metadata or {})
            now = _now()
            _recover(metadata, props.last_modified, now)
            if metadata.get("processing") == "true" or metadata.get("last_status") == "processing":
                return None
            run_id = uuid4().hex
            for key in _ERROR_KEYS:
                metadata.pop(key, None)
            metadata.update(processing="true", last_status="processing",
                            processing_run_id=run_id, processing_started_at=now.isoformat(),
                            processing_heartbeat_at=now.isoformat(),
                            processing_revision=os.getenv("CONTAINER_APP_REVISION", "local"))
            try:
                self._write(blob, props, metadata)
                return run_id
            except ResourceModifiedError:
                if attempt == 2:
                    raise

    def owns(self, name, run_id):
        props = self._blob(name).get_blob_properties()
        metadata = props.metadata or {}
        return metadata.get("processing_run_id") == run_id and metadata.get("processing") == "true"

    def renew(self, name, run_id):
        blob = self._blob(name)
        for attempt in range(3):
            props = blob.get_blob_properties()
            metadata = dict(props.metadata or {})
            if metadata.get("processing_run_id") != run_id or metadata.get("processing") != "true":
                return False
            metadata["processing_heartbeat_at"] = _now().isoformat()
            try:
                self._write(blob, props, metadata)
                return True
            except ResourceModifiedError:
                if attempt == 2:
                    raise

    def finish(self, name, run_id, status, error_message=None):
        blob = self._blob(name)
        for attempt in range(3):
            props = blob.get_blob_properties()
            metadata = dict(props.metadata or {})
            if metadata.get("processing_run_id") != run_id:
                return False
            _clear_run(metadata)
            for key in _ERROR_KEYS:
                metadata.pop(key, None)
            metadata["last_status"] = status
            if error_message:
                # Blob metadata travels in HTTP headers and must be ASCII.
                message = str(error_message).encode("ascii", "replace").decode("ascii")
                message = " ".join(message.split())[:512]
                code = "500"
                hint = "An unexpected error occurred during analysis. Check server logs."
                if error_message == INTERRUPTED_MESSAGE:
                    code, hint = "503", INTERRUPTED_MESSAGE
                elif "rate limit" in message.lower() or "429" in message:
                    code = "429"
                    hint = "The AI service is temporarily overloaded. Please try again in a few minutes."
                elif "timeout" in message.lower():
                    code = "504"
                    hint = "The analysis timed out. The document may be too large."
                metadata.update(last_error_message=message, last_error_hint=hint,
                                last_error_status_code=code)
            try:
                self._write(blob, props, metadata)
                return True
            except ResourceModifiedError:
                if attempt == 2:
                    raise
