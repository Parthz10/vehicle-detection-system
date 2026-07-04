import logging
import uuid
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from app.core.config import get_settings
from app.models.entities import VehicleType
from app.services.plate import is_valid_plate, normalize_plate

logger = logging.getLogger(__name__)

COCO_TO_VEHICLE = {
    "car": VehicleType.car,
    "motorcycle": VehicleType.motorcycle,
    "bus": VehicleType.bus,
    "truck": VehicleType.truck,
    "bicycle": VehicleType.bicycle,
}


@dataclass
class InferenceDetection:
    plate_number: str
    vehicle_type: VehicleType
    vehicle_confidence: float
    plate_confidence: float
    ocr_confidence: float
    vehicle_image_path: str | None
    plate_image_path: str | None
    track_id: str
    bbox: tuple[int, int, int, int]


class ANPRPipeline:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._vehicle_model = None
        self._ocr = None
        self.upload_dir = self.settings.upload_dir
        (self.upload_dir / "vehicles").mkdir(parents=True, exist_ok=True)
        (self.upload_dir / "plates").mkdir(parents=True, exist_ok=True)

    @property
    def vehicle_model(self):
        if self._vehicle_model is None:
            from ultralytics import YOLO

            self._vehicle_model = YOLO(self.settings.yolo_model_path)
        return self._vehicle_model

    @property
    def ocr(self):
        if self._ocr is None:
            from paddleocr import PaddleOCR

            self._ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
        return self._ocr

    def process_frame(self, frame: np.ndarray, camera_name: str) -> list[InferenceDetection]:
        detections: list[InferenceDetection] = []
        results = self.vehicle_model.predict(frame, conf=self.settings.vehicle_confidence_threshold, verbose=False)
        for result in results:
            names = result.names
            for box in result.boxes:
                label = names[int(box.cls[0])]
                if label not in COCO_TO_VEHICLE:
                    continue
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                crop = frame[max(y1, 0) : max(y2, 0), max(x1, 0) : max(x2, 0)]
                if crop.size == 0:
                    continue
                plate_crop = self._estimate_plate_region(crop)
                plate_text, ocr_confidence = self._read_plate(plate_crop)
                plate_number = normalize_plate(plate_text)
                if not is_valid_plate(plate_number) or ocr_confidence < self.settings.plate_confidence_threshold:
                    continue
                vehicle_path = self._save_image("vehicles", crop, camera_name)
                plate_path = self._save_image("plates", plate_crop, camera_name)
                track_id = f"{camera_name}:{label}:{x1}:{y1}:{x2}:{y2}"
                detections.append(
                    InferenceDetection(
                        plate_number=plate_number,
                        vehicle_type=COCO_TO_VEHICLE[label],
                        vehicle_confidence=confidence,
                        plate_confidence=ocr_confidence,
                        ocr_confidence=ocr_confidence,
                        vehicle_image_path=vehicle_path,
                        plate_image_path=plate_path,
                        track_id=track_id,
                        bbox=(x1, y1, x2, y2),
                    )
                )
        return detections

    def annotate_frame(self, frame: np.ndarray, detections: list[InferenceDetection]) -> np.ndarray:
        annotated = frame.copy()
        for detection in detections:
            x1, y1, x2, y2 = detection.bbox
            color = (0, 0, 255) if detection.ocr_confidence >= 0.9 else (0, 180, 0)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            label = f"{detection.vehicle_type.value} {detection.plate_number} {detection.ocr_confidence:.2f}"
            cv2.putText(annotated, label, (x1, max(y1 - 8, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
        return annotated

    def _estimate_plate_region(self, vehicle_crop: np.ndarray) -> np.ndarray:
        height, width = vehicle_crop.shape[:2]
        y1 = int(height * 0.55)
        y2 = int(height * 0.95)
        x1 = int(width * 0.15)
        x2 = int(width * 0.85)
        plate = vehicle_crop[y1:y2, x1:x2]
        if plate.size == 0:
            return vehicle_crop
        gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 7, 35, 35)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def _read_plate(self, image: np.ndarray) -> tuple[str, float]:
        try:
            results = self.ocr.ocr(image, cls=True)
        except Exception as exc:
            logger.warning("OCR failed: %s", exc)
            return "", 0.0
        candidates: list[tuple[str, float]] = []
        for page in results or []:
            for line in page or []:
                text, confidence = line[1]
                candidates.append((str(text), float(confidence)))
        if not candidates:
            return "", 0.0
        text, confidence = max(candidates, key=lambda item: item[1])
        return text, confidence

    def _save_image(self, folder: str, image: np.ndarray, camera_name: str) -> str:
        safe_camera = "".join(ch if ch.isalnum() else "_" for ch in camera_name)[:40]
        filename = f"{safe_camera}_{uuid.uuid4().hex}.jpg"
        path = self.upload_dir / folder / filename
        cv2.imwrite(str(path), image)
        return str(path)


pipeline = ANPRPipeline()
