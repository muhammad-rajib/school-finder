from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.school import SchoolListResponse, SchoolResponse
from app.services.school_service import get_school_by_id, search_schools


router = APIRouter()


@router.get("/schools", response_model=SchoolListResponse)
def list_schools(
    name: str | None = Query(default=None),
    division: str | None = Query(default=None),
    district: str | None = Query(default=None),
    upazila: str | None = Query(default=None),
    union: str | None = Query(default=None),
    emis_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> SchoolListResponse:
    effective_limit = min(limit, 50)
    skip = 0 if emis_code else (page - 1) * effective_limit

    schools = search_schools(
        db=db,
        name=name,
        division=division,
        district=district,
        upazila=upazila,
        union=union,
        emis_code=emis_code,
        skip=skip,
        limit=1 if emis_code else effective_limit,
    )

    return SchoolListResponse(data=schools, page=page, limit=effective_limit)


@router.get("/schools/{school_id}", response_model=SchoolResponse)
def retrieve_school(school_id: UUID, db: Session = Depends(get_db)) -> SchoolResponse:
    school = get_school_by_id(db, school_id)
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school
