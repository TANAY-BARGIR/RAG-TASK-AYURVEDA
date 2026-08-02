from typing import Generator
from fastapi import Header, HTTPException, status
from app.core.database import SessionLocal
from app.core.config import get_settings

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def verify_api_key(x_api_key: str = Header(default="")) -> None:
    """Guards write endpoints. An unconfigured ADMIN_API_KEY disables writes
    entirely rather than leaving them open to anyone."""
    settings = get_settings()
    if not settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Write API is disabled: ADMIN_API_KEY is not configured.",
        )
    if x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
