CREATE DATABASE IF NOT EXISTS hmschaitanya;
USE hmschaitanya;

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
);

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
);

CREATE TABLE IF NOT EXISTS appointments_tbl (
    patid INT NOT NULL,
    docid INT NOT NULL,
    appdate DATE NOT NULL,
    apptime TIME NOT NULL,
    comments VARCHAR(255),
    PRIMARY KEY (patid, docid, appdate, apptime),
    FOREIGN KEY (patid) REFERENCES patient_tbl(patid) ON DELETE CASCADE,
    FOREIGN KEY (docid) REFERENCES doctor_tbl(docid) ON DELETE CASCADE
);
