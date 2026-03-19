from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school import School


def get_schools(db: Session) -> list[School]:
    return db.query(School).order_by(School.name.asc()).all()


def search_schools(db: Session, query: str) -> list[School]:
    return (
        db.query(School)
        .filter(School.name.ilike(f"%{query}%"))
        .order_by(School.name.asc())
        .limit(50)
        .all()
    )


def get_school_by_id(db: Session, school_id: UUID) -> School | None:
    return db.query(School).filter(School.id == school_id).first()
