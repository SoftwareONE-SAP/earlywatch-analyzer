"""Small client for Microsoft's Decision-1 model (Azure AI Foundry).

Decision-1 answers a yes/no question about some context with a probability.
It is switched off by default (config.decision_enabled) and never raises:
on any problem it logs a warning and returns {}, so callers can fall back.
"""
from __future__ import annotations

import logging
from typing import Any, Callable
from urllib.parse import urlsplit

import requests

from ewa_pipeline.config import Config

log = logging.getLogger(__name__)

DECISION_PATH = "/providers/microsoft/v1/systemone"


def _decision_url(endpoint: str) -> str:
    """Keep scheme + host of the Azure endpoint; drop any path."""
    parts = urlsplit(endpoint.strip())
    return f"{parts.scheme}://{parts.netloc}{DECISION_PATH}"


def decide(question: str, options: dict[str, str], context: Any, *, config: Config,
           name: str = "answer", timeout: float = 30.0,
           post: Callable[..., Any] | None = None) -> dict[str, float]:
    """Ask one yes/no question. Returns {"true": p, "false": 1 - p}, or {} on any failure.

    `options` is the criteria dict, {"true": <what yes means>, "false": <what no means>}.
    Only the "noul" question type (a probability for "true") is supported; that is
    all the alert-matching step needs. `context` is the state: a string or a JSON object.
    """
    if not config.decision_enabled:
        return {}
    post = post or requests.post
    url = _decision_url(config.azure_openai.endpoint)
    headers = {
        "api-key": config.azure_openai.api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = {
        "model": config.decision_model,
        "state": context,
        "questions": {name: {"type": "noul", "instructions": question, "criteria": options}},
    }
    try:
        response = post(url, headers=headers, json=body, timeout=timeout)
        if not 200 <= response.status_code < 300:
            log.warning("Decision model returned HTTP %s", response.status_code)
            return {}
        probability = response.json()["answers"][name]["noul"]
    except Exception as exc:  # network, bad JSON, missing keys: never break the caller
        log.warning("Decision model call failed: %s", type(exc).__name__)
        return {}
    if isinstance(probability, bool) or not isinstance(probability, (int, float)) \
            or not 0.0 <= probability <= 1.0:
        log.warning("Decision model returned an unusable value")
        return {}
    return {"true": float(probability), "false": 1.0 - float(probability)}
