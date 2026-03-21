import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.v1.endpoints.school import get_db
from app.main import app


def override_get_db():
    yield object()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def build_notice(**overrides):
    notice = {
        "title": "Admission Notice",
        "description": "Class six admission forms are now available.",
        "published_date": date(2026, 3, 21).isoformat(),
    }
    notice.update(overrides)
    return notice


def test_get_notices_by_school_returns_list() -> None:
    school_id = uuid4()
    sample_notices = [
        build_notice(),
        build_notice(title="Holiday Notice"),
    ]

    with patch(
        "app.api.v1.endpoints.notice.get_notices_by_school",
        return_value=sample_notices,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/notices")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
