"""Runtime configuration loaded from environment with defaults."""
from __future__ import annotations

import os


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


CHAT_HISTORY_LIMIT = _get_int("CHAT_HISTORY_LIMIT", 10)
CHAT_MAX_OUTPUT_TOKENS = _get_int("CHAT_MAX_OUTPUT_TOKENS", 4096)

# Azure runtime and Entra ID authentication
ENVIRONMENT = os.getenv("ENVIRONMENT", "local").strip().lower()
DISABLE_API_DOCS = _get_bool("DISABLE_API_DOCS", ENVIRONMENT in {"production", "prod"})

ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID", "").strip()
ENTRA_API_CLIENT_ID = os.getenv("ENTRA_API_CLIENT_ID", "").strip()
ENTRA_API_AUDIENCE = os.getenv("ENTRA_API_AUDIENCE", "").strip()
ENTRA_ISSUER = os.getenv("ENTRA_ISSUER", "").strip()

AUTH_ENABLED = _get_bool(
    "AUTH_ENABLED",
    ENVIRONMENT not in {"local", "development", "dev"},
)

TRUST_PLATFORM_AUTH_HEADERS = _get_bool("TRUST_PLATFORM_AUTH_HEADERS", False)
