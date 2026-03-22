from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NoticeCreate(BaseModel):
    school_id: UUID | None = None
    title: str
    description: str
    published_date: date


class NoticeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    published_date: date | None = None


class NoticeResponse(BaseModel):
    id: UUID
    title: str
    description: str
    published_date: date

    model_config = ConfigDict(from_attributes=True)


class NoticeDeleteResponse(BaseModel):
    message: str
