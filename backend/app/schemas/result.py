from pydantic import BaseModel, ConfigDict


class ResultResponse(BaseModel):
    year: int
    exam_type: str
    pass_rate: float

    model_config = ConfigDict(from_attributes=True)
