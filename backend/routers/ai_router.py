"""AI analysis and workflow routes extracted from ewa_main.py.

Endpoints:
- POST /api/process-and-analyze        (combined conversion + analysis)
- POST /api/analyze-ai                 (analyze normalized HTML with AI)
- POST /api/reprocess-ai               (delete old AI files then analyze again)
"""

from __future__ import annotations

import asyncio
import os
import logging
from contextlib import suppress
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from models import BlobNameRequest
from models.request_models import ProcessAnalyzeRequest

from core.azure_clients import (
    blob_service_client,
    AZURE_STORAGE_CONTAINER_NAME,
)
from workflow_orchestrator import ewa_orchestrator
from core.entra_auth import require_auth
from services.processing_state import HEARTBEAT_INTERVAL_SECONDS, INTERRUPTED_MESSAGE

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["ai-workflow"])


async def _heartbeat_processing(blob_name: str, run_id: str, worker: asyncio.Task):
    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)
        try:
            owned = await asyncio.to_thread(ewa_orchestrator.processing_state.renew, blob_name, run_id)
        except Exception:
            logger.warning("[PROCESS] Could not renew worker heartbeat for %s", blob_name, exc_info=True)
            continue
        if not owned:
            logger.warning("[PROCESS] Worker lost ownership of %s; stopping its workflow", blob_name)
            worker.cancel()
            return


async def _run_processing_flow(original_blob_name: str, run_id: str) -> Dict[str, Any]:
    worker = asyncio.create_task(_execute_processing_flow(original_blob_name, run_id))
    heartbeat = asyncio.create_task(_heartbeat_processing(original_blob_name, run_id, worker))
    try:
        return await worker
    finally:
        heartbeat.cancel()
        with suppress(asyncio.CancelledError):
            await heartbeat


