from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Professional FastAPI Service"
    debug: bool = False
    version: str = "1.0.0"
    google_api_key: Optional[str] = None
    google_cloud_project: Optional[str] = None
    google_cloud_location: str = "global"
    model: str = "gemini-2.5-flash"
    dataset_id: str = "products_data_agent"
    table_id: str = "shoe_items"
    disable_web_driver: int = 0
    # Authentication settings
    secret_key: str = "your-secret-key-here"  # Change this in production
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # Add more config options as needed

    class Config:
        env_file = ".env"

settings = Settings()
