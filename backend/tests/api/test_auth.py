from uuid import uuid4
from unittest.mock import patch

from app.api.v1.endpoints.auth import get_current_user
from app.main import app
from tests.fixtures.test_data import build_user_data


def test_login_returns_access_token_for_valid_credentials(client) -> None:
    user = build_user_data()

    with (
        patch("app.api.v1.endpoints.auth.get_user_by_email", return_value=user),
        patch("app.api.v1.endpoints.auth.verify_password", return_value=True),
        patch("app.api.v1.endpoints.auth.create_access_token", return_value="jwt-token"),
    ):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "secret123"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Login successful",
        "data": {
        "access_token": "jwt-token",
        "token_type": "bearer",
        },
    }


def test_admin_can_create_principal_user(client) -> None:
    admin_user = build_user_data(role="admin")
    created_user = build_user_data(
        name="Principal User",
        email="principal@example.com",
        role="principal",
        school_id=uuid4(),
    )

    with (
        patch("app.api.v1.endpoints.auth.get_user_by_email", return_value=None),
        patch("app.api.v1.endpoints.auth.hash_password", return_value="hashed-password"),
        patch("app.api.v1.endpoints.auth.create_user", return_value=created_user),
    ):
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.post(
                "/api/v1/admin/users",
                json={
                    "name": "Principal User",
                    "email": "principal@example.com",
                    "password": "secret123",
                    "school_id": str(created_user.school_id),
                },
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["message"] == "User created successfully"
    assert response.json()["data"] == {
        "id": str(created_user.id),
        "name": "Principal User",
        "email": "principal@example.com",
        "role": "principal",
        "school_id": str(created_user.school_id),
        "is_active": True,
    }


def test_admin_can_activate_user(client) -> None:
    admin_user = build_user_data(role="admin")
    principal_user = build_user_data(role="principal", school_id=uuid4(), is_active=True)

    with patch("app.api.v1.endpoints.auth.update_user_active_status", return_value=principal_user):
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.put(
                f"/api/v1/admin/users/{principal_user.id}/activate",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["is_active"] is True


def test_admin_can_deactivate_user(client) -> None:
    admin_user = build_user_data(role="admin")
    principal_user = build_user_data(role="principal", school_id=uuid4(), is_active=False)

    with patch("app.api.v1.endpoints.auth.update_user_active_status", return_value=principal_user):
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.put(
                f"/api/v1/admin/users/{principal_user.id}/deactivate",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["is_active"] is False
