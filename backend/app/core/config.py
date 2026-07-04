from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "ANPR Vehicle Detection System"
    secret_key: str = "change-this-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    database_url: str = f"sqlite:///{PROJECT_ROOT / 'database' / 'anpr.db'}"
    upload_dir: Path = PROJECT_ROOT / "uploads"
    vehicle_confidence_threshold: float = 0.35
    plate_confidence_threshold: float = 0.45
    yolo_model_path: str = "yolov8n.pt"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
