from unittest.mock import MagicMock
from uuid import uuid4

from app.services.teacher_service import get_teachers_by_school


def test_get_teachers_by_school_orders_by_name() -> None:
    db = MagicMock()
    query = MagicMock()
    school_id = uuid4()
    expected_teachers = [{"name": "Ayesha Rahman"}]
    db.query.return_value = query
    query.filter.return_value = query
    query.order_by.return_value = query
    query.all.return_value = expected_teachers

    result = get_teachers_by_school(db, school_id)

    assert result == expected_teachers
    db.query.assert_called_once()
    query.filter.assert_called_once()
    query.order_by.assert_called_once()
    query.all.assert_called_once_with()
