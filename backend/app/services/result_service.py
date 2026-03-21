from uuid import UUID

from sqlalchemy.orm import Session

from app.models.result import Result


def get_results_by_school(db: Session, school_id: UUID) -> list[Result]:
    return (
        db.query(Result)
        .filter(Result.school_id == school_id)
        .order_by(Result.year.desc(), Result.exam_type.asc())
        .all()
    )