async def _execute_processing_flow(original_blob_name: str, run_id: str) -> Dict[str, Any]:
    base_name, _ = os.path.splitext(original_blob_name)
    html_blob_name = original_blob_name if original_blob_name.lower().endswith((".htm", ".html")) else f"{base_name}.html"
    container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

    try:
        if not await asyncio.to_thread(ewa_orchestrator.processing_state.owns, original_blob_name, run_id):
            raise asyncio.CancelledError("Analysis run no longer owns this document")
        # Delete all derived artifacts except the original and normalized source files.
        logger.info("[PROCESS] Cleaning derived blobs for %s", base_name)
        try:
            preserved = {original_blob_name, html_blob_name}
            blob_list = container_client.list_blobs(name_starts_with=base_name)
            for blob in blob_list:
                if blob.name in preserved:
                    continue
                blob_client = container_client.get_blob_client(blob.name)
                blob_client.delete_blob()
                logger.info("[PROCESS] Deleted %s", blob.name)
        except Exception as e:
            logger.warning("[PROCESS] Error deleting derived blobs: %s", e)

        # Ensure normalized source exists.
        try:
            html_client = container_client.get_blob_client(html_blob_name)
            if not html_client.exists():
                logger.error("[PROCESS] Normalized source missing for %s", original_blob_name)
                raise HTTPException(
                    status_code=404,
                    detail=f"{html_blob_name} was not found. Please re-upload the report.",
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("[PROCESS] Missing normalized source: %s", e)
            raise HTTPException(status_code=500, detail=f"Error accessing normalized source: {str(e)}")

        # Run analysis (normalized source guaranteed to exist)
        logger.info("[PROCESS] Starting workflow execution for %s", original_blob_name)
        result = await ewa_orchestrator.execute_workflow(original_blob_name, processing_run_id=run_id)
        await asyncio.to_thread(
            ewa_orchestrator.processing_state.finish, original_blob_name, run_id,
            "completed" if result.get("success") else "failed",
            None if result.get("success") else result.get("message", "Analysis failed. Please try again."),
        )
        logger.info("[PROCESS] Workflow completed with result: %s", result)
        return result
    except asyncio.CancelledError:
        logger.warning("[PROCESS] Analysis interrupted for %s", original_blob_name)
        raise
    except Exception as exc:
        await asyncio.to_thread(ewa_orchestrator.processing_state.finish,
                              original_blob_name, run_id, "failed",
                              str(getattr(exc, "detail", exc)))
        raise
    finally:
        # Conditional ownership prevents an old worker from clearing a newer run.
        try:
            await asyncio.to_thread(ewa_orchestrator.processing_state.finish,
                                  original_blob_name, run_id, "failed", INTERRUPTED_MESSAGE)
        except Exception:
            logger.warning("[PROCESS] Could not finish metadata for %s; heartbeat expiry will recover it",
                           original_blob_name, exc_info=True)




# ---------------------------------------------------------------------------
# Combined process + analyze
# ---------------------------------------------------------------------------

@router.post("/process-and-analyze")
async def process_and_analyze_document_endpoint(
    request: ProcessAnalyzeRequest,
    background_tasks: BackgroundTasks,
    _user: dict = Depends(require_auth()),
):
    if not blob_service_client:
        raise HTTPException(status_code=500, detail="Azure Blob Service client not initialized.")
    try:
        blob_name = request.blob_name

        # Claim atomically, recovering an interrupted run before allowing a retry.
        run_id = await asyncio.to_thread(ewa_orchestrator.processing_state.claim, blob_name)
        if run_id is None:
            return {
                "success": True,
                "started": False,
                "message": "Processing is already running for this file.",
                "original_file": blob_name,
            }

        background_tasks.add_task(_run_processing_flow, blob_name, run_id)

        return {
            "success": True,
            "started": True,
            "message": "Processing started. Status will update automatically.",
            "original_file": blob_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# ---------------------------------------------------------------------------
# Analyze normalized source only
# ---------------------------------------------------------------------------

@router.post("/analyze-ai")
async def analyze_document_with_ai_endpoint(
    request: BlobNameRequest,
    _user: dict = Depends(require_auth()),
):
    if not blob_service_client:
        raise HTTPException(status_code=500, detail="Azure Blob Service client not initialized.")

    blob_name = request.blob_name
    base_name, extension = os.path.splitext(blob_name)
    html_file = blob_name if extension.lower() in {".htm", ".html"} else f"{base_name}.html"

    container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
    try:
        html_client = container_client.get_blob_client(html_file)
        if not html_client.exists():
            raise FileNotFoundError
    except Exception:
        raise HTTPException(status_code=404, detail=f"{html_file} was not found. Please process the document first.")

    try:
        result = await ewa_orchestrator.execute_workflow(html_file)
        if not result.get("success", False):
            raise HTTPException(
                status_code=result.get("status_code", 500),
                detail=result.get("error_hint") or result.get("message", "Analysis failed"),
            )
        return {
            "success": True,
            "message": "Agentic analysis completed successfully",
            "original_file": blob_name,
            "workbook_file": result.get("workbook_file"),
            "workbook_payload_file": result.get("workbook_payload_file"),
            "usage_file": result.get("usage_file"),
            "total_findings": result.get("total_findings", 0),
            "total_parameters": result.get("total_parameters", 0),
            "supplemental_findings": result.get("supplemental_findings", 0),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ---------------------------------------------------------------------------
# Re-process AI
# ---------------------------------------------------------------------------

@router.post("/reprocess-ai")
async def reprocess_document_with_ai(
    request: BlobNameRequest,
    background_tasks: BackgroundTasks,
    _user: dict = Depends(require_auth()),
):
    if not blob_service_client:
        raise HTTPException(status_code=500, detail="Azure Blob Service client not initialized.")

    original_blob_name = request.blob_name
    logger.info("[REPROCESS] Starting reprocess for %s", original_blob_name)

    try:
        run_id = await asyncio.to_thread(ewa_orchestrator.processing_state.claim, original_blob_name)
        if run_id is None:
            return {
                "success": True,
                "started": False,
                "message": "Re-analysis is already running for this file.",
                "original_file": original_blob_name,
            }

        background_tasks.add_task(_run_processing_flow, original_blob_name, run_id)

        logger.info("[REPROCESS] Re-analysis queued for %s", original_blob_name)
        return {
            "success": True,
            "started": True,
            "message": "Re-analysis started. Status will update automatically.",
            "original_file": original_blob_name,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("[REPROCESS] Exception during workflow execution: %s", e)
        raise HTTPException(status_code=500, detail=f"Re-analysis failed: {str(e)}")
