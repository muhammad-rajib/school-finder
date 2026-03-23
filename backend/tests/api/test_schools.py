from unittest.mock import ANY, patch
from uuid import uuid4

from tests.fixtures.test_data import build_school_data


def test_get_schools_returns_results_when_no_filter_is_provided(client) -> None:
    sample_schools = [build_school_data()]

    with patch("app.api.v1.endpoints.school.search_schools", return_value=sample_schools):
        response = client.get("/api/v1/schools")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert isinstance(response.json()["data"], list)
    assert response.json()["data"][0]["country_code"] == "BD"
    assert response.json()["data"][0]["description"] == "A leading secondary school in central Dhaka."
    assert response.json()["total"] == 1


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
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == str(school_id)
    assert response.json()["data"]["description"] == "A leading secondary school in central Dhaka."
    assert response.json()["data"]["phone"] == "+8801712345678"
    assert response.json()["data"]["email"] == "info@sample-school.edu"
    assert response.json()["data"]["website"] == "https://sample-school.edu"
    assert response.json()["data"]["established_year"] == 1998
    assert response.json()["data"]["total_classrooms"] == 18
    assert response.json()["data"]["has_electricity"] is True
    assert response.json()["data"]["has_water"] is True


def test_get_school_by_id_returns_404_when_not_found(client) -> None:
    school_id = uuid4()

    with patch("app.api.v1.endpoints.school.get_school_by_id", return_value=None):
        response = client.get(f"/api/v1/schools/{school_id}")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "data": None,
        "message": "School not found",
    }


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


def test_search_schools_with_only_division_filter(client) -> None:
    sample_school = build_school_data(
        name="Location Match School",
        division="Dhaka",
    )

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get("/api/v1/schools?division=Dhaka")

    assert response.status_code == 200
    assert response.json()["data"][0]["division"] == "Dhaka"
    mock_search.assert_called_once_with(
        db=ANY,
        name=None,
        division="Dhaka",
        district=None,
        upazila=None,
        union=None,
        emis_code=None,
        skip=0,
        limit=10,
    )


def test_search_schools_with_division_and_district_filters(client) -> None:
    sample_school = build_school_data(name="Kaliganj Govt School", division="Dhaka", district="Gazipur")

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get("/api/v1/schools?division=Dhaka&district=Gazipur")

    assert response.status_code == 200
    assert response.json()["data"][0]["division"] == "Dhaka"
    assert response.json()["data"][0]["district"] == "Gazipur"
    mock_search.assert_called_once_with(
        db=ANY,
        name=None,
        division="Dhaka",
        district="Gazipur",
        upazila=None,
        union=None,
        emis_code=None,
        skip=0,
        limit=10,
    )


def test_search_schools_with_full_filter(client) -> None:
    sample_school = build_school_data(
        name="Kaliganj Govt School",
        division="Dhaka",
        district="Gazipur",
        upazila="Kaliganj",
        union="Tumlia",
    )

    with patch("app.api.v1.endpoints.school.search_schools", return_value=[sample_school]) as mock_search:
        response = client.get(
            "/api/v1/schools?division=Dhaka&district=Gazipur&upazila=Kaliganj&union=Tumlia&name=kaliganj"
        )

    assert response.status_code == 200
    assert response.json()["data"][0]["name"] == "Kaliganj Govt School"
    assert response.json()["data"][0]["union"] == "Tumlia"
    assert response.json()["total"] == 1
    mock_search.assert_called_once_with(
        db=ANY,
        name="kaliganj",
        division="Dhaka",
        district="Gazipur",
        upazila="Kaliganj",
        union="Tumlia",
        emis_code=None,
        skip=0,
        limit=10,
    )


def test_search_schools_returns_no_result_for_unknown_query(client) -> None:
    with patch("app.api.v1.endpoints.school.search_schools", return_value=[]):
        response = client.get("/api/v1/schools?name=unknown-school")

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["total"] == 0
