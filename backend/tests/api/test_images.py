from unittest.mock import patch
from uuid import uuid4

from app.api.v1.endpoints.school_image import get_current_user
from app.main import app
from tests.fixtures.test_data import build_school_image_data
from tests.fixtures.test_data import build_user_data


def test_principal_can_upload_school_image(client) -> None:
    school_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    created_image = build_school_image_data()

    with (
        patch("app.api.v1.endpoints.school_image.upload_file", return_value=created_image["image_url"]),
        patch("app.api.v1.endpoints.school_image.create_school_image", return_value=created_image),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.post(
                f"/api/v1/schools/{school_id}/images",
                files={"file": ("school.jpg", b"fake-image-data", "image/jpeg")},
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 201
    assert response.json()["image_url"] == created_image["image_url"]
    assert response.json()["is_cover"] is False


def test_principal_cannot_upload_image_for_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    school_id = uuid4()

    app.dependency_overrides[get_current_user] = lambda: principal_user
    try:
        response = client.post(
            f"/api/v1/schools/{school_id}/images",
            files={"file": ("school.jpg", b"fake-image-data", "image/jpeg")},
            headers={"Authorization": "Bearer fake-token"},
        )
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_school_image_upload_requires_authentication(client) -> None:
    school_id = uuid4()

    response = client.post(
        f"/api/v1/schools/{school_id}/images",
        files={"file": ("school.jpg", b"fake-image-data", "image/jpeg")},
    )

    assert response.status_code == 401


def test_principal_can_delete_school_image(client) -> None:
    school_id = uuid4()
    image_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_image = build_school_image_data(id=str(image_id), school_id=school_id)

    with (
        patch("app.api.v1.endpoints.school_image.get_school_image_by_id", return_value=existing_image),
        patch("app.api.v1.endpoints.school_image.delete_school_image", return_value=True),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/images/{image_id}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json() == {"message": "Image deleted"}


def test_principal_cannot_delete_image_from_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    existing_image = build_school_image_data(id=str(uuid4()), school_id=uuid4())

    with patch("app.api.v1.endpoints.school_image.get_school_image_by_id", return_value=existing_image):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.delete(
                f"/api/v1/images/{existing_image['id']}",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_principal_can_set_cover_image(client) -> None:
    school_id = uuid4()
    image_id = uuid4()
    principal_user = build_user_data(role="principal", school_id=school_id)
    existing_image = build_school_image_data(id=str(image_id), school_id=school_id, is_cover=False)
    updated_image = build_school_image_data(id=str(image_id), school_id=school_id, is_cover=True)

    with (
        patch("app.api.v1.endpoints.school_image.get_school_image_by_id", return_value=existing_image),
        patch("app.api.v1.endpoints.school_image.set_cover_image", return_value=updated_image),
    ):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/images/{image_id}/cover",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["is_cover"] is True


def test_principal_cannot_set_cover_image_for_other_school(client) -> None:
    principal_user = build_user_data(role="principal", school_id=uuid4())
    existing_image = build_school_image_data(id=str(uuid4()), school_id=uuid4(), is_cover=False)

    with patch("app.api.v1.endpoints.school_image.get_school_image_by_id", return_value=existing_image):
        app.dependency_overrides[get_current_user] = lambda: principal_user
        try:
            response = client.put(
                f"/api/v1/images/{existing_image['id']}/cover",
                headers={"Authorization": "Bearer fake-token"},
            )
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 403


def test_get_school_images_returns_list(client) -> None:
    school_id = uuid4()
    sample_images = [
        build_school_image_data(),
        build_school_image_data(image_url="https://cdn.example.com/schools/gallery.jpg"),
    ]

    with patch(
        "app.api.v1.endpoints.school_image.get_school_images",
        return_value=sample_images,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/images")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
