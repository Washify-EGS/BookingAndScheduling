from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

# Pydantic models for request and response

class Slot(BaseModel):  
    uuid: str
    date: datetime  

class SlotParams(BaseModel):
    start_date: datetime
    end_date: datetime