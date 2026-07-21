from fastapi import APIRouter
from app.models.api_models import MetadataResponse
from app.config.settings import settings

router = APIRouter(prefix="/v1", tags=["Metadata"])


@router.get("/metadata", response_model=MetadataResponse)
async def metadata():
    """Bot identity and information endpoint."""
    return MetadataResponse(
        team_name="Senior Staff Vera AI",
        team_members=["Vera AI Engineering"],
        model="4-context-deterministic-modular-composer",
        approach="Deterministic 4-context modular engine with intent transition & auto-reply detection",
        contact_email="vera-ai@magicpin.in",
        version=settings.VERSION,
        submitted_at="2026-04-26T08:00:00Z",
    )
