from pydantic import BaseModel
from datetime import datetime

class UserAppointment(BaseModel):
    id: int
    doctor_name: str
    medical_field: str
    from_time: datetime
    to_time: datetime

    class Config:
        orm_mode = True
