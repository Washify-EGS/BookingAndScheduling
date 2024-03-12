from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "Busy",
        "description": "Bookings",
    },
    {
        "name": "Free",
        "description": "Free slots",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

# Define Pydantic models for request and response
class Booking(BaseModel):
    id: Optional[int] = None
    date: str

class Slot(BaseModel):
    id: Optional[int] = None
    date: str   

# Dummy data for illustration purposes
bookings_db = []
slots_db = []

# Define FastAPI routes
@app.get("/busy", tags=["Busy"], response_model=List[Booking])
async def get_bookings():
    return bookings_db

@app.post("/busy", tags=["Busy"], response_model=Booking, status_code=201)
async def create_booking(booking: Booking):
    bookings_db.append(booking)
    return booking

@app.get("/busy/{booking_id}", tags=["Busy"], response_model=List[Booking])
async def get_booking(booking_id: int):
    booking = next((b for b in bookings_db if b["id"] == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return [booking]

@app.put("/busy/{booking_id}", tags=["Busy"], response_model=Booking)
async def update_booking(booking_id: int, booking: Booking):
    # Implementation to update the booking
    # ...

    # Return the updated booking
    return booking

@app.delete("/busy/{booking_id}", tags=["Busy"], response_model=Booking)
async def delete_booking(booking_id: int):
    booking = next((b for b in bookings_db if b["id"] == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    bookings_db.remove(booking)
    return booking

@app.get("/free", tags=["Free"], response_model=List[Slot])
async def get_free_slots():
    return slots_db

# do i need this endpoint?
# @app.delete("/free/{slot_id}", tags=["Free"], response_model=Slot)
# async def delete_free_slot(slot_id: int):
#     slot = next((s for s in slots_db if s["id"] == slot_id), None)
#     if not slot:
#         raise HTTPException(status_code=404, detail="Slot not found")
    
#     slots_db.remove(slot)
#     return slot
