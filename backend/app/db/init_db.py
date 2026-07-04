from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import Base, engine
from app.models.entities import Camera, CameraType, User, UserRole


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def seed_db(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        db.add(
            User(
                email="admin@example.com",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.administrator,
            )
        )

    if not db.query(Camera).filter(Camera.name == "Webcam 0").first():
        db.add(Camera(name="Webcam 0", source_type=CameraType.webcam, source_url="0"))

    db.commit()
