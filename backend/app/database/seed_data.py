from app.database.db import get_connection, initialize_database

vehicles = [
    ("WB06AB1234", "Hyundai", "Creta", "SUV",
     "Demo Owner 01", "2022-06-15", "Active"),

    ("WB12CD5678", "Maruti Suzuki", "Swift", "Hatchback",
     "Demo Owner 02", "2021-03-10", "Active"),

    ("WB26EF9012", "Tata", "Nexon", "SUV",
     "Demo Owner 03", "2023-01-20", "Active"),

    ("WB24GH3456", "Mahindra", "Scorpio", "SUV",
     "Demo Owner 04", "2020-08-12", "Active"),

    ("WB20JK7890", "Honda", "City", "Sedan",
     "Demo Owner 05", "2022-11-05", "Active"),

    ("WB01LM2345", "Royal Enfield", "Classic 350", "Motorcycle",
     "Demo Owner 06", "2021-09-18", "Active"),

    ("WB38NP6789", "Tata", "Punch", "SUV",
     "Demo Owner 07", "2024-02-14", "Active"),

    ("WB16QR1122", "Toyota", "Innova", "MPV",
     "Demo Owner 08", "2019-05-22", "Active"),

    ("WB02ST3344", "Kia", "Seltos", "SUV",
     "Demo Owner 09", "2023-07-11", "Active"),

    ("WB18UV5566", "Maruti Suzuki", "Baleno", "Hatchback",
     "Demo Owner 10", "2022-12-01", "Active"),
]

challans = [
    ("WB06AB1234", "Overspeeding", "NH-16, Kolkata",
     "2025-01-15", 2000, "Pending"),

    ("WB06AB1234", "Red Light Violation", "Kolkata",
     "2025-03-10", 1000, "Paid"),

    ("WB06AB1234", "Overspeeding", "NH-16, Kolkata",
     "2025-05-20", 2000, "Pending"),

    ("WB12CD5678", "Overspeeding", "Howrah",
     "2025-02-18", 1500, "Paid"),

    ("WB24GH3456", "Wrong Side Driving", "Barrackpore",
     "2025-04-12", 1000, "Pending"),

    ("WB20JK7890", "Red Light Violation", "Alipore",
     "2025-06-21", 1000, "Paid"),

    ("WB38NP6789", "Overspeeding", "Asansol",
     "2025-07-05", 2000, "Paid"),
]


def seed_database():

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO vehicles
        (registration_number, manufacturer, model,
         vehicle_type, owner_name, registration_date,
         registration_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, vehicles)

    cursor.executemany("""
        INSERT INTO challans
        (registration_number, violation_type, location,
         violation_date, amount, payment_status)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM challans
            WHERE registration_number = ?
            AND violation_type = ?
            AND violation_date = ?
        )
    """, [
        row + (row[0], row[1], row[3])
        for row in challans
    ])

    conn.commit()
    conn.close()

    print("SAMPLE VEHICLE DATABASE POPULATED!")
    print("Vehicles:", len(vehicles))
    print("Sample challans:", len(challans))


if __name__ == "__main__":
    seed_database()