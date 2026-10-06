from datetime import datetime
from .db import get_connection
from .utils import read_int, print_rows, pause


def add_appointment():
    patient_id = read_int("Patient ID: ", 1)
    doctor_id = read_int("Doctor ID: ", 1)
    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (HH:MM): ").strip()
    comments = input("Comments: ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Invalid date/time format.")
        pause()
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM patient_tbl WHERE patid=%s", (patient_id,))
    if not cur.fetchone():
        print("Patient does not exist.")
        cur.close(); conn.close(); pause(); return

    cur.execute("SELECT 1 FROM doctor_tbl WHERE docid=%s", (doctor_id,))
    if not cur.fetchone():
        print("Doctor does not exist.")
        cur.close(); conn.close(); pause(); return

    try:
        cur.execute("""
            INSERT INTO appointments_tbl
            (patid, docid, appdate, apptime, comments)
            VALUES (%s, %s, %s, %s, %s)
        """, (patient_id, doctor_id, date, time, comments))
        conn.commit()
        print("Appointment created successfully.")
    except Exception as exc:
        conn.rollback()
        print(f"Could not create appointment: {exc}")

    cur.close()
    conn.close()
    pause()


def list_appointments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.patid, p.patname, a.docid, d.docname,
               d.docspecialization, a.appdate, a.apptime, a.comments
        FROM appointments_tbl a
        JOIN patient_tbl p ON p.patid = a.patid
        JOIN doctor_tbl d ON d.docid = a.docid
        ORDER BY a.appdate, a.apptime
    """)
    rows = cur.fetchall()
    print_rows(rows, [
        "Patient ID", "Patient", "Doctor ID", "Doctor",
        "Specialization", "Date", "Time", "Comments"
    ])
    cur.close()
    conn.close()
    pause()


def delete_appointment():
    patient_id = read_int("Patient ID: ", 1)
    doctor_id = read_int("Doctor ID: ", 1)
    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (HH:MM): ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM appointments_tbl
        WHERE patid=%s AND docid=%s AND appdate=%s AND apptime=%s
    """, (patient_id, doctor_id, date, time))
    conn.commit()
    print("Appointment deleted." if cur.rowcount else "Appointment not found.")
    cur.close()
    conn.close()
    pause()


def appointment_menu():
    while True:
        print("""
========== APPOINTMENTS ==========
1. Show appointments
2. Add appointment
3. Delete appointment
4. Back
""")
        choice = input("Choice: ").strip()
        try:
            if choice == "1": list_appointments()
            elif choice == "2": add_appointment()
            elif choice == "3": delete_appointment()
            elif choice == "4": return
            else: print("Invalid choice.")
        except Exception as exc:
            print(f"Operation failed: {exc}")
            pause()
