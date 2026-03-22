from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.notice import NoticeCreate, NoticeDeleteResponse, NoticeResponse, NoticeUpdate
from app.services.notice_service import (
    create_notice,
    delete_notice,
    get_notice_by_id,
    get_notices_by_school,
    update_notice,
)


router = APIRouter()


@router.post("/notices", response_model=NoticeResponse, status_code=status.HTTP_201_CREATED)
def create_school_notice(
    payload: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoticeResponse:
    if current_user.role == "principal":
        if current_user.school_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Principal must be assigned to a school",
            )
        school_id = current_user.school_id
    elif current_user.role == "admin":
        if payload.school_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="school_id is required for admin",
            )
        school_id = payload.school_id
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create notices",
        )

    notice_data = payload.model_dump(exclude={"school_id"})
    return create_notice(db, school_id, notice_data)


@router.put("/notices/{notice_id}", response_model=NoticeResponse)
def update_school_notice(
    notice_id: UUID,
    payload: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoticeResponse:
    notice = get_notice_by_id(db, notice_id)
    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )

    notice_school_id = notice["school_id"] if isinstance(notice, dict) else notice.school_id

    if current_user.role == "principal":
        if current_user.school_id != notice_school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this notice",
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update notices",
        )

    updated_notice = update_notice(db, notice_id, payload)
    if updated_notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )
    return updated_notice


@router.delete("/notices/{notice_id}", response_model=NoticeDeleteResponse)
def delete_school_notice(
    notice_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoticeDeleteResponse:
    notice = get_notice_by_id(db, notice_id)
    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )

    notice_school_id = notice["school_id"] if isinstance(notice, dict) else notice.school_id

    if current_user.role == "principal":
        if current_user.school_id != notice_school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this notice",
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete notices",
        )

    deleted = delete_notice(db, notice_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )

    return NoticeDeleteResponse(message="Notice deleted successfully")


@router.get("/schools/{school_id}/notices", response_model=list[NoticeResponse])
def list_school_notices(
    school_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[NoticeResponse]:
    if current_user.role == "principal" and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this school's notices",
        )
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access notices",
        )

    return get_notices_by_school(db, school_id)
