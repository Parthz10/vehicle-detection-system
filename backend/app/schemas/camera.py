from datetime import datetime

from pydantic import BaseModel, Field

from app.models.entities import CameraType
from app.schemas.common import ORMModel


class CameraCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    source_type: CameraType
    source_url: str | None = None
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class CameraUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    source_type: CameraType | None = None
    source_url: str | None = None
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None


class CameraRead(ORMModel):
    id: int
    name: str
    source_type: CameraType
    source_url: str | None
    location_name: str | None
    latitude: float | None
    longitude: float | None
    is_active: bool
    created_at: datetime
