# Hospital Management System

A Python + MySQL command-line Hospital Management System based on the original school project, rebuilt into a cleaner and safer GitHub-ready implementation.

## Features

- Patient management
  - Add
  - View
  - Search
  - Modify
  - Delete
- Doctor management
  - Add
  - View
  - Search
  - Modify
  - Delete
- Appointment management
- Patient measurement bar chart
- Doctor specialization pie chart
- Automatic database/table initialization
- MySQL credentials stored in `.env` instead of source code

## Tech Stack

- Python
- MySQL
- mysql-connector-python
- Matplotlib
- python-dotenv

## Requirements

- Python 3.9+
- MySQL Server
- MySQL user with permission to create/use the database

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd hospital-management-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Copy `.env.example` to `.env` and edit the password:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=hmschaitanya
```

Do NOT commit `.env`.

### 5. Run

```bash
python main.py
```

The application automatically creates the database and tables if they do not already exist.

## Project Structure

```text
hospital-management-system/
├── hospital/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── utils.py
│   ├── patients.py
│   ├── doctors.py
│   ├── appointments.py
│   └── reports.py
├── sql/
│   └── schema.sql
├── screenshots/
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Security Note

The original project contained a MySQL password directly inside Python source code. This version removes that practice and reads credentials from environment variables.

## Original Project Context

The project was originally developed as a Python + SQL Hospital Management System for managing patient and doctor information, including add, update, delete and view operations. The rebuilt version keeps that core idea while making the implementation easier to maintain and publish.

## License

You may add a license appropriate to your intended use before publishing.
