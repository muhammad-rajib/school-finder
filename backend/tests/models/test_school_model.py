from app.models.school import School


def test_school_model_exposes_student_stat_columns() -> None:
    columns = School.__table__.columns

    assert "total_students" in columns
    assert "boys" in columns
    assert "girls" in columns
    assert columns["name"].nullable is False


def test_school_model_declares_expected_relationships() -> None:
    relationships = School.__mapper__.relationships

    assert "images" in relationships
    assert "teachers" in relationships
    assert "results" in relationships
    assert "notices" in relationships
