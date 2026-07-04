# Backend

FastAPI backend for vehicle detection, ANPR, alerts, and dashboard APIs.

## Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload
```

The first run creates `database/anpr.db` and a default administrator:

- Email: `admin@example.com`
- Password: `admin123`

