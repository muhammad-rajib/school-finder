from unittest.mock import patch
from uuid import uuid4

from tests.fixtures.test_data import build_school_image_data


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


def test_get_cover_image_returns_single_object(client) -> None:
    school_id = uuid4()
    cover_image = build_school_image_data(is_cover=True)

    with patch(
        "app.api.v1.endpoints.school_image.get_cover_image",
        return_value=cover_image,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/images/cover")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["is_cover"] is True


def test_get_school_images_returns_empty_list_when_no_images(client) -> None:
    school_id = uuid4()

    with patch("app.api.v1.endpoints.school_image.get_school_images", return_value=[]):
        response = client.get(f"/api/v1/schools/{school_id}/images")

    assert response.status_code == 200
    assert response.json() == []
