from dataclasses import dataclass
from time import monotonic


@dataclass
class TrackMemory:
    plate_number: str
    seen_at: float


class DuplicateTracker:
    def __init__(self, ttl_seconds: int = 45) -> None:
        self.ttl_seconds = ttl_seconds
        self._items: dict[str, TrackMemory] = {}

    def should_record(self, track_id: str, plate_number: str) -> bool:
        now = monotonic()
        expired = [key for key, value in self._items.items() if now - value.seen_at > self.ttl_seconds]
        for key in expired:
            self._items.pop(key, None)
        memory = self._items.get(track_id)
        if memory and memory.plate_number == plate_number:
            return False
        self._items[track_id] = TrackMemory(plate_number=plate_number, seen_at=now)
        return True
