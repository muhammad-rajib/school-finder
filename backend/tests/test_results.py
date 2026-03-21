import sys
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


def build_result(**overrides):
    result = {
        "year": 2025,
        "exam_type": "SSC",
        "pass_rate": 92.5,
    }
    result.update(overrides)
    return result


def test_get_results_by_school_returns_list() -> None:
    school_id = uuid4()
    sample_results = [
        build_result(),
        build_result(year=2024, exam_type="HSC", pass_rate=89.2),
    ]

    with patch(
        "app.api.v1.endpoints.result.get_results_by_school",
        return_value=sample_results,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/results")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
