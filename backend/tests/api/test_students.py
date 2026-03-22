from unittest.mock import patch
from uuid import uuid4

from app.api.v1.endpoints.student import get_current_user
from app.main import app
from tests.fixtures.test_data import build_school_data
from tests.fixtures.test_data import build_user_data


def test_get_student_stats_returns_aggregated_data(client) -> None:
    school_id = uuid4()
    admin_user = build_user_data(role="admin")
    sample_school = build_school_data(
        id=str(school_id),
        total_students=750,
        boys=390,
        girls=360,
    )

    with patch("app.api.v1.endpoints.student.get_student_stats", return_value=sample_school):
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.get(
                f"/api/v1/schools/{school_id}/students",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {
            "total": 750,
            "boys": 390,
            "girls": 360,
        },
        "message": "Student stats retrieved successfully",
    }


def test_update_student_stats_returns_updated_data(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    updated_school = build_school_data(
        id=str(school_id),
        total_students=800,
        boys=410,
        girls=390,
    )

    with patch("app.api.v1.endpoints.student.update_student_stats", return_value=updated_school):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/schools/{school_id}/students",
                json={"total": 800, "boys": 410, "girls": 390},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {
            "total": 800,
            "boys": 410,
            "girls": 390,
        },
        "message": "Student stats updated successfully",
    }


def test_student_stats_requires_authentication(client) -> None:
    school_id = uuid4()

    response = client.get(f"/api/v1/schools/{school_id}/students")

    assert response.status_code == 401
    assert response.json()["success"] is False


def test_principal_cannot_access_other_school_student_stats(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=uuid4())
    sample_school = build_school_data(id=str(school_id))

    with patch("app.api.v1.endpoints.student.get_student_stats", return_value=sample_school):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.get(
                f"/api/v1/schools/{school_id}/students",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403
    assert response.json()["success"] is False
