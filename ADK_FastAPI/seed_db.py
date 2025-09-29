from app.database import SessionLocal
from app.db_models import User
from passlib.context import CryptContext
from app.logging_config import logger

pwd_context = CryptContext(schemes=["sha256_crypt"])

def create_test_user():
    logger.info("Checking for existing test user...")
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.username == "testuser").first()
        if user:
            logger.info("Test user already exists")
            return

        # Create test user
        hashed_password = pwd_context.hash("password")
        test_user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=hashed_password,
            disabled=False
        )
        db.add(test_user)
        db.commit()
        logger.info("Test user created successfully")
    except Exception as e:
        logger.error(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()