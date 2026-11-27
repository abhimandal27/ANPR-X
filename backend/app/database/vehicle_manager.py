from app.database.db import get_connection
from app.database.challan_manager import get_challan_summary


def get_vehicle_details(registration_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM vehicles
        WHERE registration_number = ?
    """, (registration_number,))

    vehicle = cursor.fetchone()

    conn.close()

    if vehicle is None:
        return None

    vehicle = dict(vehicle)

    challan_data = get_challan_summary(registration_number)

    vehicle["traffic_intelligence"] = challan_data

    return vehicle


def calculate_vehicle_score(challan_data):

    total = challan_data["total_challans"]
    pending = challan_data["pending_challans"]

    # Simple demonstration metric
    score = 100 - (total * 8) - (pending * 5)

    return max(0, min(100, score))


def generate_vehicle_report(registration_number):

    vehicle = get_vehicle_details(registration_number)

    if vehicle is None:
        return {
            "found": False,
            "message": "Vehicle not found in ANPR-X database"
        }

    traffic = vehicle["traffic_intelligence"]

    score = calculate_vehicle_score(traffic)

    vehicle["intelligence_score"] = score

    if score >= 90:
        vehicle["risk_category"] = "Low"
    elif score >= 70:
        vehicle["risk_category"] = "Moderate"
    else:
        vehicle["risk_category"] = "High"

    return {
        "found": True,
        "vehicle": vehicle
    }