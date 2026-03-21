import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.v1.endpoints.school import get_db
from app.main import app


@pytest.fixture
def db_session() -> Generator[object, None, None]:
    # TODO: Replace with a real test database session when integration tests are added.
    yield object()


@pytest.fixture
def client(db_session: object) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[object, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
