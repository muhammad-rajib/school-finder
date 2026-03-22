from uuid import UUID

from sqlalchemy.orm import Session

from app.models.notice import Notice


def get_notice_by_id(db: Session, notice_id: UUID) -> Notice | None:
    return db.query(Notice).filter(Notice.id == notice_id).first()


def create_notice(db: Session, school_id: UUID, data) -> Notice:
    payload = data.model_dump() if hasattr(data, "model_dump") else dict(data)
    payload.pop("school_id", None)
    notice = Notice(school_id=school_id, **payload)
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice


def update_notice(db: Session, notice_id: UUID, data) -> Notice | None:
    notice = get_notice_by_id(db, notice_id)
    if notice is None:
        return None

    payload = (
        data.model_dump(exclude_unset=True)
        if hasattr(data, "model_dump")
        else dict(data)
    )
    for field, value in payload.items():
        setattr(notice, field, value)

    db.commit()
    db.refresh(notice)
    return notice


def delete_notice(db: Session, notice_id: UUID) -> bool:
    notice = get_notice_by_id(db, notice_id)
    if notice is None:
        return False

    db.delete(notice)
    db.commit()
    return True


def get_notices_by_school(db: Session, school_id: UUID) -> list[Notice]:
    return (
        db.query(Notice)
        .filter(Notice.school_id == school_id)
        .order_by(Notice.published_date.desc(), Notice.created_at.desc())
        .all()
    )
