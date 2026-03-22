from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.school_image import ImageCreateResponse, ImageDeleteResponse, SchoolImageResponse
from app.services.s3_service import upload_file
from app.services.school_image_service import (
    create_school_image,
    delete_school_image,
    get_cover_image,
    get_school_image_by_id,
    get_school_images,
    set_cover_image,
)
from app.utils.responses import success_response


router = APIRouter()


@router.post(
    "/schools/{school_id}/images",
    response_model=APIResponse[ImageCreateResponse],
    status_code=status.HTTP_201_CREATED,
)
def upload_school_image(
    school_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    if current_user.role == "principal" and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload images for this school",
        )
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload school images",
        )

    image_url = upload_file(file, f"schools/{school_id}")
    image = create_school_image(db, school_id, image_url=image_url, is_cover=False)
    return success_response(data=image, message="Image uploaded successfully")


@router.delete("/images/{image_id}", response_model=APIResponse[ImageDeleteResponse])
def delete_image(
    image_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    image = get_school_image_by_id(db, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image_school_id = image["school_id"] if isinstance(image, dict) else image.school_id

    if current_user.role == "principal" and current_user.school_id != image_school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this image",
        )
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete images",
        )

    deleted = delete_school_image(db, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")

    return success_response(
        data=ImageDeleteResponse(message="Image deleted"),
        message="Image deleted",
    )


@router.put("/images/{image_id}/cover", response_model=APIResponse[SchoolImageResponse])
def set_school_cover_image(
    image_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    image = get_school_image_by_id(db, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image_school_id = image["school_id"] if isinstance(image, dict) else image.school_id

    if current_user.role == "principal" and current_user.school_id != image_school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this image",
        )
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update images",
        )

    updated_image = set_cover_image(db, image_id)
    if updated_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return success_response(data=updated_image, message="Cover image updated successfully")


@router.get("/schools/{school_id}/images", response_model=APIResponse[list[SchoolImageResponse]])
def list_school_images(school_id: UUID, db: Session = Depends(get_db)) -> dict:
    return success_response(
        data=get_school_images(db, school_id),
        message="Images retrieved successfully",
    )


@router.get("/schools/{school_id}/images/cover", response_model=APIResponse[SchoolImageResponse])
def retrieve_cover_image(school_id: UUID, db: Session = Depends(get_db)) -> dict:
    image = get_cover_image(db, school_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Cover image not found")
    return success_response(data=image, message="Cover image retrieved successfully")
