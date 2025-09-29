from fastapi import FastAPI, Request
from app.routers.ping import router as ping_router
from app.routers.google import router as google_router
from app.routers.auth import router as auth_router
from app.config import settings
from app.database import engine
from app.db_models import Base
from app.logging_config import setup_logging, logger
import time

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
	title=settings.app_name,
	description="A scalable FastAPI example.",
	version=settings.version,
	debug=settings.debug
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url} from {request.client.host}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} in {process_time:.4f}s")
    
    return response

app.include_router(ping_router)
app.include_router(google_router)
app.include_router(auth_router, prefix="/auth")

logger.info("FastAPI application started")

# To run: uvicorn app.main:app --reload