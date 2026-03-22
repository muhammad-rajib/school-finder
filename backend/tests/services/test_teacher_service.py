from unittest.mock import MagicMock
from uuid import uuid4

from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.services.teacher_service import (
    create_teacher,
    delete_teacher,
    get_teacher_by_id,
    get_teachers_by_school,
    update_teacher,
)


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


def test_get_teacher_by_id_returns_first_match() -> None:
    db = MagicMock()
    query = MagicMock()
    teacher_id = uuid4()
    expected_teacher = {"id": str(teacher_id)}
    db.query.return_value = query
    query.filter.return_value = query
    query.first.return_value = expected_teacher

    result = get_teacher_by_id(db, teacher_id)

    assert result == expected_teacher
    db.query.assert_called_once()
    query.filter.assert_called_once()
    query.first.assert_called_once_with()


def test_create_teacher_saves_and_returns_teacher() -> None:
    db = MagicMock()
    school_id = uuid4()
    data = TeacherCreate(
        name="Ayesha Rahman",
        designation="Assistant Teacher",
        subject="Mathematics",
    )

    teacher = create_teacher(db, school_id, data)

    assert teacher.school_id == school_id
    assert teacher.name == "Ayesha Rahman"
    assert teacher.designation == "Assistant Teacher"
    db.add.assert_called_once_with(teacher)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(teacher)


def test_update_teacher_updates_existing_teacher() -> None:
    db = MagicMock()
    teacher_id = uuid4()
    existing_teacher = MagicMock()
    existing_teacher.name = "Old Name"
    existing_teacher.designation = "Assistant Teacher"
    db.query.return_value.filter.return_value.first.return_value = existing_teacher
    data = TeacherUpdate(name="New Name", phone="+8801712345678")

    result = update_teacher(db, teacher_id, data)

    assert result is existing_teacher
    assert existing_teacher.name == "New Name"
    assert existing_teacher.phone == "+8801712345678"
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(existing_teacher)


def test_delete_teacher_removes_existing_teacher() -> None:
    db = MagicMock()
    teacher_id = uuid4()
    existing_teacher = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = existing_teacher

    result = delete_teacher(db, teacher_id)

    assert result is True
    db.delete.assert_called_once_with(existing_teacher)
    db.commit.assert_called_once_with()
