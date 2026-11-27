from app.database.vehicle_manager import generate_vehicle_report

registration_number = "WB06AB1234"

report = generate_vehicle_report(registration_number)

print("\n========== ANPR-X INTELLIGENCE ==========\n")

if report["found"]:

    vehicle = report["vehicle"]
    traffic = vehicle["traffic_intelligence"]

    print("REGISTRATION:", vehicle["registration_number"])
    print("MANUFACTURER:", vehicle["manufacturer"])
    print("MODEL:", vehicle["model"])
    print("VEHICLE TYPE:", vehicle["vehicle_type"])
    print("OWNER:", vehicle["owner_name"])

    print("\n========== CHALLAN SUMMARY ==========")

    print("Total Challans:", traffic["total_challans"])
    print("Paid:", traffic["paid_challans"])
    print("Pending:", traffic["pending_challans"])

    print("Total Fine:", traffic["total_fine_amount"])
    print("Pending Fine:", traffic["pending_fine_amount"])

    print("\n========== VIOLATIONS ==========")

    for violation, count in traffic["violations"].items():
        print(f"{violation}: {count}")

    print("\n========== VEHICLE INTELLIGENCE ==========")

    print("Score:", vehicle["intelligence_score"])
    print("Category:", vehicle["risk_category"])

else:
    print(report["message"])