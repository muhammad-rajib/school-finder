from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.student import StudentStatsResponse, StudentStatsUpdate
from app.services.student_service import get_student_stats, update_student_stats
from app.utils.responses import success_response


router = APIRouter()


def _build_student_stats_response(school) -> StudentStatsResponse:
    if isinstance(school, dict):
        return StudentStatsResponse(
            total=school["total_students"],
            boys=school["boys"],
            girls=school["girls"],
        )

    return StudentStatsResponse(
        total=school.total_students,
        boys=school.boys,
        girls=school.girls,
    )


@router.get("/schools/{school_id}/students", response_model=APIResponse[StudentStatsResponse])
def retrieve_student_stats(
    school_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    school = get_student_stats(db, school_id)
    if school is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")

    if current_user.role == "principal" and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this school",
        )
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access student stats",
        )

    return success_response(
        data=_build_student_stats_response(school),
        message="Student stats retrieved successfully",
    )


@router.put("/schools/{school_id}/students", response_model=APIResponse[StudentStatsResponse])
def update_school_student_stats(
    school_id: UUID,
    payload: StudentStatsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    if current_user.role == "principal" and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this school",
        )
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update student stats",
        )

    school = update_student_stats(db, school_id, payload)
    if school is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")

    return success_response(
        data=_build_student_stats_response(school),
        message="Student stats updated successfully",
    )
