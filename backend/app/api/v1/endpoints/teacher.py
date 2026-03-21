from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.teacher import TeacherResponse
from app.services.teacher_service import get_teachers_by_school


router = APIRouter()


@router.get("/schools/{school_id}/teachers", response_model=list[TeacherResponse])
def list_school_teachers(school_id: UUID, db: Session = Depends(get_db)) -> list[TeacherResponse]:
    return get_teachers_by_school(db, school_id)
