from unittest.mock import patch
from uuid import uuid4

from tests.fixtures.test_data import build_school_data


def test_get_student_stats_returns_aggregated_data(client) -> None:
    school_id = uuid4()
    sample_school = build_school_data(
        id=str(school_id),
        total_students=750,
        boys=390,
        girls=360,
    )

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=sample_school):
        response = client.get(f"/api/v1/schools/{school_id}/students")

    assert response.status_code == 200
    assert response.json() == {
        "total": 750,
        "boys": 390,
        "girls": 360,
    }
