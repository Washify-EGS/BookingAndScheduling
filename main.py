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

tags_metadata = [   { "name": "Busy", "description": "Bookings"}, 
                    { "name": "Free", "description": "Free slots"},
                    { "name": "Config", "description": "Config"}  ]

app = FastAPI(openapi_tags=tags_metadata)
version = "v1"

# Default slot interval
SLOT_INTERVAL = timedelta(hours=1)

# Get current slot interval configuration
@app.get(f"/{version}/config/slot_interval", tags=["Config"])
async def get_slot_interval():
    global SLOT_INTERVAL
    return {"current slot interval":f"{int(SLOT_INTERVAL.total_seconds()/60)} minutes", "message": "Available slot intervals from 1 minute to 60 minutes(1 hour slots)"}

# Slot interval configuration endpoint
@app.post(f"/{version}/config/slot_interval", tags=["Config"])
async def set_slot_interval(slot_interval: timedelta):
    # min slot -> 1 min ; max slot -> 60 min  
    if (slot_interval.total_seconds() < 60 or slot_interval.total_seconds() > 3600) :
        raise HTTPException(status_code=400, detail=f"Invalid slot interval. Available slot intervals go from 1 minute to 60 minutes(1 hour slots)")
    global SLOT_INTERVAL
    SLOT_INTERVAL = slot_interval
    return {"message": "Slot interval updated successfully"}



@app.get(f"/{version}/busy", tags=["Busy"], response_model=List[Slot])
async def get_bookings_handler():
    return get_bookings()


@app.post(f"/{version}/busy", tags=["Busy"], response_model=Slot, status_code=201)
async def create_booking_handler(date: datetime):
    if (date.minute*60 % SLOT_INTERVAL.total_seconds() != 0 or date.second != 0 or date.microsecond != 0):
        raise HTTPException(status_code=400, detail=f"Invalid booking time. Bookings must be made at intervals of {int(SLOT_INTERVAL.total_seconds() / 60)} minutes.")
    if check_booking_conflict(date):
        raise HTTPException(status_code=409, detail="Booking conflict: There's already a booking at this date and time")
    result = await create_booking(date)
    return result


@app.get(f"/{version}/busy/{{booking_uuid}}", tags=["Busy"], response_model=Slot)
async def get_booking_handler(booking_uuid: str):
    found_booking = get_booking(booking_uuid)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return found_booking


@app.put(f"/{version}/busy/{{booking_uuid}}", tags=["Busy"], response_model=Slot)
async def update_booking_handler(booking_uuid: str, date: datetime):
    found_booking = get_booking(booking_uuid)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    if (date.minute*60 % SLOT_INTERVAL.total_seconds() != 0 or date.second != 0 or date.microsecond != 0):
        raise HTTPException(status_code=400, detail=f"Invalid booking time. Bookings must be made at intervals of {int(SLOT_INTERVAL.total_seconds() / 60)} minutes.")
    if check_booking_conflict(date):
        raise HTTPException(status_code=409, detail="Booking conflict: There's already a booking at this date and time")
    
    return await update_booking(booking_uuid, date)


@app.delete(f"/{version}/busy/{{booking_uuid}}", tags=["Busy"])
async def delete_booking_handler(booking_uuid: str):
    found_booking = get_booking(booking_uuid)
    if found_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    del_msg = delete_booking(booking_uuid)
    return del_msg
    

@app.post(f"/{version}/free", tags=["Free"])
async def get_free_slots(slot_params: SlotParams):
    start_date = slot_params.start_date
    end_date = slot_params.end_date
    if (start_date.minute*60 % SLOT_INTERVAL.total_seconds() != 0 or start_date.second != 0 or start_date.microsecond != 0):
        raise HTTPException(status_code=400, detail=f"Invalid start date. Slots must be made at intervals of {int(SLOT_INTERVAL.total_seconds() / 60)} minutes.")
    
    if (end_date.minute*60 % SLOT_INTERVAL.total_seconds() != 0 or end_date.second != 0 or end_date.microsecond != 0):
        raise HTTPException(status_code=400, detail=f"Invalid end date. Slots must be made at intervals of {int(SLOT_INTERVAL.total_seconds() / 60)} minutes.")
    
    # Retrieve booked slots
    booked_dates = [datetime.strptime(str(b["date"]), "%Y-%m-%d %H:%M:%S") for b in get_bookings()]

    # Generate all possible slots within the scheduling window
    current_date = start_date
    free_slots = []

    while current_date < end_date:
        if all(current_date != b for b in booked_dates):
            free_slots.append(current_date)
        current_date += SLOT_INTERVAL

    return free_slots   