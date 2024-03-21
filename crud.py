import sqlite3
from models import Slot
from datetime import datetime
from uuid import uuid4  

conn = sqlite3.connect('bookings.db')
c = conn.cursor()

def get_bookings():
    c.execute("SELECT * FROM bookings")
    bookings = [{"uuid": row[1], "date": row[2]} for row in c.fetchall()]
    return bookings

async def create_booking(date: datetime):
    booking_uuid = str(uuid4())
    with conn:
        c.execute("INSERT INTO bookings (uuid, date) VALUES (?, ?)", (booking_uuid, date,))
    return {"uuid": booking_uuid, "date": date}

def get_booking(booking_uuid: str):
    c.execute("SELECT * FROM bookings WHERE uuid=?", (booking_uuid,))
    result = c.fetchone()
    if result:
        return {"uuid": result[1], "date": result[2]}
    else:
        return None

async def update_booking(booking_uuid: str, date: datetime):
    with conn:
        c.execute("UPDATE bookings SET date=? WHERE uuid=?", (date, booking_uuid))
    return {"uuid": booking_uuid, "date": date}

def delete_booking(booking_uuid: str):
    with conn:
        c.execute("DELETE FROM bookings WHERE uuid=?", (booking_uuid,))
    return {"message": "Booking deleted"}
