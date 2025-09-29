from app.config import settings
from app.logging_config import logger

def get_ping_message():
    logger.debug("Generating ping message")
    message = f"pong from {settings.app_name}"
    return message