from unittest.mock import patch
from uuid import uuid4

from app.api.v1.endpoints.notice import get_current_user
from app.main import app
from tests.fixtures.test_data import build_notice_data
from tests.fixtures.test_data import build_user_data


def test_principal_can_create_notice_for_own_school(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    created_notice = build_notice_data()

    with patch(
        "app.api.v1.endpoints.notice.create_notice",
        return_value=created_notice,
    ) as mock_create_notice:
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.post(
                "/api/v1/notices",
                json={
                    "title": "Admission Notice",
                    "description": "Class six admission forms are now available.",
                    "published_date": "2026-03-21",
                },
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["title"] == "Admission Notice"
    mock_create_notice.assert_called_once()
    assert mock_create_notice.call_args.args[1] == school_id


def test_principal_can_update_notice_in_own_school(client) -> None:
    school_id = uuid4()
    notice_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_notice = build_notice_data(id=str(notice_id), school_id=school_id)
    updated_notice = build_notice_data(
        id=str(notice_id),
        school_id=school_id,
        title="Updated Notice",
    )

    with (
        patch("app.api.v1.endpoints.notice.get_notice_by_id", return_value=existing_notice),
        patch("app.api.v1.endpoints.notice.update_notice", return_value=updated_notice),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/notices/{notice_id}",
                json={"title": "Updated Notice"},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Notice"


def test_principal_can_delete_notice_in_own_school(client) -> None:
    school_id = uuid4()
    notice_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_notice = build_notice_data(id=str(notice_id), school_id=school_id)

    with (
        patch("app.api.v1.endpoints.notice.get_notice_by_id", return_value=existing_notice),
        patch("app.api.v1.endpoints.notice.delete_notice", return_value=True),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/notices/{notice_id}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json() == {"message": "Notice deleted successfully"}


def test_get_notices_by_school_returns_list(client) -> None:
    school_id = uuid4()
    admin_user = build_user_data(role="admin")
    sample_notices = [
        build_notice_data(),
        build_notice_data(title="Holiday Notice"),
    ]

    with patch(
        "app.api.v1.endpoints.notice.get_notices_by_school",
        return_value=sample_notices,
    ):
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.get(
                f"/api/v1/schools/{school_id}/notices",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


def test_notice_routes_require_authentication(client) -> None:
    response = client.get(f"/api/v1/schools/{uuid4()}/notices")

    assert response.status_code == 401


def test_principal_cannot_access_other_school_notices(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=uuid4())
    sample_notices = [build_notice_data(school_id=school_id)]

    with patch("app.api.v1.endpoints.notice.get_notices_by_school", return_value=sample_notices):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.get(
                f"/api/v1/schools/{school_id}/notices",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403
