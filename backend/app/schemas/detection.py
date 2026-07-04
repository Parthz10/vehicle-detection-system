from datetime import datetime

from pydantic import BaseModel, Field

from app.models.entities import VehicleType
from app.schemas.common import ORMModel


class DetectionCreate(BaseModel):
    plate_number: str = Field(min_length=2, max_length=64)
    vehicle_type: VehicleType = VehicleType.unknown
    camera_id: int | None = None
    camera_name: str = "Manual"
    latitude: float | None = None
    longitude: float | None = None
    vehicle_confidence: float = Field(ge=0, le=1)
    plate_confidence: float = Field(ge=0, le=1)
    ocr_confidence: float = Field(ge=0, le=1)
    vehicle_image_path: str | None = None
    plate_image_path: str | None = None
    track_id: str | None = None


class DetectionRead(ORMModel):
    id: int
    plate_number: str
    vehicle_type: VehicleType
    timestamp: datetime
    camera_id: int | None
    camera_name: str
    latitude: float | None
    longitude: float | None
    vehicle_confidence: float
    plate_confidence: float
    ocr_confidence: float
    vehicle_image_path: str | None
    plate_image_path: str | None
    track_id: str | None
    is_blacklisted: bool


class DetectionSearch(BaseModel):
    plate_number: str | None = None
    vehicle_type: VehicleType | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    limit: int = Field(default=50, ge=1, le=500)
