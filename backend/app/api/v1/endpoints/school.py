from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.school import SchoolResponse
from app.services.school_service import get_school_by_id, get_schools


router = APIRouter()


@router.get("/schools", response_model=list[SchoolResponse])
def list_schools(db: Session = Depends(get_db)) -> list[SchoolResponse]:
    return get_schools(db)


@router.get("/schools/{school_id}", response_model=SchoolResponse)
def retrieve_school(school_id: UUID, db: Session = Depends(get_db)) -> SchoolResponse:
    school = get_school_by_id(db, school_id)
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school
