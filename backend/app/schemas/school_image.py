from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SchoolImageResponse(BaseModel):
    id: UUID
    image_url: str
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)


class ImageCreateResponse(BaseModel):
    id: UUID
    image_url: str
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)


class ImageDeleteResponse(BaseModel):
    message: str
