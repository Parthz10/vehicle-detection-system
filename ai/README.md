# AI Pipeline Notes

The backend uses `backend/app/ai/pipeline.py`.

- Vehicle detection: Ultralytics YOLO (`yolov8n.pt` by default).
- Plate region: pragmatic OpenCV crop from the vehicle bounding box for MVP use.
- OCR: PaddleOCR English model.

For higher Nepali plate accuracy, collect plate images from the target region and replace the heuristic plate crop with a dedicated license-plate detector trained on local plates.
