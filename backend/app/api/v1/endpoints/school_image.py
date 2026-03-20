from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.school_image import SchoolImageResponse
from app.services.school_image_service import get_cover_image, get_school_images


router = APIRouter()


@router.get("/schools/{school_id}/images", response_model=list[SchoolImageResponse])
def list_school_images(school_id: UUID, db: Session = Depends(get_db)) -> list[SchoolImageResponse]:
    return get_school_images(db, school_id)


@router.get("/schools/{school_id}/images/cover", response_model=SchoolImageResponse)
def retrieve_cover_image(school_id: UUID, db: Session = Depends(get_db)) -> SchoolImageResponse:
    image = get_cover_image(db, school_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Cover image not found")
    return image
