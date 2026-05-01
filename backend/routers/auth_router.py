"""Authentication diagnostic routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from core.entra_auth import VIEWER_OR_ADMIN, require_roles

router = APIRouter(prefix="/api", tags=["auth"])


@router.get("/me")
async def get_me(user: dict = Depends(require_roles(*VIEWER_OR_ADMIN))):
    """Return the authenticated user context normalized by the backend."""
    return user
