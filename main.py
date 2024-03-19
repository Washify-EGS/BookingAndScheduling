from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List
from models import Slot, SlotParams
from crud import (
    get_bookings,
    create_booking,
    get_booking,
    update_booking,
    delete_booking,
)
import sqlite3


tags_metadata = [ { "name": "Busy", "description": "Bookings"}, { "name": "Free", "description": "Free slots"} ]

app = FastAPI(openapi_tags=tags_metadata)


conn = sqlite3.connect('bookings.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bookings
             (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT)''')
conn.commit()


@app.get("/busy", tags=["Busy"], response_model=List[Slot])
async def get_bookings_handler():
    return get_bookings()


@app.post("/busy", tags=["Busy"], response_model=Slot, status_code=201)
async def create_booking_handler(date: datetime):
    result = await create_booking(date)
    return result


@app.get("/busy/{booking_id}", tags=["Busy"], response_model=Slot)
async def get_booking_handler(booking_id: int):
    found_booking = get_booking(booking_id)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return found_booking


@app.put("/busy/{booking_id}", tags=["Busy"], response_model=Slot)
async def update_booking_handler(booking_id: int, date: datetime):
    found_booking = get_booking(booking_id)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return await update_booking(booking_id, date)


@app.delete("/busy/{booking_id}", tags=["Busy"])
async def delete_booking_handler(booking_id: int):
    found_booking = get_booking(booking_id)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    del_msg = delete_booking(booking_id)
    return del_msg
    

# TODO

@app.post("/free", tags=["Free"], response_model=List[Slot])
async def get_free_slots(slot_params: SlotParams):
    start_time = slot_params.start_time
    end_time = slot_params.end_time

    # Retrieve booked slots
    booked_slots = get_bookings()

    # Generate all possible slots within the scheduling window
    all_slots = []
    current_slot = start_time
    while current_slot < end_time:
        all_slots.append(current_slot)
        current_slot += slot_params.slot_interval

    # Identify free slots
    free_slots = [slot for slot in all_slots if slot not in booked_slots]

    return free_slots

