from fastapi import APIRouter
from app.models.api_models import HealthzResponse
from app.services.context_service import context_service

router = APIRouter(prefix="/v1", tags=["Health"])


@router.get("/healthz", response_model=HealthzResponse)
async def healthz():
    """Liveness probe for judging harness."""
    return HealthzResponse(
        status="ok",
        uptime_seconds=context_service.get_uptime_seconds(),
        contexts_loaded=context_service.get_context_counts(),
    )
