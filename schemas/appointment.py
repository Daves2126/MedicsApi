from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentBase(BaseModel):
    doctor_id: int
    from_time: datetime
    to_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    is_reserved: bool
    patient_id: Optional[int] = None

    class Config:
        orm_mode = True
