import re


def normalize_plate(raw_text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9\u0900-\u097F]+", " ", raw_text).strip()
    return re.sub(r"\s+", " ", cleaned).upper()


def is_valid_plate(plate_number: str) -> bool:
    compact = re.sub(r"\s+", "", plate_number)
    return len(compact) >= 4 and any(char.isdigit() for char in compact)
