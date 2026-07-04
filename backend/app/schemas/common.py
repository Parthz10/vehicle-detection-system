from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


class Message(BaseModel):
    message: str


class StatsSummary(BaseModel):
    total_detections: int
    today: int
    blacklisted_hits: int
    by_vehicle_type: dict[str, int]
    by_day: dict[str, int]
    generated_at: datetime
