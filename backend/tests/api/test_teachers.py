from unittest.mock import patch
from uuid import uuid4

from app.api.v1.endpoints.teacher import get_current_user
from app.main import app
from tests.fixtures.test_data import build_teacher_data
from tests.fixtures.test_data import build_user_data


def test_principal_can_create_teacher_for_own_school(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    created_teacher = build_teacher_data()

    with patch(
        "app.api.v1.endpoints.teacher.create_teacher",
        return_value=created_teacher,
    ) as mock_create_teacher:
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.post(
                "/api/v1/teachers",
                json={
                    "name": "Ayesha Rahman",
                    "designation": "Assistant Teacher",
                    "subject": "Mathematics",
                },
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["name"] == "Sample Teacher"
    mock_create_teacher.assert_called_once()
    assert mock_create_teacher.call_args.args[1] == school_id


def test_admin_can_create_teacher_for_given_school(client) -> None:
    school_id = uuid4()
    admin_user = build_user_data(role="admin")
    created_teacher = build_teacher_data()

    with patch(
        "app.api.v1.endpoints.teacher.create_teacher",
        return_value=created_teacher,
    ) as mock_create_teacher:
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.post(
                "/api/v1/teachers",
                json={
                    "name": "Ayesha Rahman",
                    "designation": "Assistant Teacher",
                    "school_id": str(school_id),
                },
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["designation"] == "Assistant Teacher"
    mock_create_teacher.assert_called_once()
    assert mock_create_teacher.call_args.args[1] == school_id


def test_create_teacher_requires_authentication(client) -> None:
    response = client.post(
        "/api/v1/teachers",
        json={
            "name": "Ayesha Rahman",
            "designation": "Assistant Teacher",
        },
    )

    assert response.status_code == 401


def test_principal_can_update_teacher_in_own_school(client) -> None:
    school_id = uuid4()
    teacher_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_teacher = build_teacher_data(id=str(teacher_id), school_id=school_id)
    updated_teacher = build_teacher_data(
        id=str(teacher_id),
        school_id=school_id,
        name="Updated Teacher",
    )

    with (
        patch("app.api.v1.endpoints.teacher.get_teacher_by_id", return_value=existing_teacher),
        patch("app.api.v1.endpoints.teacher.update_teacher", return_value=updated_teacher),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/teachers/{teacher_id}",
                json={"name": "Updated Teacher"},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Teacher"


def test_principal_cannot_update_teacher_from_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    existing_teacher = build_teacher_data(id=str(uuid4()), school_id=uuid4())

    with patch("app.api.v1.endpoints.teacher.get_teacher_by_id", return_value=existing_teacher):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/teachers/{existing_teacher['id']}",
                json={"name": "Updated Teacher"},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_principal_can_delete_teacher_in_own_school(client) -> None:
    school_id = uuid4()
    teacher_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_teacher = build_teacher_data(id=str(teacher_id), school_id=school_id)

    with (
        patch("app.api.v1.endpoints.teacher.get_teacher_by_id", return_value=existing_teacher),
        patch("app.api.v1.endpoints.teacher.delete_teacher", return_value=True),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/teachers/{teacher_id}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json() == {"message": "Teacher deleted successfully"}


def test_principal_cannot_delete_teacher_from_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    existing_teacher = build_teacher_data(id=str(uuid4()), school_id=uuid4())

    with patch("app.api.v1.endpoints.teacher.get_teacher_by_id", return_value=existing_teacher):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/teachers/{existing_teacher['id']}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


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
