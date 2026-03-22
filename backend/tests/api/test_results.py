from unittest.mock import patch
from uuid import uuid4

from app.api.v1.endpoints.result import get_current_user
from app.main import app
from tests.fixtures.test_data import build_result_data
from tests.fixtures.test_data import build_user_data


def test_principal_can_create_result_for_own_school(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    created_result = build_result_data()

    with patch(
        "app.api.v1.endpoints.result.create_result",
        return_value=created_result,
    ) as mock_create_result:
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.post(
                "/api/v1/results",
                json={
                    "year": 2025,
                    "exam_type": "SSC",
                    "pass_rate": 92.5,
                },
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["exam_type"] == "SSC"
    mock_create_result.assert_called_once()
    assert mock_create_result.call_args.args[1] == school_id


def test_admin_can_create_result_for_given_school(client) -> None:
    school_id = uuid4()
    admin_user = build_user_data(role="admin")
    created_result = build_result_data()

    with patch(
        "app.api.v1.endpoints.result.create_result",
        return_value=created_result,
    ) as mock_create_result:
        app.dependency_overrides[get_current_user] = lambda: admin_user
        try:
            response = client.post(
                "/api/v1/results",
                json={
                    "school_id": str(school_id),
                    "year": 2025,
                    "exam_type": "SSC",
                    "pass_rate": 92.5,
                },
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["pass_rate"] == 92.5
    mock_create_result.assert_called_once()
    assert mock_create_result.call_args.args[1] == school_id


def test_create_result_requires_authentication(client) -> None:
    response = client.post(
        "/api/v1/results",
        json={
            "year": 2025,
            "exam_type": "SSC",
            "pass_rate": 92.5,
        },
    )

    assert response.status_code == 401


def test_principal_can_update_result_in_own_school(client) -> None:
    school_id = uuid4()
    result_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_result = build_result_data(id=str(result_id), school_id=school_id)
    updated_result = build_result_data(
        id=str(result_id),
        school_id=school_id,
        pass_rate=95.0,
    )

    with (
        patch("app.api.v1.endpoints.result.get_result_by_id", return_value=existing_result),
        patch("app.api.v1.endpoints.result.update_result", return_value=updated_result),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/results/{result_id}",
                json={"pass_rate": 95.0},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["pass_rate"] == 95.0


def test_principal_cannot_update_result_from_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    existing_result = build_result_data(id=str(uuid4()), school_id=uuid4())

    with patch("app.api.v1.endpoints.result.get_result_by_id", return_value=existing_result):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/results/{existing_result['id']}",
                json={"pass_rate": 95.0},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_principal_can_delete_result_in_own_school(client) -> None:
    school_id = uuid4()
    result_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_result = build_result_data(id=str(result_id), school_id=school_id)

    with (
        patch("app.api.v1.endpoints.result.get_result_by_id", return_value=existing_result),
        patch("app.api.v1.endpoints.result.delete_result", return_value=True),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/results/{result_id}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json() == {"message": "Result deleted successfully"}


def test_principal_cannot_delete_result_from_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    existing_result = build_result_data(id=str(uuid4()), school_id=uuid4())

    with patch("app.api.v1.endpoints.result.get_result_by_id", return_value=existing_result):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/results/{existing_result['id']}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_get_results_by_school_returns_list(client) -> None:
    school_id = uuid4()
    sample_results = [
        build_result_data(),
        build_result_data(year=2024, exam_type="HSC", pass_rate=89.2),
    ]

    with patch(
        "app.api.v1.endpoints.result.get_results_by_school",
        return_value=sample_results,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/results")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
