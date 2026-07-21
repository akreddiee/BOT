from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Response, status
from app.models.api_models import ContextPushRequest, ContextPushResponse, ContextErrorResponse
from app.services.context_service import context_service
from app.utils.logger import get_logger

logger = get_logger("ContextAPI")

router = APIRouter(prefix="/v1", tags=["Context"])


@router.post(
    "/context",
    responses={
        200: {"model": ContextPushResponse},
        400: {"model": ContextErrorResponse},
        409: {"model": ContextErrorResponse},
    },
)
async def push_context(body: ContextPushRequest, response: Response):
    """Receive incremental context updates."""
    accepted, current_ver, reason = context_service.push_context(
        scope=body.scope,
        context_id=body.context_id,
        version=body.version,
        payload=body.payload,
    )

    if not accepted:
        if reason == "stale_version":
            response.status_code = status.HTTP_409_CONFLICT
            return ContextErrorResponse(
                accepted=False,
                reason="stale_version",
                current_version=current_ver,
            )
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ContextErrorResponse(
            accepted=False,
            reason="invalid_scope",
            details=reason,
        )

    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return ContextPushResponse(
        accepted=True,
        ack_id=f"ack_{body.context_id}_v{body.version}",
        stored_at=now_iso,
    )
