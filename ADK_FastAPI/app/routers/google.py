from fastapi import APIRouter, HTTPException, Depends
from app.config import settings
from app.models import User
from app.logging_config import logger

router = APIRouter()

# Import the dependency from auth router
from app.routers.auth import get_current_active_user

@router.get("/google/status", summary="Check Google API key status", tags=["Google"])
def google_status(current_user: User = Depends(get_current_active_user)):
    logger.info(f"Google status check requested by user: {current_user.username}")
    if settings.google_api_key:
        logger.debug("Google API key is configured")
        return {"api_key_loaded": True, "message": "Google API key is loaded"}
    else:
        logger.warning("Google API key not configured")
        raise HTTPException(status_code=400, detail="Google API key not loaded")