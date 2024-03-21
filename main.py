from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import List
from models import Slot, SlotParams
from crud import (
    get_bookings,
    check_booking_conflict,
    create_booking,
    get_booking,
    update_booking,
    delete_booking,
)
import sqlite3


tags_metadata = [   { "name": "Busy", "description": "Bookings"}, 
                    { "name": "Free", "description": "Free slots"},
                    { "name": "Config", "description": "Config"}  ]

app = FastAPI(openapi_tags=tags_metadata)


conn = sqlite3.connect('bookings.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bookings
             (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, date TEXT)''')
                        # devo garantir q o uuid seja UNIQUE?
conn.commit()

# Default slot interval
SLOT_INTERVAL = timedelta(hours=1)

# Slot interval configuration endpoint
@app.post("/config/slot_interval", tags=["Config"])
async def set_slot_interval(slot_interval: timedelta):
    global SLOT_INTERVAL
    SLOT_INTERVAL = slot_interval
    return {"message": "Slot interval updated successfully"}

# Get current slot interval configuration
@app.get("/config/slot_interval", tags=["Config"], response_model=timedelta)
async def get_slot_interval():
    global SLOT_INTERVAL
    return SLOT_INTERVAL


@app.get("/busy", tags=["Busy"], response_model=List[Slot])
async def get_bookings_handler():
    print(SLOT_INTERVAL)
    return get_bookings()


@app.post("/busy", tags=["Busy"], response_model=Slot, status_code=201)
async def create_booking_handler(date: datetime):
    if check_booking_conflict(date):
        raise HTTPException(status_code=409, detail="Booking conflict: There's already a booking at this date and time")
    result = await create_booking(date)
    return result


@app.get("/busy/{booking_uuid}", tags=["Busy"], response_model=Slot)
async def get_booking_handler(booking_uuid: str):
    found_booking = get_booking(booking_uuid)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return found_booking


@app.put("/busy/{booking_id}", tags=["Busy"], response_model=Slot)
async def update_booking_handler(booking_uuid: str, date: datetime):
    found_booking = get_booking(booking_uuid)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return await update_booking(booking_uuid, date)


@app.delete("/busy/{booking_id}", tags=["Busy"])
async def delete_booking_handler(booking_uuid: str):
    found_booking = get_booking(booking_uuid)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    del_msg = delete_booking(booking_uuid)
    return del_msg
    

# TODO

@app.post("/free", tags=["Free"])
async def get_free_slots(slot_params: SlotParams):
    start_date = slot_params.start_date
    end_date = slot_params.end_date

    # Retrieve booked slots
    booked_dates = [datetime.strptime(b["date"], "%Y-%m-%d %H:%M:%S") for b in get_bookings()]

    # Generate all possible slots within the scheduling window
    current_date = start_date
    free_slots = []

    while current_date < end_date:
        if all(current_date != b for b in booked_dates):
            free_slots.append(current_date)
        current_date += SLOT_INTERVAL

    return free_slots