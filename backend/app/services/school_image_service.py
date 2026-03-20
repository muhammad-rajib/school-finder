from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school_image import SchoolImage


def get_school_images(db: Session, school_id: UUID) -> list[SchoolImage]:
    return (
        db.query(SchoolImage)
        .filter(SchoolImage.school_id == school_id)
        .order_by(SchoolImage.created_at.asc())
        .all()
    )


def get_cover_image(db: Session, school_id: UUID) -> SchoolImage | None:
    return (
        db.query(SchoolImage)
        .filter(SchoolImage.school_id == school_id, SchoolImage.is_cover.is_(True))
        .first()
    )
