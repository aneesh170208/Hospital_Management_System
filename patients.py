from .db import get_connection
from .utils import read_int, read_float, read_nonempty, print_rows, pause


HEADERS = [
    "ID", "Name", "Age", "Gender", "Height", "Weight",
    "Blood", "Guardian", "Address", "Phone", "Email"
]


def list_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT patid, patname, patage, patgender, patheight, patweight,
               patbloodgroup, patguardianname, pataddress, patphone, patemail
        FROM patient_tbl ORDER BY patid
    """)
    rows = cur.fetchall()
    print_rows(rows, HEADERS)
    cur.close()
    conn.close()
    pause()


def add_patient():
    data = (
        read_nonempty("Patient name: "),
        read_int("Age: ", 0, 150),
        input("Gender: ").strip(),
        read_float("Height (cm): ", 0),
        read_float("Weight (kg): ", 0),
        input("Blood group: ").strip(),
        input("Guardian name: ").strip(),
        input("Address: ").strip(),
        input("Phone: ").strip(),
        input("Email: ").strip(),
    )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO patient_tbl
        (patname, patage, patgender, patheight, patweight, patbloodgroup,
         patguardianname, pataddress, patphone, patemail)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    print(f"Patient added successfully. ID: {cur.lastrowid}")
    cur.close()
    conn.close()
    pause()


def find_patient():
    term = input("Enter patient ID or name: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT patid, patname, patage, patgender, patheight, patweight,
               patbloodgroup, patguardianname, pataddress, patphone, patemail
        FROM patient_tbl
        WHERE patid = %s OR patname LIKE %s
        ORDER BY patid
    """, (int(term) if term.isdigit() else -1, f"%{term}%"))
    rows = cur.fetchall()
    print_rows(rows, HEADERS)
    cur.close()
    conn.close()
    pause()


def update_patient():
    patient_id = read_int("Patient ID: ", 1)
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM patient_tbl WHERE patid = %s", (patient_id,))
    patient = cur.fetchone()

    if not patient:
        print("Patient not found.")
        cur.close()
        conn.close()
        pause()
        return

    print("Press Enter to keep the existing value.")
    name = input(f"Name [{patient['patname']}]: ").strip() or patient["patname"]
    age_raw = input(f"Age [{patient['patage']}]: ").strip()
    gender = input(f"Gender [{patient['patgender']}]: ").strip() or patient["patgender"]
    height_raw = input(f"Height [{patient['patheight']}]: ").strip()
    weight_raw = input(f"Weight [{patient['patweight']}]: ").strip()
    blood = input(f"Blood group [{patient['patbloodgroup']}]: ").strip() or patient["patbloodgroup"]
    guardian = input(f"Guardian [{patient['patguardianname']}]: ").strip() or patient["patguardianname"]
    address = input(f"Address [{patient['pataddress']}]: ").strip() or patient["pataddress"]
    phone = input(f"Phone [{patient['patphone']}]: ").strip() or patient["patphone"]
    email = input(f"Email [{patient['patemail']}]: ").strip() or patient["patemail"]

    age = int(age_raw) if age_raw else patient["patage"]
    height = float(height_raw) if height_raw else patient["patheight"]
    weight = float(weight_raw) if weight_raw else patient["patweight"]

    cur.execute("""
        UPDATE patient_tbl
        SET patname=%s, patage=%s, patgender=%s, patheight=%s, patweight=%s,
            patbloodgroup=%s, patguardianname=%s, pataddress=%s,
            patphone=%s, patemail=%s
        WHERE patid=%s
    """, (name, age, gender, height, weight, blood, guardian,
          address, phone, email, patient_id))
    conn.commit()
    print("Patient updated successfully.")
    cur.close()
    conn.close()
    pause()


def delete_patient():
    patient_id = read_int("Patient ID to delete: ", 1)
    confirm = input("This also removes related appointments. Continue? (y/n): ").lower()
    if confirm != "y":
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patient_tbl WHERE patid = %s", (patient_id,))
    conn.commit()
    print("Patient deleted." if cur.rowcount else "Patient not found.")
    cur.close()
    conn.close()
    pause()


def patient_menu():
    while True:
        print("""
========== PATIENT MANAGEMENT ==========
1. Show all patients
2. Add patient
3. Modify patient
4. Search patient
5. Delete patient
6. Back
""")
        choice = input("Choice: ").strip()
        try:
            if choice == "1": list_patients()
            elif choice == "2": add_patient()
            elif choice == "3": update_patient()
            elif choice == "4": find_patient()
            elif choice == "5": delete_patient()
            elif choice == "6": return
            else: print("Invalid choice.")
        except Exception as exc:
            print(f"Operation failed: {exc}")
            pause()
