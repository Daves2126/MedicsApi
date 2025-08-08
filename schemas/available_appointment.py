from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AvailableAppointment(BaseModel):
    id: int
    doctor_name: str
    doctor_id: int
    from_time: datetime
    to_time: datetime
    is_reserved: bool
    patient_id: Optional[int] = None

    class Config:
        orm_mode = True
