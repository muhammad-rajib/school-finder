from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.result import ResultResponse
from app.services.result_service import get_results_by_school


router = APIRouter()


@router.get("/schools/{school_id}/results", response_model=list[ResultResponse])
def list_school_results(school_id: UUID, db: Session = Depends(get_db)) -> list[ResultResponse]:
    return get_results_by_school(db, school_id)
