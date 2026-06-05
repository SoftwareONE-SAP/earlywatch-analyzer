"""Chat endpoint extracted from ewa_main.py.

This is functionally identical to the previous implementation, just wrapped in an APIRouter so
that main stays slim.  No behavioural changes.
"""

from __future__ import annotations

import os
import traceback
import logging
import json
import re
import tempfile
from pathlib import Path
from typing import List, Dict, Any
import asyncio

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv

from services.storage_service import StorageService
from core.entra_auth import require_auth
from core.runtime_config import (
    CHAT_HISTORY_LIMIT,
    CHAT_MAX_OUTPUT_TOKENS,
    CHAT_NODE_CANDIDATE_LIMIT,
    CHAT_NODE_CONTEXT_CHARS,
    CHAT_NODE_TEXT_SCAN_CHARS,
)

# Lazy import AzureOpenAI only when needed to avoid cost at module load

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatHistoryItem(BaseModel):
    text: str
    isUser: bool = True


class ChatRequest(BaseModel):
    message: str
    fileName: str
    documentContent: str
    fileOrigin: str = ""
    contentLength: int = 0
    chatHistory: List[Dict[str, Any]] = []


@router.post("/chat")
async def chat_with_document(
    request: ChatRequest,
    _user: dict = Depends(require_auth()),
):
    """Chat with a processed EWA document using Azure OpenAI GPT models."""
    # DEBUG: Log incoming request summary
    logger.info("----- /api/chat CALL -----")
    try:
        logger.info(
            "file=%s, message_len=%s, content_len=%s, history_len=%s",
            request.fileName,
            len(request.message),
            len(request.documentContent),
            len(request.chatHistory),
        )
    except Exception as _logerr:
        logger.warning("Logging error: %s", _logerr)
    try:
        load_dotenv()
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_name = os.getenv("V2_ORCHESTRATOR_MODEL", "gpt-4.1")
        logger.info("Azure endpoint set: %s, model: %s", bool(azure_endpoint), model_name)

        if not api_key or not azure_endpoint:
            raise HTTPException(status_code=500, detail="Azure OpenAI environment variables missing.")

        from openai import AzureOpenAI  # local import to keep module import light

        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )

        # Keep only recent history and reuse for retrieval + answer generation.
        recent_history = (
            request.chatHistory[-CHAT_HISTORY_LIMIT:]
            if len(request.chatHistory) > CHAT_HISTORY_LIMIT
            else request.chatHistory
        )

        # Fetch normalized source from storage first; fallback to incoming payload.
        document_content = (request.documentContent or "").strip()
        tree: dict[str, Any] | None = None
        selected_doc_context = ""
        try:
            if request.fileName:
                storage = StorageService()
                base, _ = os.path.splitext(request.fileName)
                html_filename = f"{base}.html"
                md_filename = f"{base}.md"
                source_filename = html_filename
                try:
                    fetched_content = await asyncio.to_thread(lambda: storage.get_text_content(html_filename))
                except FileNotFoundError:
                    source_filename = md_filename
                    fetched_content = await asyncio.to_thread(lambda: storage.get_text_content(md_filename))
                if fetched_content:
                    document_content = fetched_content.strip()

                if document_content:
                    tree = await _load_or_build_tree(storage, source_filename, document_content)
                    selected_doc_context = _build_relevant_context(
                        tree=tree,
                        question=request.message,
                        chat_history=recent_history,
                    )

                # Also try to fetch the structured findings payload as extra context
                try:
                    payload_blob = f"{base}_workbook_payload.json"
                    payload_content = await asyncio.to_thread(lambda: storage.get_text_content(payload_blob))
                    if payload_content:
                        selected_doc_context += (
                            f"\n\n--- EXTRACTED WORKBOOK FINDINGS (JSON) ---\n"
                            f"{payload_content.strip()}\n"
                            f"--- END EXTRACTED WORKBOOK FINDINGS ---\n"
                        )
                except Exception as p_err:
                    logger.info("Workbook payload not found or could not be fetched for %s: %s", request.fileName, p_err)

        except Exception as e:
            logger.warning("Storage fetch failed (using fallback): %s", e)

        # Fallback: if tree retrieval yields nothing, keep only a bounded excerpt.
        if not selected_doc_context and document_content:
            selected_doc_context = document_content[:CHAT_NODE_CONTEXT_CHARS]

        if not selected_doc_context:
            raise HTTPException(status_code=400, detail="Document content is missing. Please process the document first.")

        system_instruction = _build_system_prompt(request.fileName, selected_doc_context)

        # Build Responses API input messages with selected node context and chat history.
        responses_messages = []
        responses_messages.append({
            "role": "system",
            "content": [{"type": "input_text", "text": system_instruction}],
        })

        # Include recent chat history (text only)
        for msg in recent_history:
            role = "user" if msg.get("isUser") else "assistant"
            text = msg.get("text", "")
            content_type = "input_text" if role == "user" else "output_text"
            responses_messages.append({
                "role": role,
                "content": [{"type": content_type, "text": text}],
            })

        # Current user turn: just the user's question (no file attachment)
        responses_messages.append({
            "role": "user",
            "content": [
                {"type": "input_text", "text": request.message},
            ],
        })

        try:
            # Use Azure OpenAI Responses API (GPT-5 compatible) off the event loop
            response = await asyncio.to_thread(
                lambda: client.responses.create(
                    model=model_name,
                    input=responses_messages,
                    max_output_tokens=CHAT_MAX_OUTPUT_TOKENS,
                    reasoning={"effort": "medium"},
                    text={"verbosity": "low"},
                )
            )
            # Log token usage if available
            try:
                usage = getattr(response, "usage", None)
                if usage is not None:
                    in_tok = getattr(usage, "input_tokens", None) if hasattr(usage, "input_tokens") else (usage.get("input_tokens") if isinstance(usage, dict) else None)
                    out_tok = getattr(usage, "output_tokens", None) if hasattr(usage, "output_tokens") else (usage.get("output_tokens") if isinstance(usage, dict) else None)
                    logger.info("Token usage: input_tokens=%s, output_tokens=%s", in_tok, out_tok)
            except Exception:
                pass

            ai_response = getattr(response, "output_text", None)
            if not ai_response:
                # Fallback: try to stringify response for debugging context
                try:
                    ai_response = response.model_dump_json() if hasattr(response, "model_dump_json") else str(response)
                except Exception:
                    ai_response = ""
            return {"response": ai_response}
        except Exception as api_err:
            logger.exception("OpenAI API error: %s", api_err)
            err_text = _humanize_openai_error(api_err, model_name)
            raise HTTPException(status_code=500, detail=f"Open AI API error: {err_text}")

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Chat endpoint error: %s", e)
        raise HTTPException(status_code=500, detail="Unexpected server error in chat endpoint.")


