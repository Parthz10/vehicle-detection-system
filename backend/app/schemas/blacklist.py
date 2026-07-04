from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class BlacklistCreate(BaseModel):
    plate_number: str = Field(min_length=2, max_length=64)
    reason: str = Field(min_length=3)


class BlacklistUpdate(BaseModel):
    reason: str | None = Field(default=None, min_length=3)
    is_active: bool | None = None


class BlacklistRead(ORMModel):
    id: int
    plate_number: str
    reason: str
    is_active: bool
    created_at: datetime


class AlertRead(ORMModel):
    id: int
    detection_id: int
    plate_number: str
    message: str
    created_at: datetime
    acknowledged: bool
