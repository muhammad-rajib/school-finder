from unittest.mock import patch
from uuid import uuid4

from tests.fixtures.test_data import build_teacher_data


def test_get_teachers_by_school_returns_list(client) -> None:
    school_id = uuid4()
    sample_teachers = [
        build_teacher_data(),
        build_teacher_data(name="Karim Uddin", designation="Head Teacher"),
    ]

    with patch(
        "app.api.v1.endpoints.teacher.get_teachers_by_school",
        return_value=sample_teachers,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/teachers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
