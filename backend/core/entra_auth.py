"""Microsoft Entra ID JWT validation and role authorization helpers."""

from __future__ import annotations

import base64
import json
import logging
import time
from typing import Any, Callable

import jwt
import requests
from fastapi import HTTPException, Request, status
from jwt.algorithms import RSAAlgorithm
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.runtime_config import (
    AUTH_ENABLED,
    ENTRA_API_AUDIENCE,
    ENTRA_API_CLIENT_ID,
    ENTRA_ISSUER,
    ENTRA_TENANT_ID,
    ENVIRONMENT,
    TRUST_PLATFORM_AUTH_HEADERS,
)

logger = logging.getLogger(__name__)

VIEWER_ROLE = "Viewer"
ADMIN_ROLE = "Administrator"
VIEWER_OR_ADMIN = (VIEWER_ROLE, ADMIN_ROLE)

_PUBLIC_PATHS = frozenset({"/", "/health", "/api/ping"})
_KEY_CACHE_SECONDS = 3600


def _auth_configured() -> bool:
    return bool(ENTRA_TENANT_ID and ENTRA_API_CLIENT_ID)


def is_auth_enabled() -> bool:
    return AUTH_ENABLED and _auth_configured()


def _expected_issuer() -> str:
    if ENTRA_ISSUER:
        return ENTRA_ISSUER.rstrip("/")
    return f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/v2.0"


def _expected_audiences() -> list[str]:
    audiences = []
    if ENTRA_API_AUDIENCE:
        audiences.append(ENTRA_API_AUDIENCE)
    if ENTRA_API_CLIENT_ID:
        audiences.extend([ENTRA_API_CLIENT_ID, f"api://{ENTRA_API_CLIENT_ID}"])
    return list(dict.fromkeys(audiences))


class EntraAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.public_keys: dict[str, Any] = {}
        self._keys_cached_at = 0.0

        if AUTH_ENABLED and not _auth_configured():
            logger.error(
                "AUTH_ENABLED=true but ENTRA_TENANT_ID or ENTRA_API_CLIENT_ID is missing; "
                "protected requests will be rejected."
            )

    async def dispatch(self, request: Request, call_next):
        if request.url.path in _PUBLIC_PATHS:
            return await call_next(request)

        if not AUTH_ENABLED:
            request.state.user = _development_user()
            return await call_next(request)

        platform_user = _platform_authenticated_user(request)
        if platform_user:
            request.state.user = platform_user
            return await call_next(request)

        if not _auth_configured():
            return self._unauthorized("Authentication is not configured")

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return self._unauthorized("Missing Authorization header")

        token = auth_header.split(" ", 1)[1]
        try:
            claims = self._decode_token(token)
            if claims.get("tid") != ENTRA_TENANT_ID:
                logger.warning("Rejected token for unexpected tenant: %s", claims.get("tid"))
                return self._unauthorized("Invalid token tenant")

            request.state.user = _normalize_user(claims)
        except jwt.ExpiredSignatureError:
            return self._unauthorized("Token has expired")
        except jwt.InvalidTokenError as exc:
            logger.warning("Entra JWT validation failed: %s", exc)
            return self._unauthorized("Invalid token")
        except Exception as exc:
            logger.exception("Unexpected Entra auth failure: %s", exc)
            return self._unauthorized("Token validation failed")

        return await call_next(request)

    def _decode_token(self, token: str) -> dict[str, Any]:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        key = self._get_key(kid)
        if key is None:
            self._refresh_keys()
            key = self._get_key(kid)
        if key is None:
            raise jwt.InvalidTokenError("Unrecognised token key")

        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=_expected_audiences(),
            issuer=_expected_issuer(),
            options={"require": ["exp", "iss", "aud"]},
        )

    def _get_key(self, kid: str | None):
        if time.time() - self._keys_cached_at > _KEY_CACHE_SECONDS:
            self._refresh_keys()
        if kid and kid in self.public_keys:
            return self.public_keys[kid]
        return None

    def _refresh_keys(self) -> None:
        if not ENTRA_TENANT_ID:
            self.public_keys = {}
            self._keys_cached_at = time.time()
            return

        metadata_url = f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/v2.0/.well-known/openid-configuration"
        metadata = requests.get(metadata_url, timeout=10)
        metadata.raise_for_status()

        jwks_url = metadata.json().get("jwks_uri")
        if not jwks_url:
            raise jwt.InvalidTokenError("Missing jwks_uri in Entra metadata")

        jwks = requests.get(jwks_url, timeout=10)
        jwks.raise_for_status()

        self.public_keys = {
            key_info["kid"]: RSAAlgorithm.from_jwk(key_info)
            for key_info in jwks.json().get("keys", [])
            if key_info.get("kid")
        }
        self._keys_cached_at = time.time()
        logger.info("Cached %d Entra public key(s)", len(self.public_keys))

    @staticmethod
    def _unauthorized(detail: str) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": detail},
            headers={"WWW-Authenticate": "Bearer"},
        )


