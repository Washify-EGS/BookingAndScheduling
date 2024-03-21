import os
import sqlite3


def reset_database():
    # Delete the existing database file
    if os.path.exists('bookings.db'):
        os.remove('bookings.db')
        print("Old database deleted successfully")

    # Create a new database file
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, date TEXT)''')
    conn.commit()
    print("New database created successfully")

reset_database()
