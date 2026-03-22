from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.teacher import (
    TeacherCreate,
    TeacherDeleteResponse,
    TeacherResponse,
    TeacherUpdate,
)
from app.services.teacher_service import (
    create_teacher,
    delete_teacher,
    get_teacher_by_id,
    get_teachers_by_school,
    update_teacher,
)


router = APIRouter()


@router.post("/teachers", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_school_teacher(
    payload: TeacherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TeacherResponse:
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
            detail="Not authorized to create teachers",
        )

    teacher_data = payload.model_dump(exclude={"school_id"})
    return create_teacher(db, school_id, teacher_data)


@router.put("/teachers/{teacher_id}", response_model=TeacherResponse)
def update_school_teacher(
    teacher_id: UUID,
    payload: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TeacherResponse:
    teacher = get_teacher_by_id(db, teacher_id)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )

    teacher_school_id = teacher["school_id"] if isinstance(teacher, dict) else teacher.school_id

    if current_user.role == "principal":
        if current_user.school_id != teacher_school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this teacher",
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update teachers",
        )

    updated_teacher = update_teacher(db, teacher_id, payload)
    if updated_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )
    return updated_teacher


@router.delete("/teachers/{teacher_id}", response_model=TeacherDeleteResponse)
def delete_school_teacher(
    teacher_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TeacherDeleteResponse:
    teacher = get_teacher_by_id(db, teacher_id)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )

    teacher_school_id = teacher["school_id"] if isinstance(teacher, dict) else teacher.school_id

    if current_user.role == "principal":
        if current_user.school_id != teacher_school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this teacher",
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete teachers",
        )

    deleted = delete_teacher(db, teacher_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )

    return TeacherDeleteResponse(message="Teacher deleted successfully")


@router.get("/schools/{school_id}/teachers", response_model=list[TeacherResponse])
def list_school_teachers(school_id: UUID, db: Session = Depends(get_db)) -> list[TeacherResponse]:
    return get_teachers_by_school(db, school_id)
