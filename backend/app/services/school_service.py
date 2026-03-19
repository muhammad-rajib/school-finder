from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school import School


def get_schools(db: Session) -> list[School]:
    return db.query(School).order_by(School.name.asc()).all()


def search_schools(
    db: Session,
    name: str | None,
    division: str | None,
    district: str | None,
    upazila: str | None,
    union: str | None,
    emis_code: str | None,
    skip: int,
    limit: int,
) -> list[School]:
    query = db.query(School)

    if emis_code:
        query = query.filter(School.emis_code == emis_code)

    if name:
        query = query.filter(School.name.ilike(f"%{name}%"))

    if division:
        query = query.filter(School.division == division)

    if district:
        query = query.filter(School.district == district)

    if upazila:
        query = query.filter(School.upazila == upazila)

    if union:
        query = query.filter(School.union == union)

    query = query.order_by(School.name.asc())
    query = query.offset(skip).limit(limit)

    return query.all()


def get_school_by_id(db: Session, school_id: UUID) -> School | None:
    return db.query(School).filter(School.id == school_id).first()
