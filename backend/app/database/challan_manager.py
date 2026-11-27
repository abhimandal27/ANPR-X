from app.database.db import get_connection


def get_challan_history(registration_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM challans
        WHERE registration_number = ?
        ORDER BY violation_date DESC
    """, (registration_number,))

    records = cursor.fetchall()
    conn.close()

    return [dict(row) for row in records]


def get_challan_summary(registration_number):

    challans = get_challan_history(registration_number)

    total = len(challans)

    pending = [
        c for c in challans
        if c["payment_status"].lower() == "pending"
    ]

    paid = [
        c for c in challans
        if c["payment_status"].lower() == "paid"
    ]

    total_amount = sum(c["amount"] or 0 for c in challans)

    pending_amount = sum(c["amount"] or 0 for c in pending)

    violations = {}

    for challan in challans:
        violation = challan["violation_type"]

        violations[violation] = violations.get(violation, 0) + 1

    return {
        "total_challans": total,
        "paid_challans": len(paid),
        "pending_challans": len(pending),
        "total_fine_amount": total_amount,
        "pending_fine_amount": pending_amount,
        "violations": violations,
        "history": challans
    }