from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProfessionCreate(BaseModel):
    name: str


class ProfessionUpdate(BaseModel):
    name: str | None = None


class ProfessionResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
