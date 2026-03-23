from unittest.mock import MagicMock
from uuid import uuid4

from app.services.school_service import get_school_by_id, search_schools


def test_search_schools_applies_filters_and_pagination() -> None:
    db = MagicMock()
    query = MagicMock()
    db.query.return_value = query
    query.filter.return_value = query
    query.order_by.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query
    query.all.return_value = ["school-1"]

    result = search_schools(
        db=db,
        name="sample",
        division="Dhaka",
        district="Dhaka",
        upazila="Dhanmondi",
        union="Ward 1",
        emis_code="123456",
        skip=5,
        limit=10,
    )

    assert result == ["school-1"]
    db.query.assert_called_once()
    assert query.filter.call_count == 6
    query.order_by.assert_called_once()
    query.offset.assert_called_once_with(5)
    query.limit.assert_called_once_with(10)


def test_search_schools_ignores_empty_filter_values() -> None:
    db = MagicMock()
    query = MagicMock()
    db.query.return_value = query
    query.filter.return_value = query
    query.order_by.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query
    query.all.return_value = []

    result = search_schools(
        db=db,
        name="   ",
        division=" ",
        district=None,
        upazila="",
        union="   ",
        emis_code=None,
        skip=0,
        limit=10,
    )

    assert result == []
    query.filter.assert_not_called()
    query.order_by.assert_called_once()
    query.offset.assert_called_once_with(0)
    query.limit.assert_called_once_with(10)


def test_get_school_by_id_returns_first_match() -> None:
    db = MagicMock()
    query = MagicMock()
    school_id = uuid4()
    expected_school = {"id": str(school_id)}
    db.query.return_value = query
    query.filter.return_value = query
    query.first.return_value = expected_school

    result = get_school_by_id(db, school_id)

    assert result == expected_school
    db.query.assert_called_once()
    query.filter.assert_called_once()
    query.first.assert_called_once_with()
