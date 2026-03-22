from pydantic import BaseModel


class StudentStatsUpdate(BaseModel):
    total: int
    boys: int
    girls: int


class StudentStatsResponse(BaseModel):
    total: int
    boys: int
    girls: int
