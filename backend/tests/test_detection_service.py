from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.entities import BlacklistEntry, VehicleType
from app.schemas.detection import DetectionCreate
from app.services.detection_service import create_detection


def test_create_detection_generates_alert_for_blacklist() -> None:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    session.add(BlacklistEntry(plate_number="BA 2 PA 1234", reason="Stolen vehicle"))
    session.commit()

    detection = create_detection(
        session,
        DetectionCreate(
            plate_number="ba-2-pa-1234",
            vehicle_type=VehicleType.car,
            camera_name="Gate 1",
            vehicle_confidence=0.96,
            plate_confidence=0.91,
            ocr_confidence=0.91,
        ),
    )

    assert detection.is_blacklisted is True
    assert detection.alerts[0].plate_number == "BA 2 PA 1234"
