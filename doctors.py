from .db import get_connection
from .utils import read_int, read_nonempty, print_rows, pause

HEADERS = [
    "ID", "Name", "Specialization", "Age", "Gender",
    "Qualification", "Address", "Phone", "Email"
]


def list_doctors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT docid, docname, docspecialization, docage, docgender,
               docqualifications, docaddress, docphone, docemail
        FROM doctor_tbl ORDER BY docid
    """)
    rows = cur.fetchall()
    print_rows(rows, HEADERS)
    cur.close()
    conn.close()
    pause()


def add_doctor():
    data = (
        read_nonempty("Doctor name: "),
        read_nonempty("Specialization: "),
        read_int("Age: ", 0, 120),
        input("Gender: ").strip(),
        input("Qualification: ").strip(),
        input("Address: ").strip(),
        input("Phone: ").strip(),
        input("Email: ").strip(),
    )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO doctor_tbl
        (docname, docspecialization, docage, docgender, docqualifications,
         docaddress, docphone, docemail)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    print(f"Doctor added successfully. ID: {cur.lastrowid}")
    cur.close()
    conn.close()
    pause()


def search_doctor():
    term = input("Enter doctor ID or name: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT docid, docname, docspecialization, docage, docgender,
               docqualifications, docaddress, docphone, docemail
        FROM doctor_tbl
        WHERE docid = %s OR docname LIKE %s
        ORDER BY docid
    """, (int(term) if term.isdigit() else -1, f"%{term}%"))
    rows = cur.fetchall()
    print_rows(rows, HEADERS)
    cur.close()
    conn.close()
    pause()


def update_doctor():
    doctor_id = read_int("Doctor ID: ", 1)
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM doctor_tbl WHERE docid = %s", (doctor_id,))
    doctor = cur.fetchone()

    if not doctor:
        print("Doctor not found.")
        cur.close()
        conn.close()
        pause()
        return

    print("Press Enter to keep the existing value.")
    age_raw = input(f"Age [{doctor['docage']}]: ").strip()
    gender = input(f"Gender [{doctor['docgender']}]: ").strip() or doctor["docgender"]
    qualification = input(f"Qualification [{doctor['docqualifications']}]: ").strip() or doctor["docqualifications"]
    address = input(f"Address [{doctor['docaddress']}]: ").strip() or doctor["docaddress"]
    phone = input(f"Phone [{doctor['docphone']}]: ").strip() or doctor["docphone"]
    email = input(f"Email [{doctor['docemail']}]: ").strip() or doctor["docemail"]

    age = int(age_raw) if age_raw else doctor["docage"]

    cur.execute("""
        UPDATE doctor_tbl
        SET docage=%s, docgender=%s, docqualifications=%s,
            docaddress=%s, docphone=%s, docemail=%s
        WHERE docid=%s
    """, (age, gender, qualification, address, phone, email, doctor_id))
    conn.commit()
    print("Doctor updated successfully.")
    cur.close()
    conn.close()
    pause()


def delete_doctor():
    doctor_id = read_int("Doctor ID to delete: ", 1)
    confirm = input("This also removes related appointments. Continue? (y/n): ").lower()
    if confirm != "y":
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM doctor_tbl WHERE docid = %s", (doctor_id,))
    conn.commit()
    print("Doctor deleted." if cur.rowcount else "Doctor not found.")
    cur.close()
    conn.close()
    pause()


def doctor_menu():
    while True:
        print("""
========== DOCTOR MANAGEMENT ==========
1. Show all doctors
2. Add doctor
3. Modify doctor
4. Search doctor
5. Delete doctor
6. Back
""")
        choice = input("Choice: ").strip()
        try:
            if choice == "1": list_doctors()
            elif choice == "2": add_doctor()
            elif choice == "3": update_doctor()
            elif choice == "4": search_doctor()
            elif choice == "5": delete_doctor()
            elif choice == "6": return
            else: print("Invalid choice.")
        except Exception as exc:
            print(f"Operation failed: {exc}")
            pause()
