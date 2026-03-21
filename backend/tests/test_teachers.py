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


def build_teacher(**overrides):
    teacher = {
        "id": str(uuid4()),
        "name": "Ayesha Rahman",
        "designation": "Assistant Teacher",
        "subject": "Mathematics",
        "qualification": "M.Sc. in Mathematics",
    }
    teacher.update(overrides)
    return teacher


def test_get_teachers_by_school_returns_list() -> None:
    school_id = uuid4()
    sample_teachers = [
        build_teacher(),
        build_teacher(name="Karim Uddin", designation="Head Teacher"),
    ]

    with patch(
        "app.api.v1.endpoints.teacher.get_teachers_by_school",
        return_value=sample_teachers,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/teachers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
