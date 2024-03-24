import mysql.connector

def reset_database():
    db = mysql.connector.connect(
        host="172.17.0.2",
        user="root",
        password="password"
    )

    cursor = db.cursor()

    # Drop existing database if it exists
    cursor.execute("DROP DATABASE IF EXISTS testdb")

    # Create new database
    cursor.execute("CREATE DATABASE testdb")

    # Use the new database
    cursor.execute("USE testdb")

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            uuid VARCHAR(36) UNIQUE,
            date DATETIME
        )
    """)

    print("Database reset successfully")

    cursor.close()
    db.close()

if __name__ == "__main__":
    reset_database()
