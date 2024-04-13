import sqlite3
from models import Slot
from datetime import datetime
from uuid import uuid4  
from database import read_config
import mysql.connector

dbconfig = read_config("dbconfig.ini")
conn = mysql.connector.connect(
    host=dbconfig['database']['host'],
    user="root",
    password=dbconfig['database']['password'],
    database=dbconfig['database']['database_name'],
    consume_results=True
)
c = conn.cursor()


def get_bookings():
    c.execute("SELECT * FROM bookings")
    bookings = [{"uuid": row[1], "date": row[2]} for row in c.fetchall()]
    return bookings

def check_booking_conflict(date: datetime):
    # Check if there is already a booking at the specified date and time
    c.execute("SELECT * FROM bookings WHERE date = %s", (date,))
    existing_booking = c.fetchone()
    return existing_booking is not None

async def create_booking(date: datetime):
    booking_uuid = str(uuid4())
    print(date.minute)
    c.execute("INSERT INTO bookings (uuid, date) VALUES (%s, %s)", (booking_uuid, date,))
    conn.commit()
    return {"uuid": booking_uuid, "date": date}

def get_booking(booking_uuid: str):
    c.execute("SELECT * FROM bookings WHERE uuid=%s", (booking_uuid,))
    result = c.fetchone()
    if result:
        return {"uuid": result[1], "date": result[2]}
    else:
        return None

async def update_booking(booking_uuid: str, date: datetime):
    c.execute("UPDATE bookings SET date=%s WHERE uuid=%s", (date, booking_uuid,))
    conn.commit()
    return {"uuid": booking_uuid, "date": date}

def delete_booking(booking_uuid: str):
    c.execute("DELETE FROM bookings WHERE uuid=%s", (booking_uuid,))
    conn.commit()
    return {"message": "Booking deleted"}
