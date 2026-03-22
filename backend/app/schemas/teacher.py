from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TeacherCreate(BaseModel):
    name: str
    designation: str
    school_id: UUID | None = None
    subject: str | None = None
    qualification: str | None = None
    phone: str | None = None
    joining_date: date | None = None


class TeacherUpdate(BaseModel):
    name: str | None = None
    designation: str | None = None
    subject: str | None = None
    qualification: str | None = None
    phone: str | None = None
    joining_date: date | None = None


class TeacherResponse(BaseModel):
    id: UUID
    name: str
    designation: str
    subject: str | None = None
    qualification: str | None = None

    model_config = ConfigDict(from_attributes=True)
