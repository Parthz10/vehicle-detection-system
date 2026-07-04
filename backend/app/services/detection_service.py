from collections import Counter
from datetime import datetime, time

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.entities import Alert, BlacklistEntry, Detection, VehicleType
from app.schemas.common import StatsSummary
from app.schemas.detection import DetectionCreate, DetectionSearch
from app.services.plate import normalize_plate


def create_detection(db: Session, data: DetectionCreate) -> Detection:
    plate_number = normalize_plate(data.plate_number)
    blacklist = (
        db.query(BlacklistEntry)
        .filter(BlacklistEntry.plate_number == plate_number, BlacklistEntry.is_active.is_(True))
        .first()
    )
    detection = Detection(**data.model_dump(exclude={"plate_number"}), plate_number=plate_number)
    detection.is_blacklisted = blacklist is not None
    db.add(detection)
    db.flush()
    if blacklist:
        db.add(
            Alert(
                detection_id=detection.id,
                plate_number=plate_number,
                message=f"Blacklisted plate detected: {plate_number}. Reason: {blacklist.reason}",
            )
        )
    db.commit()
    db.refresh(detection)
    return detection


def search_detections(db: Session, params: DetectionSearch) -> list[Detection]:
    query = db.query(Detection)
    if params.plate_number:
        query = query.filter(Detection.plate_number.ilike(f"%{normalize_plate(params.plate_number)}%"))
    if params.vehicle_type:
        query = query.filter(Detection.vehicle_type == params.vehicle_type)
    if params.start_date:
        query = query.filter(Detection.timestamp >= params.start_date)
    if params.end_date:
        query = query.filter(Detection.timestamp <= params.end_date)
    return query.order_by(Detection.timestamp.desc()).limit(params.limit).all()


def get_stats(db: Session) -> StatsSummary:
    now = datetime.utcnow()
    start_today = datetime.combine(now.date(), time.min)
    total = db.query(func.count(Detection.id)).scalar() or 0
    today = db.query(func.count(Detection.id)).filter(Detection.timestamp >= start_today).scalar() or 0
    blacklisted = db.query(func.count(Detection.id)).filter(Detection.is_blacklisted.is_(True)).scalar() or 0
    vehicle_rows = db.query(Detection.vehicle_type, func.count(Detection.id)).group_by(Detection.vehicle_type).all()
    by_vehicle_type = {str(vehicle.value if isinstance(vehicle, VehicleType) else vehicle): count for vehicle, count in vehicle_rows}
    last_rows = db.query(Detection.timestamp).order_by(Detection.timestamp.desc()).limit(500).all()
    by_day = Counter(row[0].date().isoformat() for row in last_rows)
    return StatsSummary(
        total_detections=total,
        today=today,
        blacklisted_hits=blacklisted,
        by_vehicle_type=by_vehicle_type,
        by_day=dict(sorted(by_day.items())),
        generated_at=now,
    )
