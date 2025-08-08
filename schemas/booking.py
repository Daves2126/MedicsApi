from pydantic import BaseModel

class BookingRequest(BaseModel):
    doctor_id: int
    appointment_id: int
