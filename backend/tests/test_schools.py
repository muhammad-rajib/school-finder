import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import ANY, patch
from uuid import uuid4

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.v1.endpoints.school import get_db
from app.main import app


def override_get_db():
    yield object()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def build_school(**overrides):
    school = {
        "id": str(uuid4()),
        "emis_code": "123456",
        "name": "Sample School",
        "country_code": "BD",
        "division": "Dhaka",
        "district": "Dhaka",
        "upazila": "Dhanmondi",
        "union": "Ward 1",
        "address": "Road 1, Dhaka",
        "total_students": 500,
        "total_teachers": 25,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    school.update(overrides)
    return school


def test_get_schools_returns_paginated_response() -> None:
    sample_schools = [build_school()]

    with patch("app.api.v1.endpoints.school.search_schools", return_value=sample_schools):
        response = client.get("/api/v1/schools")

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert response.json()["data"][0]["country_code"] == "BD"
    assert response.json()["page"] == 1
    assert response.json()["limit"] == 10


def test_get_school_by_id_returns_school_when_found() -> None:
    school_id = uuid4()
    sample_school = build_school(
        id=str(school_id),
        emis_code="654321",
        name="Single School",
        district="Gazipur",
        upazila="Sreepur",
        address="Main Road, Gazipur",
        total_students=750,
        total_teachers=30,
    )

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=sample_school):
        response = client.get(f"/api/v1/schools/{school_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(school_id)


def test_get_school_by_id_returns_404_when_not_found() -> None:
    school_id = uuid4()

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=None):
        response = client.get(f"/api/v1/schools/{school_id}")

    assert response.status_code == 404


def test_search_schools_by_name() -> None:
    sample_school = build_school(
        emis_code="777777",
        name="Kaliganj Govt School",
        district="Gazipur",
        upazila="Kaliganj",
        address="Kaliganj Bazar, Gazipur",
        total_students=980,
        total_teachers=34,
    )

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get("/api/v1/schools?name=kaliganj")

    assert response.status_code == 200
    assert any(school["name"] == "Kaliganj Govt School" for school in response.json()["data"])
    mock_search.assert_called_once_with(
        db=ANY,
        name="kaliganj",
        division=None,
        district=None,
        upazila=None,
        union=None,
        emis_code=None,
        skip=0,
        limit=10,
    )


def test_search_schools_by_emis_code_returns_exact_match() -> None:
    sample_school = build_school(emis_code="123456", name="Exact Match School")

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get("/api/v1/schools?emis_code=123456")

    assert response.status_code == 200
    assert response.json()["data"][0]["emis_code"] == "123456"
    mock_search.assert_called_once_with(
        db=ANY,
        name=None,
        division=None,
        district=None,
        upazila=None,
        union=None,
        emis_code="123456",
        skip=0,
        limit=1,
    )


def test_search_schools_by_location_filters() -> None:
    sample_school = build_school(
        name="Location Match School",
        division="Dhaka",
        district="Gazipur",
        upazila="Kaliganj",
    )

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get(
            "/api/v1/schools?division=Dhaka&district=Gazipur&upazila=Kaliganj"
        )

    assert response.status_code == 200
    assert response.json()["data"][0]["district"] == "Gazipur"
    assert response.json()["data"][0]["upazila"] == "Kaliganj"
    mock_search.assert_called_once_with(
        db=ANY,
        name=None,
        division="Dhaka",
        district="Gazipur",
        upazila="Kaliganj",
        union=None,
        emis_code=None,
        skip=0,
        limit=10,
    )


def test_search_schools_with_combined_filters() -> None:
    sample_school = build_school(name="Kaliganj Govt School", district="Gazipur")

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get("/api/v1/schools?name=kaliganj&district=Gazipur")

    assert response.status_code == 200
    assert response.json()["data"][0]["name"] == "Kaliganj Govt School"
    assert response.json()["data"][0]["district"] == "Gazipur"
    mock_search.assert_called_once_with(
        db=ANY,
        name="kaliganj",
        division=None,
        district="Gazipur",
        upazila=None,
        union=None,
        emis_code=None,
        skip=0,
        limit=10,
    )


def test_search_schools_with_pagination() -> None:
    sample_schools = [build_school(name=f"School {index}") for index in range(1, 6)]

    with patch("app.api.v1.endpoints.school.search_schools", return_value=sample_schools) as mock_search:
        response = client.get("/api/v1/schools?page=1&limit=5")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 5
    assert response.json()["page"] == 1
    assert response.json()["limit"] == 5
    mock_search.assert_called_once_with(
        db=ANY,
        name=None,
        division=None,
        district=None,
        upazila=None,
        union=None,
        emis_code=None,
        skip=0,
        limit=5,
    )


def test_search_schools_returns_no_result_for_unknown_query() -> None:
    with patch("app.api.v1.endpoints.school.search_schools", return_value=[]):
        response = client.get("/api/v1/schools?name=unknown-school")

    assert response.status_code == 200
    assert response.json()["data"] == []
