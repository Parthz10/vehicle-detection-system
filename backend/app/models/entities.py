from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class UserRole(str, Enum):
    administrator = "administrator"
    police_officer = "police_officer"
    viewer = "viewer"


class CameraType(str, Enum):
    webcam = "webcam"
    rtsp = "rtsp"
    upload = "upload"
    smartphone = "smartphone"


class VehicleType(str, Enum):
    car = "car"
    motorcycle = "motorcycle"
    bus = "bus"
    truck = "truck"
    van = "van"
    bicycle = "bicycle"
    unknown = "unknown"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.viewer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    source_type: Mapped[CameraType] = mapped_column(SAEnum(CameraType))
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    detections: Mapped[list["Detection"]] = relationship(back_populates="camera")


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plate_number: Mapped[str] = mapped_column(String(64), index=True)
    vehicle_type: Mapped[VehicleType] = mapped_column(SAEnum(VehicleType), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    camera_id: Mapped[int | None] = mapped_column(ForeignKey("cameras.id"), nullable=True)
    camera_name: Mapped[str] = mapped_column(String(120), index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    vehicle_confidence: Mapped[float] = mapped_column(Float)
    plate_confidence: Mapped[float] = mapped_column(Float)
    ocr_confidence: Mapped[float] = mapped_column(Float)
    vehicle_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    plate_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    track_id: Mapped[str | None] = mapped_column(String(120), index=True, nullable=True)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)

    camera: Mapped[Camera | None] = relationship(back_populates="detections")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="detection")


class BlacklistEntry(Base):
    __tablename__ = "blacklist_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plate_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    reason: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    detection_id: Mapped[int] = mapped_column(ForeignKey("detections.id"))
    plate_number: Mapped[str] = mapped_column(String(64), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)

    detection: Mapped[Detection] = relationship(back_populates="alerts")
