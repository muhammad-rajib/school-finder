from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TeacherResponse(BaseModel):
    id: UUID
    name: str
    designation: str
    subject: str | None = None
    qualification: str | None = None

    model_config = ConfigDict(from_attributes=True)
