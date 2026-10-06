from hospital.db import initialize_database
from hospital.patients import patient_menu
from hospital.doctors import doctor_menu
from hospital.appointments import appointment_menu
from hospital.reports import reports_menu


def main():
    print("=" * 60)
    print("              HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 60)

    try:
        initialize_database()
        print("Database and tables are ready.")
    except Exception as exc:
        print(f"\nDatabase setup failed: {exc}")
        print("Check MySQL is running and verify your .env settings.")
        return

    while True:
        print("""
================ MAIN MENU ================
1. Patient management
2. Doctor management
3. Appointments
4. Reports and charts
5. Quit
============================================
""")
        choice = input("Choice: ").strip()

        try:
            if choice == "1":
                patient_menu()
            elif choice == "2":
                doctor_menu()
            elif choice == "3":
                appointment_menu()
            elif choice == "4":
                reports_menu()
            elif choice == "5":
                print("Thank you for using Hospital Management System.")
                break
            else:
                print("Invalid choice.")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
