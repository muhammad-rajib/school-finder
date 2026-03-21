from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notice import NoticeResponse
from app.services.notice_service import get_notices_by_school


router = APIRouter()


@router.get("/schools/{school_id}/notices", response_model=list[NoticeResponse])
def list_school_notices(school_id: UUID, db: Session = Depends(get_db)) -> list[NoticeResponse]:
    return get_notices_by_school(db, school_id)
