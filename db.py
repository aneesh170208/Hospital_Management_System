import mysql.connector
from mysql.connector import Error
from .config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection(database=True):
    config = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
    if database:
        config["database"] = DB_NAME

    return mysql.connector.connect(**config)


def initialize_database():
    conn = None
    cursor = None
    try:
        conn = get_connection(database=False)
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    conn = get_connection(database=True)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_tbl (
            patid INT AUTO_INCREMENT PRIMARY KEY,
            patname VARCHAR(100) NOT NULL,
            patage INT,
            patgender VARCHAR(20),
            patheight DECIMAL(5,2),
            patweight DECIMAL(5,2),
            patbloodgroup VARCHAR(5),
            patguardianname VARCHAR(100),
            pataddress VARCHAR(255),
            patphone VARCHAR(20),
            patemail VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctor_tbl (
            docid INT AUTO_INCREMENT PRIMARY KEY,
            docname VARCHAR(100) NOT NULL,
            docspecialization VARCHAR(100) NOT NULL,
            docage INT,
            docgender VARCHAR(20),
            docqualifications VARCHAR(150),
            docaddress VARCHAR(255),
            docphone VARCHAR(20),
            docemail VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments_tbl (
            patid INT NOT NULL,
            docid INT NOT NULL,
            appdate DATE NOT NULL,
            apptime TIME NOT NULL,
            comments VARCHAR(255),
            PRIMARY KEY (patid, docid, appdate, apptime),
            CONSTRAINT fk_appointment_patient
                FOREIGN KEY (patid) REFERENCES patient_tbl(patid)
                ON DELETE CASCADE,
            CONSTRAINT fk_appointment_doctor
                FOREIGN KEY (docid) REFERENCES doctor_tbl(docid)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