def _normalize_user(claims: dict[str, Any]) -> dict[str, Any]:
    roles = claims.get("roles") or []
    if isinstance(roles, str):
        roles = [roles]

    return {
        "id": claims.get("oid") or claims.get("sub"),
        "email": claims.get("preferred_username") or claims.get("email") or claims.get("upn"),
        "name": claims.get("name"),
        "roles": roles,
        "tenant_id": claims.get("tid"),
    }


def _platform_authenticated_user(request: Request) -> dict[str, Any] | None:
    if not TRUST_PLATFORM_AUTH_HEADERS:
        return None

    principal_header = request.headers.get("X-MS-CLIENT-PRINCIPAL", "")
    principal_id = request.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "").strip()
    principal_name = request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME", "").strip()

    if not any([principal_header, principal_id, principal_name]):
        return None

    claims_by_type: dict[str, list[str]] = {}
    name_type = ""
    role_type = ""

    if principal_header:
        try:
            decoded = base64.b64decode(principal_header)
            principal_payload = json.loads(decoded.decode("utf-8"))
            name_type = str(principal_payload.get("name_typ") or "")
            role_type = str(principal_payload.get("role_typ") or "")
            claims_by_type = _group_claims_by_type(principal_payload.get("claims") or [])
        except Exception as exc:
            logger.warning("Failed to decode X-MS-CLIENT-PRINCIPAL header: %s", exc)

    token_like_claims = {
        "oid": principal_id or _first_claim(
            claims_by_type,
            "http://schemas.microsoft.com/identity/claims/objectidentifier",
            "oid",
            "sub",
        ),
        "sub": principal_id or _first_claim(claims_by_type, "sub"),
        "preferred_username": principal_name or _first_claim(
            claims_by_type,
            "preferred_username",
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn",
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
        ),
        "email": principal_name or _first_claim(
            claims_by_type,
            "email",
            "emails",
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
            "preferred_username",
        ),
        "upn": principal_name or _first_claim(
            claims_by_type,
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn",
            "preferred_username",
        ),
        "name": principal_name or _first_claim(
            claims_by_type,
            name_type,
            "name",
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
            "preferred_username",
        ),
        "tid": _first_claim(
            claims_by_type,
            "http://schemas.microsoft.com/identity/claims/tenantid",
            "tid",
        ),
        "roles": _extract_roles(claims_by_type, role_type),
    }

    return _normalize_user(token_like_claims)


def _group_claims_by_type(claims: list[dict[str, Any]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for claim in claims:
        claim_type = str(claim.get("typ") or "").strip()
        claim_value = str(claim.get("val") or "").strip()
        if not claim_type or not claim_value:
            continue
        grouped.setdefault(claim_type, []).append(claim_value)
    return grouped


def _first_claim(claims_by_type: dict[str, list[str]], *claim_types: str) -> str | None:
    for claim_type in claim_types:
        if not claim_type:
            continue
        values = claims_by_type.get(claim_type)
        if values:
            return values[0]
    return None


def _extract_roles(claims_by_type: dict[str, list[str]], role_type: str) -> list[str]:
    role_claim_types = [
        role_type,
        "roles",
        "role",
        "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
    ]
    roles: list[str] = []
    for claim_type in role_claim_types:
        if not claim_type:
            continue
        roles.extend(claims_by_type.get(claim_type, []))
    return list(dict.fromkeys(role for role in roles if role))


def _development_user() -> dict[str, Any]:
    return {
        "id": "local-development-user",
        "email": "local@example.com",
        "name": "Local Development User",
        "roles": [VIEWER_ROLE, ADMIN_ROLE],
        "tenant_id": ENTRA_TENANT_ID or "local",
    }


def current_user(request: Request) -> dict[str, Any]:
    user = getattr(request.state, "user", None)
    if user:
        return user
    if not AUTH_ENABLED:
        return _development_user()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def require_roles(*allowed_roles: str) -> Callable[[Request], dict[str, Any]]:
    def dependency(request: Request) -> dict[str, Any]:
        user = current_user(request)
        user_roles = set(user.get("roles") or [])
        if user_roles.intersection(allowed_roles):
            return user
        logger.warning(
            "User %s lacks required role(s) %s in environment %s",
            user.get("email") or user.get("id"),
            allowed_roles,
            ENVIRONMENT,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient role",
        )

    return dependency
