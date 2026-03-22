from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school import School


def update_student_stats(db: Session, school_id: UUID, data) -> School | None:
    school = db.query(School).filter(School.id == school_id).first()
    if school is None:
        return None

    payload = data.model_dump() if hasattr(data, "model_dump") else dict(data)
    school.total_students = payload["total"]
    school.boys = payload["boys"]
    school.girls = payload["girls"]
    db.commit()
    db.refresh(school)
    return school


def get_student_stats(db: Session, school_id: UUID) -> School | None:
    return db.query(School).filter(School.id == school_id).first()
