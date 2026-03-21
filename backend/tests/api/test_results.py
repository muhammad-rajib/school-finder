from unittest.mock import patch
from uuid import uuid4

from tests.fixtures.test_data import build_result_data


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
