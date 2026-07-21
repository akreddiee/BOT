"""
bot.py — Entrypoint satisfying Section 7.1 of magicpin AI Challenge Brief.
"""

from typing import Dict, Any, Optional
from main import app
from app.services.composer_service import composer_service


def compose(
    category: Dict[str, Any],
    merchant: Dict[str, Any],
    trigger: Dict[str, Any],
    customer: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Compose a Vera message given the 4 contexts.
    Inputs are dicts loaded from dataset JSON.
    Returns dict with keys: body, cta, send_as, suppression_key, rationale.
    """
    return composer_service.compose(category, merchant, trigger, customer)


if __name__ == "__main__":
    import os
    import uvicorn
    from app.config.settings import settings

    port = int(os.environ.get("PORT", settings.PORT))
    uvicorn.run(app, host=settings.HOST, port=port)