# Path to system prompt template
_PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts", "chat_system_prompt.md")


def _build_system_prompt(filename: str, doc_content: str) -> str:
    """Return the chat system prompt, loading from markdown template if present."""
    if os.path.exists(_PROMPT_PATH):
        with open(_PROMPT_PATH, "r", encoding="utf-8") as _f:
            template = _f.read()
        return template.format(filename=filename, doc_content=doc_content)

    # Fallback inline prompt (legacy)
    return (
        "You are an expert SAP Basis Architect specialized in analyzing SAP Early Watch Alert (EWA) reports.\n\n"
        f"DOCUMENT: {filename}\nCONTENT:\n{doc_content}\n\n"
        "IMPORTANT INSTRUCTIONS:\n1. This is an SAP Early Watch Alert (EWA) report which contains system performance metrics, issues, warnings, and recommendations.\n"
        "2. The report typically covers areas like database statistics, memory usage, backup frequency, system availability, and performance parameters.\n"
        "3. When answering questions, focus on extracting SPECIFIC INFORMATION from the document, even if it's just a brief mention.\n"
        "4. If information is present but brief, explain it and note that limited details are available.\n"
        "5. Be especially attentive to technical metrics, parameter recommendations, and critical warnings in the report.\n"
        "6. Quote specific sections and values from the report whenever possible.\n"
        "7. If you truly cannot find ANY mention of a topic, only then state that it's not in the document.\n"
        "8. The CONTENT may include an \"EXTRACTED WORKBOOK FINDINGS (JSON)\" section at the end. This JSON contains the structured observations, findings, and recommendations generated by the orchestrator system (often carrying IDs like SEC-01, PERF-02, etc.). Use this JSON data to explain these specific findings in detail when the user asks about them, quoting the underlying context from the report.\n\n"
        "DIRECTING USERS TO SPECIALIZED SECTIONS:\n1. This application has DEDICATED SECTIONS for Key Metrics and Parameters that provide more detailed and structured information.\n"
        "2. When users ask about specific metrics, give a brief summary (exclude numeric values) and direct them explicitly to the Key Metrics section.\n"
        "3. When users ask about parameters, give a brief summary (exclude numeric values) and direct them explicitly to the Parameters section.\n\n"
        "Provide technically precise answers in Markdown."
    )


def _humanize_openai_error(err: Exception, model_name: str) -> str:
    txt = str(err).lower()
    if "not found" in txt and "model" in txt:
        return f"Model '{model_name}' not found. Please check configuration."
    if "deploymentnotfound" in txt or "deployment not found" in txt:
        return f"Deployment '{model_name}' not found. Verify Azure deployment name and AZURE_OPENAI_* environment variables."
    if "authenticate" in txt or "key" in txt:
        return "Authentication error. Please check Azure OpenAI API key and endpoint."
    if "rate limit" in txt:
        return "Rate limit exceeded. Please try again later."
    return str(err)


def _iter_nodes(nodes: List[Dict[str, Any]], path: str = ""):
    for node in nodes or []:
        title = (node.get("title") or "").strip()
        current_path = f"{path} > {title}" if path and title else (title or path)
        yield node, current_path
        yield from _iter_nodes(node.get("nodes") or [], current_path)


