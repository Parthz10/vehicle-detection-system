from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import User, UserRole
from app.schemas.common import StatsSummary
from app.schemas.detection import DetectionCreate, DetectionRead, DetectionSearch
from app.services.detection_service import create_detection, get_stats, search_detections

router = APIRouter(prefix="/detections", tags=["detections"])


@router.get("", response_model=list[DetectionRead])
def list_detections(
    plate_number: str | None = None,
    vehicle_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list:
    from datetime import datetime
    from app.models.entities import VehicleType

    params = DetectionSearch(
        plate_number=plate_number,
        vehicle_type=VehicleType(vehicle_type) if vehicle_type else None,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        end_date=datetime.fromisoformat(end_date) if end_date else None,
        limit=limit,
    )
    return search_detections(db, params)


@router.post("", response_model=DetectionRead)
def add_detection(
    payload: DetectionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.administrator, UserRole.police_officer)),
):
    return create_detection(db, payload)


@router.get("/stats", response_model=StatsSummary)
def stats(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> StatsSummary:
    return get_stats(db)
