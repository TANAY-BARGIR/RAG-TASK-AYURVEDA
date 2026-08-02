import os
import tempfile
import uuid

# Must happen before anything under app/ is imported: app.core.database and
# app.core.config read these at import time via module-level settings.
_TEST_DB_PATH = os.path.join(tempfile.gettempdir(), f"ayurveda_test_{uuid.uuid4().hex}.db")
_TEST_CHROMA_DIR = os.path.join(tempfile.gettempdir(), f"ayurveda_test_chroma_{uuid.uuid4().hex}")

os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB_PATH}"
os.environ["CHROMA_PERSIST_DIRECTORY"] = _TEST_CHROMA_DIR
os.environ["NVIDIA_API_KEY"] = "test-key"
os.environ["ADMIN_API_KEY"] = "test-admin-secret"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000"
os.environ["SEARCH_RATE_LIMIT"] = "1000/minute"

import pytest
from fastapi.testclient import TestClient

from app.core.database import engine
from app.models.base import Base
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if os.path.exists(_TEST_DB_PATH):
        os.remove(_TEST_DB_PATH)


@pytest.fixture(autouse=True)
def _clean_tables():
    """Each test starts with empty tables (only the ones the suite touches)."""
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_headers():
    return {"X-Api-Key": os.environ["ADMIN_API_KEY"]}
