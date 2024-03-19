from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

# Pydantic models for request and response

class Slot(BaseModel):
    id: int
    date: datetime  

class SlotParams(BaseModel):
    start_time: datetime
    end_time: datetime
    slot_interval: timedelta