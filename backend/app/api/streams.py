import tempfile
from pathlib import Path

import cv2
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.ai.pipeline import pipeline
from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import Camera, User, UserRole
from app.schemas.detection import DetectionCreate, DetectionRead
from app.services.detection_service import create_detection
from app.services.tracker import DuplicateTracker

router = APIRouter(prefix="/streams", tags=["streams"])
tracker = DuplicateTracker()


def _camera_source(camera: Camera):
    if camera.source_type.value == "webcam":
        return int(camera.source_url or 0)
    return camera.source_url


@router.get("/{camera_id}/mjpeg")
def stream_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    def generate():
        cap = cv2.VideoCapture(_camera_source(camera))
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Unable to open camera source")
        try:
            frame_index = 0
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                frame_index += 1
                detections = []
                if frame_index % 8 == 0:
                    detections = pipeline.process_frame(frame, camera.name)
                    for item in detections:
                        if tracker.should_record(item.track_id, item.plate_number):
                            create_detection(
                                db,
                                DetectionCreate(
                                    plate_number=item.plate_number,
                                    vehicle_type=item.vehicle_type,
                                    camera_id=camera.id,
                                    camera_name=camera.name,
                                    latitude=camera.latitude,
                                    longitude=camera.longitude,
                                    vehicle_confidence=item.vehicle_confidence,
                                    plate_confidence=item.plate_confidence,
                                    ocr_confidence=item.ocr_confidence,
                                    vehicle_image_path=item.vehicle_image_path,
                                    plate_image_path=item.plate_image_path,
                                    track_id=item.track_id,
                                ),
                            )
                annotated = pipeline.annotate_frame(frame, detections)
                ok, encoded = cv2.imencode(".jpg", annotated)
                if not ok:
                    continue
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + encoded.tobytes() + b"\r\n"
        finally:
            cap.release()

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.post("/upload-video", response_model=list[DetectionRead])
def upload_video(
    camera_name: str = Form(default="Uploaded video"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.administrator, UserRole.police_officer)),
):
    suffix = Path(file.filename or "video.mp4").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(file.file.read())
        temp_path = temp.name
    cap = cv2.VideoCapture(temp_path)
    saved = []
    try:
        frame_index = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_index += 1
            if frame_index % 15 != 0:
                continue
            for item in pipeline.process_frame(frame, camera_name):
                if not tracker.should_record(item.track_id, item.plate_number):
                    continue
                saved.append(
                    create_detection(
                        db,
                        DetectionCreate(
                            plate_number=item.plate_number,
                            vehicle_type=item.vehicle_type,
                            camera_name=camera_name,
                            vehicle_confidence=item.vehicle_confidence,
                            plate_confidence=item.plate_confidence,
                            ocr_confidence=item.ocr_confidence,
                            vehicle_image_path=item.vehicle_image_path,
                            plate_image_path=item.plate_image_path,
                            track_id=item.track_id,
                        ),
                    )
                )
    finally:
        cap.release()
        Path(temp_path).unlink(missing_ok=True)
    return saved


@router.post("/upload-frame", response_model=list[DetectionRead])
def upload_frame(
    camera_name: str = Form(default="Smartphone camera"),
    latitude: float | None = Form(default=None),
    longitude: float | None = Form(default=None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.administrator, UserRole.police_officer)),
):
    content = file.file.read()
    import numpy as np

    frame = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid image")
    saved = []
    for item in pipeline.process_frame(frame, camera_name):
        if not tracker.should_record(item.track_id, item.plate_number):
            continue
        saved.append(
            create_detection(
                db,
                DetectionCreate(
                    plate_number=item.plate_number,
                    vehicle_type=item.vehicle_type,
                    camera_name=camera_name,
                    latitude=latitude,
                    longitude=longitude,
                    vehicle_confidence=item.vehicle_confidence,
                    plate_confidence=item.plate_confidence,
                    ocr_confidence=item.ocr_confidence,
                    vehicle_image_path=item.vehicle_image_path,
                    plate_image_path=item.plate_image_path,
                    track_id=item.track_id,
                ),
            )
        )
    return saved
