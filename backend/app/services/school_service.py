from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school import School


def get_schools(db: Session) -> list[School]:
    return db.query(School).order_by(School.name.asc()).all()


def _normalize_filter(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


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
    normalized_emis_code = _normalize_filter(emis_code)
    normalized_name = _normalize_filter(name)
    normalized_division = _normalize_filter(division)
    normalized_district = _normalize_filter(district)
    normalized_upazila = _normalize_filter(upazila)
    normalized_union = _normalize_filter(union)

    if normalized_emis_code:
        query = query.filter(School.emis_code == normalized_emis_code)

    if normalized_name:
        query = query.filter(School.name.ilike(f"%{normalized_name}%"))

    if normalized_division:
        query = query.filter(School.division.ilike(f"%{normalized_division}%"))

    if normalized_district:
        query = query.filter(School.district.ilike(f"%{normalized_district}%"))

    if normalized_upazila:
        query = query.filter(School.upazila.ilike(f"%{normalized_upazila}%"))

    if normalized_union:
        query = query.filter(School.union.ilike(f"%{normalized_union}%"))

    query = query.order_by(School.name.asc())
    query = query.offset(skip).limit(limit)

    return query.all()


def get_school_by_id(db: Session, school_id: UUID) -> School | None:
    return db.query(School).filter(School.id == school_id).first()
