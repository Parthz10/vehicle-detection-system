# AI Vehicle Detection & ANPR System

FastAPI + React + OpenCV + YOLO + PaddleOCR project for vehicle detection, license plate recognition, storage, search, alerts, and dashboard monitoring. It runs directly on Ubuntu or Windows using Python virtual environments. Docker is not required.

## Project Structure

```text
backend/     FastAPI app, database models, APIs, services, AI pipeline
frontend/    React + TypeScript + Tailwind dashboard
ai/          AI pipeline notes
database/    SQLite database location
uploads/     Saved vehicle, plate, and video files
models/      Optional custom YOLO/license plate model files
docs/        Schema and setup documentation
tests/       Shared test location
```

## Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

Default administrator:

- Email: `admin@example.com`
- Password: `admin123`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Main APIs

- `POST /api/auth/login`
- `GET /api/cameras`
- `POST /api/cameras`
- `GET /api/detections`
- `POST /api/detections`
- `GET /api/detections/stats`
- `GET /api/alerts`
- `PATCH /api/alerts/{id}/ack`
- `GET /api/blacklist`
- `POST /api/blacklist`
- `GET /api/streams/{camera_id}/mjpeg`
- `POST /api/streams/upload-video`
- `POST /api/streams/upload-frame`

## Camera Sources

- Webcam: create a camera with `source_type=webcam` and `source_url=0`.
- IP camera: create a camera with `source_type=rtsp` and the RTSP URL.
- Uploaded video: use the dashboard/API upload endpoint.
- Smartphone: scan the QR code from the dashboard, open the phone camera page, and send frames.

Browser camera access requires HTTPS on real phones unless testing on localhost. For LAN testing, run Vite and FastAPI behind a trusted HTTPS tunnel or local certificate.

## AI Notes

The default YOLO model is `yolov8n.pt`. Ultralytics downloads it on first use if it is not present. Plate recognition uses a practical MVP crop from the detected vehicle and PaddleOCR. For production-level Nepali ANPR, add a dedicated license plate detector and train or fine-tune OCR with local plate images.

## Tests

```bash
pytest
```

## Scalability Path

The app is intentionally separated into models, schemas, routes, services, and AI inference modules. Later upgrades can swap SQLite for PostgreSQL, move stream processing to workers, add Docker, and deploy multiple camera processors without rewriting the API contract.
