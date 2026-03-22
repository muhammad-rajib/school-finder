from uuid import UUID

from pydantic import BaseModel


class SchoolImageResponse(BaseModel):
    id: UUID
    image_url: str
    is_cover: bool

    class Config:
        from_attributes = True


class ImageCreateResponse(BaseModel):
    id: UUID
    image_url: str
    is_cover: bool


class ImageDeleteResponse(BaseModel):
    message: str
