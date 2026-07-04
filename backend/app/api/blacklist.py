from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import Alert, BlacklistEntry, User, UserRole
from app.schemas.blacklist import AlertRead, BlacklistCreate, BlacklistRead, BlacklistUpdate
from app.services.plate import normalize_plate

router = APIRouter(tags=["blacklist"])


@router.get("/blacklist", response_model=list[BlacklistRead])
def list_blacklist(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[BlacklistEntry]:
    return db.query(BlacklistEntry).order_by(BlacklistEntry.created_at.desc()).all()


@router.post("/blacklist", response_model=BlacklistRead)
def create_blacklist_entry(
    payload: BlacklistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.administrator)),
) -> BlacklistEntry:
    plate_number = normalize_plate(payload.plate_number)
    if db.query(BlacklistEntry).filter(BlacklistEntry.plate_number == plate_number).first():
        raise HTTPException(status_code=409, detail="Plate already blacklisted")
    entry = BlacklistEntry(plate_number=plate_number, reason=payload.reason, created_by_id=current_user.id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/blacklist/{entry_id}", response_model=BlacklistRead)
def update_blacklist_entry(
    entry_id: int,
    payload: BlacklistUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.administrator)),
) -> BlacklistEntry:
    entry = db.get(BlacklistEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Blacklist entry not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/alerts", response_model=list[AlertRead])
def list_alerts(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[Alert]:
    return db.query(Alert).order_by(Alert.created_at.desc()).limit(100).all()


@router.patch("/alerts/{alert_id}/ack", response_model=AlertRead)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.administrator, UserRole.police_officer)),
) -> Alert:
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert
