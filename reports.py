import matplotlib.pyplot as plt
from .db import get_connection
from .utils import pause


def patient_measurements_chart():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT patname, patage, patweight, patheight
        FROM patient_tbl ORDER BY patid
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("No patient data available.")
        pause()
        return

    names = [r[0] for r in rows]
    ages = [float(r[1] or 0) for r in rows]
    weights = [float(r[2] or 0) for r in rows]
    heights = [float(r[3] or 0) for r in rows]

    x = list(range(len(names)))
    width = 0.25

    plt.figure(figsize=(11, 6))
    plt.bar([i - width for i in x], ages, width=width, label="Age")
    plt.bar(x, weights, width=width, label="Weight (kg)")
    plt.bar([i + width for i in x], heights, width=width, label="Height (cm)")
    plt.xticks(x, names, rotation=45, ha="right")
    plt.xlabel("Patient")
    plt.ylabel("Measurement")
    plt.title("Patient Measurements")
    plt.legend()
    plt.tight_layout()
    plt.show()


def doctor_specialization_chart():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT docspecialization, COUNT(*)
        FROM doctor_tbl
        GROUP BY docspecialization
        ORDER BY docspecialization
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("No doctor data available.")
        pause()
        return

    labels = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Doctors by Specialization")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def reports_menu():
    while True:
        print("""
========== REPORTS ==========
1. Patient measurements chart
2. Doctor specialization chart
3. Back
""")
        choice = input("Choice: ").strip()
        try:
            if choice == "1": patient_measurements_chart()
            elif choice == "2": doctor_specialization_chart()
            elif choice == "3": return
            else: print("Invalid choice.")
        except Exception as exc:
            print(f"Report failed: {exc}")
            pause()
