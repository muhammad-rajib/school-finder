from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school_image import SchoolImage


def create_school_image(
    db: Session,
    school_id: UUID,
    image_url: str,
    is_cover: bool = False,
) -> SchoolImage:
    image = SchoolImage(school_id=school_id, image_url=image_url, is_cover=is_cover)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_school_image_by_id(db: Session, image_id: UUID) -> SchoolImage | None:
    return db.query(SchoolImage).filter(SchoolImage.id == image_id).first()


def delete_school_image(db: Session, image_id: UUID) -> bool:
    image = get_school_image_by_id(db, image_id)
    if image is None:
        return False

    db.delete(image)
    db.commit()
    return True


def set_cover_image(db: Session, image_id: UUID) -> SchoolImage | None:
    image = get_school_image_by_id(db, image_id)
    if image is None:
        return None

    db.query(SchoolImage).filter(SchoolImage.school_id == image.school_id).update(
        {SchoolImage.is_cover: False}
    )
    image.is_cover = True
    db.commit()
    db.refresh(image)
    return image


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
