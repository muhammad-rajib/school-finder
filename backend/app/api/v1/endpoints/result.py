from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.result import ResultCreate, ResultDeleteResponse, ResultResponse, ResultUpdate
from app.services.result_service import (
    create_result,
    delete_result,
    get_result_by_id,
    get_results_by_school,
    update_result,
)
from app.utils.responses import success_response


router = APIRouter()


@router.post("/results", response_model=APIResponse[ResultResponse], status_code=status.HTTP_201_CREATED)
def create_school_result(
    payload: ResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
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
            detail="Not authorized to create results",
        )

    result_data = payload.model_dump(exclude={"school_id"})
    result = create_result(db, school_id, result_data)
    return success_response(data=result, message="Result created successfully")


@router.put("/results/{result_id}", response_model=APIResponse[ResultResponse])
def update_school_result(
    result_id: UUID,
    payload: ResultUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    result = get_result_by_id(db, result_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found",
        )

    result_school_id = result["school_id"] if isinstance(result, dict) else result.school_id

    if current_user.role == "principal":
        if current_user.school_id != result_school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this result",
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update results",
        )

    updated_result = update_result(db, result_id, payload)
    if updated_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found",
        )
    return success_response(data=updated_result, message="Result updated successfully")


@router.delete("/results/{result_id}", response_model=APIResponse[ResultDeleteResponse])
def delete_school_result(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    result = get_result_by_id(db, result_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found",
        )

    result_school_id = result["school_id"] if isinstance(result, dict) else result.school_id

    if current_user.role == "principal":
        if current_user.school_id != result_school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this result",
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete results",
        )

    deleted = delete_result(db, result_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found",
        )

    return success_response(
        data=ResultDeleteResponse(message="Result deleted successfully"),
        message="Result deleted successfully",
    )


@router.get("/schools/{school_id}/results", response_model=APIResponse[list[ResultResponse]])
def list_school_results(school_id: UUID, db: Session = Depends(get_db)) -> dict:
    return success_response(
        data=get_results_by_school(db, school_id),
        message="Results retrieved successfully",
    )
