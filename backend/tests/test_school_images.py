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


def build_school_image(**overrides):
    image = {
        "id": str(uuid4()),
        "image_url": "https://cdn.example.com/schools/cover.jpg",
        "is_cover": False,
    }
    image.update(overrides)
    return image


def test_get_school_images_returns_list() -> None:
    school_id = uuid4()
    sample_images = [
        build_school_image(),
        build_school_image(image_url="https://cdn.example.com/schools/gallery.jpg"),
    ]

    with patch(
        "app.api.v1.endpoints.school_image.get_school_images",
        return_value=sample_images,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/images")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


def test_get_cover_image_returns_single_object() -> None:
    school_id = uuid4()
    cover_image = build_school_image(is_cover=True)

    with patch(
        "app.api.v1.endpoints.school_image.get_cover_image",
        return_value=cover_image,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/images/cover")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["is_cover"] is True


def test_get_school_images_returns_empty_list_when_no_images() -> None:
    school_id = uuid4()

    with patch("app.api.v1.endpoints.school_image.get_school_images", return_value=[]):
        response = client.get(f"/api/v1/schools/{school_id}/images")

    assert response.status_code == 200
    assert response.json() == []
