from fastapi import APIRouter
from app.models import PingResponse
from app.services.ping_service import get_ping_message
from app.logging_config import logger

router = APIRouter()

@router.get("/ping", response_model=PingResponse, summary="Ping the server", tags=["Health"])
def ping():
    logger.info("Ping endpoint called")
    message = get_ping_message()
    logger.debug(f"Ping response: {message}")
    return PingResponse(message=message)