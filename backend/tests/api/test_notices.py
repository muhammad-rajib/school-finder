from unittest.mock import patch
from uuid import uuid4

from tests.fixtures.test_data import build_notice_data


def test_get_notices_by_school_returns_list(client) -> None:
    school_id = uuid4()
    sample_notices = [
        build_notice_data(),
        build_notice_data(title="Holiday Notice"),
    ]

    with patch(
        "app.api.v1.endpoints.notice.get_notices_by_school",
        return_value=sample_notices,
    ):
        response = client.get(f"/api/v1/schools/{school_id}/notices")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
