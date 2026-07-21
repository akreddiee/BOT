from fastapi import APIRouter
from app.models.api_models import ActionModel, TickRequest, TickResponse
from app.services.composer_service import composer_service
from app.services.context_service import context_service
from app.utils.logger import get_logger

logger = get_logger("TickAPI")

router = APIRouter(prefix="/v1", tags=["Tick"])


@router.post("/tick", response_model=TickResponse)
async def tick(body: TickRequest):
    """Periodic tick wake-up for proactive message initiation."""
    actions = []
    triggers_seen = set()

    for trig_id in body.available_triggers:
        if trig_id in triggers_seen:
            continue
        triggers_seen.add(trig_id)

        trig = context_service.get_context("trigger", trig_id)
        if not trig:
            logger.warning(f"Trigger {trig_id} not found in storage")
            continue

        merchant_id = trig.get("merchant_id")
        if not merchant_id:
            payload = trig.get("payload", {})
            merchant_id = payload.get("merchant_id")

        if not merchant_id:
            continue

        merchant = context_service.get_context("merchant", merchant_id)
        if not merchant:
            logger.warning(f"Merchant {merchant_id} not found for trigger {trig_id}")
            continue

        cat_slug = merchant.get("category_slug", "generic")
        category = context_service.get_context("category", cat_slug) or {"slug": cat_slug}

        customer_id = trig.get("customer_id")
        customer = context_service.get_context("customer", customer_id) if customer_id else None

        # Compose message
        composed = composer_service.compose(category, merchant, trig, customer)

        conv_id = f"conv_{merchant_id}_{trig_id}"

        action = ActionModel(
            conversation_id=conv_id,
            merchant_id=merchant_id,
            customer_id=customer_id,
            send_as=composed["send_as"],
            trigger_id=trig_id,
            template_name=composed["template_name"],
            template_params=composed["template_params"],
            body=composed["body"],
            cta=composed["cta"],
            suppression_key=composed["suppression_key"],
            rationale=composed["rationale"],
        )
        actions.append(action)

    return TickResponse(actions=actions)
