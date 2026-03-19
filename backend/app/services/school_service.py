from sqlalchemy.orm import Session

from app.models.school import School


def get_schools(db: Session) -> list[School]:
    return db.query(School).order_by(School.name.asc()).all()
