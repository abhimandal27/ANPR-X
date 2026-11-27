import re

# West Bengal RTO code reference
WB_RTO_CODES = {
    "01": "Kolkata - PVD",
    "02": "Kolkata - PVD",
    "03": "Kolkata - PVD",
    "04": "Kolkata - PVD",
    "06": "Kolkata - PVD",
    "12": "Howrah",
    "16": "Hooghly",
    "18": "Hooghly",
    "20": "Alipore",
    "24": "Barrackpore",
    "26": "Barasat",
    "38": "Asansol",
}

def validate_plate(plate_number):

    # Remove spaces and special characters
    cleaned = re.sub(r"[^A-Z0-9]", "", plate_number.upper())

    # Expected WB registration format
    pattern = r"^WB(\d{2})([A-Z]{1,3})(\d{1,4})$"

    match = re.match(pattern, cleaned)

    if not match:
        return {
            "original": plate_number,
            "cleaned": cleaned,
            "state": "West Bengal",
            "valid_format": False,
            "rto": "Unknown",
            "message": "Invalid registration format"
        }

    rto_code = match.group(1)

    rto_name = WB_RTO_CODES.get(rto_code)

    return {
        "original": plate_number,
        "cleaned": cleaned,
        "state": "West Bengal",
        "rto_code": rto_code,
        "rto": rto_name or "Unmapped RTO code",
        "valid_format": rto_name is not None,
        "message": (
            "Valid-looking WB registration format"
            if rto_name else
            "Format recognized, but RTO code not mapped"
        )
    }


if __name__ == "__main__":

    test_plates = [
        "WB 06 AB 1234",
        "WB12CD5678",
        "MH04ET1006",
        "WB99AB1234",
        "WB06ABC123"
    ]

    for plate in test_plates:
        print(validate_plate(plate))