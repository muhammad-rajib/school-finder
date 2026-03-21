from app.models.teacher import Teacher


def test_teacher_model_has_expected_columns() -> None:
    columns = Teacher.__table__.columns

    assert "school_id" in columns
    assert "name" in columns
    assert "designation" in columns
    assert "joining_date" in columns
    assert columns["name"].nullable is False


def test_teacher_model_declares_school_relationship() -> None:
    relationships = Teacher.__mapper__.relationships

    assert "school" in relationships
