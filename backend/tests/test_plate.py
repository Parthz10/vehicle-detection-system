from app.services.plate import is_valid_plate, normalize_plate


def test_normalize_plate_keeps_devanagari_and_ascii() -> None:
    assert normalize_plate(" ba-2-pa 1234 ") == "BA 2 PA 1234"
    assert normalize_plate("बा २ प १२३४") == "बा २ प १२३४"


def test_plate_validation_requires_digit_and_length() -> None:
    assert is_valid_plate("BA 2 PA 1234")
    assert not is_valid_plate("POLICE")
