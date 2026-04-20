from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import ModerationActionType, ModerationTargetType


class ModerationReportCreate(BaseModel):
    target_type: ModerationTargetType
    target_id: int
    reason: str
    details: Optional[str] = None


class ModerationReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reporter_user_id: int
    target_type: ModerationTargetType
    target_id: int
    reason: str
    details: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class ModerationReportStatusUpdate(BaseModel):
    status: str


class ModerationActionCreate(BaseModel):
    action_type: ModerationActionType
    note: Optional[str] = None


class ModerationActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    report_id: int
    moderator_user_id: Optional[int]
    action_type: ModerationActionType
    note: Optional[str]
    created_at: datetime
