from uuid import UUID

from sqlalchemy.orm import Session

from app.models.teacher import Teacher


def get_teachers_by_school(db: Session, school_id: UUID) -> list[Teacher]:
    return (
        db.query(Teacher)
        .filter(Teacher.school_id == school_id)
        .order_by(Teacher.name.asc())
        .all()
    )
