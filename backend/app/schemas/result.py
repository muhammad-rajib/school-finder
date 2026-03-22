from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResultCreate(BaseModel):
    school_id: UUID | None = None
    year: int
    exam_type: str
    pass_rate: float


class ResultUpdate(BaseModel):
    year: int | None = None
    exam_type: str | None = None
    pass_rate: float | None = None


class ResultResponse(BaseModel):
    id: UUID
    year: int
    exam_type: str
    pass_rate: float

    model_config = ConfigDict(from_attributes=True)


class ResultDeleteResponse(BaseModel):
    message: str
