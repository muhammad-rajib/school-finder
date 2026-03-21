from unittest.mock import ANY, patch
from uuid import uuid4

from tests.fixtures.test_data import build_school_data


def test_get_schools_returns_paginated_response(client) -> None:
    sample_schools = [build_school_data()]

    with patch("app.api.v1.endpoints.school.search_schools", return_value=sample_schools):
        response = client.get("/api/v1/schools")

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert response.json()["data"][0]["country_code"] == "BD"
    assert response.json()["data"][0]["description"] == "A leading secondary school in central Dhaka."
    assert response.json()["page"] == 1
    assert response.json()["limit"] == 10


def test_get_school_by_id_returns_school_when_found(client) -> None:
    school_id = uuid4()
    sample_school = build_school_data(
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
    assert response.json()["description"] == "A leading secondary school in central Dhaka."
    assert response.json()["phone"] == "+8801712345678"
    assert response.json()["email"] == "info@sample-school.edu"
    assert response.json()["website"] == "https://sample-school.edu"
    assert response.json()["established_year"] == 1998
    assert response.json()["total_classrooms"] == 18
    assert response.json()["has_electricity"] is True
    assert response.json()["has_water"] is True


def test_get_school_by_id_returns_404_when_not_found(client) -> None:
    school_id = uuid4()

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=None):
        response = client.get(f"/api/v1/schools/{school_id}")

    assert response.status_code == 404


def test_search_schools_by_name(client) -> None:
    sample_school = build_school_data(
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


def test_search_schools_by_emis_code_returns_exact_match(client) -> None:
    sample_school = build_school_data(emis_code="123456", name="Exact Match School")

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


def test_search_schools_by_location_filters(client) -> None:
    sample_school = build_school_data(
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


def test_search_schools_with_combined_filters(client) -> None:
    sample_school = build_school_data(name="Kaliganj Govt School", district="Gazipur")

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


def test_search_schools_with_pagination(client) -> None:
    sample_schools = [build_school_data(name=f"School {index}") for index in range(1, 6)]

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


def test_search_schools_returns_no_result_for_unknown_query(client) -> None:
    with patch("app.api.v1.endpoints.school.search_schools", return_value=[]):
        response = client.get("/api/v1/schools?name=unknown-school")

    assert response.status_code == 200
    assert response.json()["data"] == []
