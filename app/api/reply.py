from fastapi import APIRouter
from app.models.api_models import ReplyRequest, ReplyResponse
from app.services.reply_service import reply_service
from app.utils.logger import get_logger

logger = get_logger("ReplyAPI")

router = APIRouter(prefix="/v1", tags=["Reply"])


@router.post("/reply", response_model=ReplyResponse, response_model_exclude_none=True)
async def reply(body: ReplyRequest):
    """Receive and respond to simulated merchant/customer replies."""
    res = reply_service.handle_reply(
        conversation_id=body.conversation_id,
        merchant_id=body.merchant_id,
        customer_id=body.customer_id,
        from_role=body.from_role,
        message=body.message,
        received_at=body.received_at,
        turn_number=body.turn_number,
    )
    return ReplyResponse(
        action=res["action"],
        body=res.get("body"),
        wait_seconds=res.get("wait_seconds"),
        cta=res.get("cta"),
        rationale=res["rationale"],
    )
