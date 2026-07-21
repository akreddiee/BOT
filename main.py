import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from app.api import (
    health_router,
    metadata_router,
    context_router,
    tick_router,
    reply_router,
)
from app.config.settings import settings
from app.services.context_service import context_service
from app.utils.logger import get_logger

logger = get_logger("Main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Vera AI Assistant...")
    try:
        context_service.load_seed_data()
    except Exception as e:
        logger.warning(f"Error loading seed dataset: {e}")
    yield
    logger.info("Shutting down Vera AI Assistant...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Vera Merchant AI Assistant - magicpin AI Challenge Submission",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle malformed request bodies with HTTP 400 per testing brief spec."""
    logger.warning(f"Malformed request on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "accepted": False,
            "reason": "invalid_payload",
            "details": str(exc.errors()),
        },
    )


# Include all 5 required endpoint routers
app.include_router(health_router)
app.include_router(metadata_router)
app.include_router(context_router)
app.include_router(tick_router)
app.include_router(reply_router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.PORT))
    logger.info(f"Starting server on {settings.HOST}:{port}")
    uvicorn.run(app, host=settings.HOST, port=port)
