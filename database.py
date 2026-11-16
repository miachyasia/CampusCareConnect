import sqlite3

# Connect to the CampusCare Connect database
def get_db_connection():
    connection = sqlite3.connect("campuscare.db")
    connection.row_factory = sqlite3.Row
    return connection


# Create the student accounts table
def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()