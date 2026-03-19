import sys
from datetime import datetime, timezone
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


def test_get_schools_returns_list() -> None:
    sample_schools = [
        {
            "id": str(uuid4()),
            "emis_code": "123456",
            "name": "Sample School",
            "division": "Dhaka",
            "district": "Dhaka",
            "upazila": "Dhanmondi",
            "address": "Road 1, Dhaka",
            "total_students": 500,
            "total_teachers": 25,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]

    with patch("app.api.v1.endpoints.school.get_schools", return_value=sample_schools):
        response = client.get("/api/v1/schools")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_school_by_id_returns_school_when_found() -> None:
    school_id = uuid4()
    sample_school = {
        "id": str(school_id),
        "emis_code": "654321",
        "name": "Single School",
        "division": "Dhaka",
        "district": "Gazipur",
        "upazila": "Sreepur",
        "address": "Main Road, Gazipur",
        "total_students": 750,
        "total_teachers": 30,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=sample_school):
        response = client.get(f"/api/v1/schools/{school_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(school_id)


def test_get_school_by_id_returns_404_when_not_found() -> None:
    school_id = uuid4()

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=None):
        response = client.get(f"/api/v1/schools/{school_id}")

    assert response.status_code == 404
