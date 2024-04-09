import mysql.connector
from argparse import ArgumentParser

database = None

def reset_database(name, pw, host="172.17.0.2"):
    global database
    database = {  # Store arguments in a global dictionary
        'host': host,
        'user': 'root',
        'password': pw,
        'database': name
    }

    db = mysql.connector.connect(
        host=host,
        user="root",
        password=pw
    )
    cursor = db.cursor()

    # Drop existing database if it exists
    cursor.execute("DROP DATABASE IF EXISTS {}".format(name))

    cursor.execute("CREATE DATABASE {}".format(name))
    cursor.execute("USE {}".format(name))
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            uuid VARCHAR(36) UNIQUE,
            date DATETIME
        )
    """)

    print("Database '{}' reset successfully!".format(name))

    cursor.close()
    db.close()


if __name__ == "__main__":
    parser = ArgumentParser(description="Reset a MySQL database.")
    parser.add_argument("database_name", help="The name of the database to reset.")
    parser.add_argument("password", help="The password for the database user.")
    parser.add_argument("-H", "--host", help="The host address of the MySQL server (default: localhost)", default="172.17.0.2")
    args = parser.parse_args()

    reset_database(args.database_name, args.password, args.host)
