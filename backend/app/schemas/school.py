from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SchoolResponse(BaseModel):
    id: UUID
    emis_code: str
    name: str
    country_code: str
    division: str | None = None
    district: str | None = None
    upazila: str | None = None
    union: str | None = None
    address: str | None = None
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    established_year: int | None = None
    total_students: int
    total_teachers: int
    total_classrooms: int
    has_electricity: bool
    has_water: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SchoolListResponse(BaseModel):
    data: list[SchoolResponse]
    page: int
    limit: int


class StudentStatsResponse(BaseModel):
    total: int
    boys: int
    girls: int