def _tokenize(text: str) -> set[str]:
    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "what", "when", "where", "which",
        "about", "have", "has", "into", "your", "their", "there", "please", "show", "list", "give",
        "does", "how", "why", "can", "could", "would", "will", "are", "was", "were", "been", "also",
        "not", "all", "any", "our", "you", "its", "sap", "ewa", "report", "document",
    }
    tokens = set(re.findall(r"[a-z0-9_]{3,}", (text or "").lower()))
    return {t for t in tokens if t not in stopwords}


def _score_node(node: Dict[str, Any], query_terms: set[str]) -> int:
    title = (node.get("title") or "").lower()
    summary = (node.get("summary") or node.get("prefix_summary") or "").lower()
    text = (node.get("text") or "")[:CHAT_NODE_TEXT_SCAN_CHARS].lower()

    score = 0
    for term in query_terms:
        if term in title:
            score += 6
        if term in summary:
            score += 3
        if term in text:
            score += 1
    return score


def _build_relevant_context(tree: Dict[str, Any], question: str, chat_history: List[Dict[str, Any]]) -> str:
    structure = tree.get("structure") or []
    if not structure:
        return ""

    history_text = "\n".join((msg.get("text") or "") for msg in chat_history if isinstance(msg, dict))
    query_terms = _tokenize(f"{question}\n{history_text}")
    if not query_terms:
        query_terms = _tokenize(question)

    scored: list[tuple[int, Dict[str, Any], str]] = []
    for node, node_path in _iter_nodes(structure):
        node_text = (node.get("text") or "").strip()
        if not node_text:
            continue
        score = _score_node(node, query_terms)
        if score > 0:
            scored.append((score, node, node_path))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_nodes = scored[:CHAT_NODE_CANDIDATE_LIMIT]

    # If lexical matching misses, fall back to top-level sections with text.
    if not top_nodes:
        for node, node_path in _iter_nodes(structure):
            node_text = (node.get("text") or "").strip()
            if node_text:
                top_nodes.append((0, node, node_path))
            if len(top_nodes) >= CHAT_NODE_CANDIDATE_LIMIT:
                break

    selected_blocks: list[str] = []
    current_chars = 0
    selected_ids: list[str] = []
    for _, node, node_path in top_nodes:
        node_id = str(node.get("node_id") or "")
        title = node.get("title") or ""
        line_num = node.get("line_num")
        text = (node.get("text") or "").strip()
        if not text:
            continue

        block = (
            f"--- NODE {node_id} ---\n"
            f"PATH: {node_path}\n"
            f"TITLE: {title}\n"
            f"LINE: {line_num}\n"
            f"CONTENT:\n{text}\n"
        )

        if current_chars + len(block) > CHAT_NODE_CONTEXT_CHARS and selected_blocks:
            break
        if current_chars + len(block) > CHAT_NODE_CONTEXT_CHARS:
            block = block[:CHAT_NODE_CONTEXT_CHARS]

        selected_blocks.append(block)
        current_chars += len(block)
        selected_ids.append(node_id)

    logger.info("Chat context selected %s node(s): %s", len(selected_ids), ",".join(selected_ids))
    return "\n\n".join(selected_blocks)


def _build_tree_from_markdown(md_filename: str, markdown_content: str) -> Dict[str, Any]:
    from pageindex import md_to_tree

    with tempfile.TemporaryDirectory() as temp_dir:
        md_path = os.path.join(temp_dir, md_filename)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return asyncio.run(
            md_to_tree(
                md_path=md_path,
                if_thinning=False,
                if_add_node_summary="no",
                if_add_doc_description="no",
                if_add_node_text="yes",
                if_add_node_id="yes",
            )
        )


def _build_tree_from_html(html_filename: str, html_content: str) -> Dict[str, Any]:
    from ewa_pipeline.indexer.html_tree_builder import build_document_tree_from_html

    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, html_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return build_document_tree_from_html(Path(html_path), Path(temp_dir))


async def _load_or_build_tree(storage: StorageService, source_filename: str, source_content: str) -> Dict[str, Any]:
    base, ext = os.path.splitext(source_filename)
    tree_blob = f"{base}_tree.json"

    try:
        tree_text = await asyncio.to_thread(lambda: storage.get_text_content(tree_blob))
        return json.loads(tree_text)
    except Exception:
        if ext.lower() in {".htm", ".html"}:
            tree = await asyncio.to_thread(_build_tree_from_html, source_filename, source_content)
        else:
            tree = await asyncio.to_thread(_build_tree_from_markdown, source_filename, source_content)
        try:
            await asyncio.to_thread(
                lambda: storage.upload_text_content(
                    tree_blob,
                    json.dumps(tree, ensure_ascii=False),
                    content_type="application/json",
                )
            )
        except Exception as cache_err:
            logger.info("Tree cache upload skipped for %s: %s", source_filename, cache_err)
        return tree
