
import sqlite3

DATABASE = "models/mailguard.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    # Create predictions table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_preview TEXT NOT NULL,
            prediction TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check existing table columns
    cursor.execute("PRAGMA table_info(predictions)")

    columns = [
        column[1] for column in cursor.fetchall()
    ]

    # Add analysis_type without deleting existing records
    if "analysis_type" not in columns:

        cursor.execute("""
            ALTER TABLE predictions
            ADD COLUMN analysis_type TEXT
            NOT NULL DEFAULT 'MESSAGE'
        """)

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_table()

    print("MailGuard AI database updated successfully!")
