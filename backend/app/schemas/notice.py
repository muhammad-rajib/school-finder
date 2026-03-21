from datetime import date

from pydantic import BaseModel, ConfigDict


class NoticeResponse(BaseModel):
    title: str
    description: str
    published_date: date

    model_config = ConfigDict(from_attributes=True)
