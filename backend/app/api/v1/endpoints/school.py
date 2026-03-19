from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.school import SchoolResponse
from app.services.school_service import get_schools


router = APIRouter()


@router.get("/schools", response_model=list[SchoolResponse])
def list_schools(db: Session = Depends(get_db)) -> list[SchoolResponse]:
    return get_schools(db)
