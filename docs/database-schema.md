# Database Schema

SQLite database path: `database/anpr.db`

## users

Stores authenticated users and roles.

- `id`
- `email`
- `full_name`
- `hashed_password`
- `role`: `administrator`, `police_officer`, `viewer`
- `is_active`
- `created_at`

## cameras

Stores webcam, RTSP, uploaded-video, and smartphone camera sources.

- `id`
- `name`
- `source_type`: `webcam`, `rtsp`, `upload`, `smartphone`
- `source_url`
- `location_name`
- `latitude`
- `longitude`
- `is_active`
- `created_at`

## detections

Stores vehicle and plate recognition events.

- `id`
- `plate_number`
- `vehicle_type`
- `timestamp`
- `camera_id`
- `camera_name`
- `latitude`
- `longitude`
- `vehicle_confidence`
- `plate_confidence`
- `ocr_confidence`
- `vehicle_image_path`
- `plate_image_path`
- `track_id`
- `is_blacklisted`

## blacklist_entries

Stores administrator-managed plate watch list entries.

- `id`
- `plate_number`
- `reason`
- `is_active`
- `created_at`
- `created_by_id`

## alerts

Stores alert events created when a detection matches an active blacklist entry.

- `id`
- `detection_id`
- `plate_number`
- `message`
- `created_at`
- `acknowledged`
