from uuid import UUID

from sqlalchemy.orm import Session

from app.models.notice import Notice


def get_notices_by_school(db: Session, school_id: UUID) -> list[Notice]:
    return (
        db.query(Notice)
        .filter(Notice.school_id == school_id)
        .order_by(Notice.published_date.desc(), Notice.created_at.desc())
        .all()
    )
