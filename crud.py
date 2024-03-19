import sqlite3
from models import Slot
from datetime import datetime

conn = sqlite3.connect('bookings.db')
c = conn.cursor()

def get_bookings():
    c.execute("SELECT * FROM bookings")
    bookings = [{"id": row[0], "date": row[1]} for row in c.fetchall()]
    return bookings

# async def create_booking(booking: Slot):
#     with conn:
#         c.execute("INSERT INTO bookings (date) VALUES (?)", (booking.date,))
#         booking_id = c.lastrowid
#     return {"id": booking_id, **booking.dict()}

async def create_booking(date: datetime):
    with conn:
        c.execute("INSERT INTO bookings (date) VALUES (?)", (date,))
        booking_id = c.lastrowid
    return {"id": booking_id, "date": date}

def get_booking(booking_id: int):
    c.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
    result = c.fetchone()
    if result:
        return {"id": result[0], "date": result[1]}
    else:
        return None

async def update_booking(booking_id: int, date: datetime):
    with conn:
        c.execute("UPDATE bookings SET date=? WHERE id=?", (date, booking_id))
    return {"id": booking_id, "date": date}

def delete_booking(booking_id: int):
    with conn:
        c.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    return {"message": "Booking deleted"}
