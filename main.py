from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import extract
from db.db import SessionLocal, engine, Base
from entities.doctor import Doctor
from entities.appointment import Appointment
from entities.user import User
import schemas.doctor as doctor_schema
import schemas.booking as booking_schema
import schemas.user_appointment as user_appointment_schema
import schemas.appointment as appointment_schema
import schemas.available_appointment as available_appointment_schema
from typing import List
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)


def populate_db():
    db = SessionLocal()
    try:
        if db.query(Doctor).count() == 0:
            doctors_data = [
                {"name": "Dr. House", "specialtyCode": "CARD"},
                {"name": "Dr. Strange", "specialtyCode": "NEUR"},
                {"name": "Dr. Arizona Robbins", "specialtyCode": "PED"},
                {"name": "Dr. Miranda Bailey", "specialtyCode": "GMED"},
                {"name": "Dr. Mark Sloan", "specialtyCode": "DER"},
                {"name": "Dr. Amelia Shepherd", "specialtyCode": "PNEU"},
                {"name": "Dr. Owen Hunt", "specialtyCode": "ORTH"},
                {"name": "Dr. Izzie Stevens", "specialtyCode": "ONC"},
                {"name": "Dr. April Kepner", "specialtyCode": "OBS"},
                {"name": "Dr. Tae Takemi", "specialtyCode": "PSY"},
                {"name": "Dr. Daedalus Yumeno", "specialtyCode": "ENDO"},
            ]
            doctors = [Doctor(**data) for data in doctors_data]
            db.add_all(doctors)
            db.commit()

            for doctor in db.query(Doctor).all():
                for i in range(5):
                    start_time = datetime.now() + timedelta(days=i + 1, hours=9 + i)
                    end_time = start_time + timedelta(hours=1)
                    appointment = Appointment(
                        doctor_id=doctor.id,
                        from_time=start_time,
                        to_time=end_time,
                        is_reserved=False,
                    )
                    db.add(appointment)
            db.commit()

    finally:
        db.close()


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    populate_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/doctors/", response_model=List[doctor_schema.Doctor])
def get_doctors(specialtyCode: str = None, db: Session = Depends(get_db)):
    query = db.query(Doctor)
    if specialtyCode:
        query = query.filter(Doctor.specialtyCode == specialtyCode)
    doctors = query.all()
    return doctors


@app.post("/appointments/book/")
def book_appointment(
    booking: booking_schema.BookingRequest,
    user_email: str = Header(...),
    db: Session = Depends(get_db),
):
    print(f"Booking request: {booking}")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        user = User(email=user_email)
        db.add(user)
        db.commit()
        db.refresh(user)

    appointment = (
        db.query(Appointment).filter(Appointment.id == booking.appointment_id).first()
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.doctor_id != booking.doctor_id:
        raise HTTPException(
            status_code=400,
            detail="Appointment does not belong to the specified doctor",
        )

    if appointment.is_reserved:
        raise HTTPException(status_code=400, detail="Appointment is already reserved")

    appointment.patient_id = user.id
    appointment.is_reserved = True
    db.commit()

    return {"message": "Appointment booked successfully"}


@app.get(
    "/appointments/my-appointments/",
    response_model=List[user_appointment_schema.UserAppointment],
)
def get_my_appointments(
    user_email: str = Header(...), month: int = None, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = db.query(Appointment).filter(Appointment.patient_id == user.id)

    if month:
        query = query.filter(extract("month", Appointment.from_time) == month)

    appointments = (
        query.join(Doctor)
        .with_entities(
            Appointment.id.label("id"),
            Doctor.name.label("doctor_name"),
            Doctor.specialtyCode.label("medical_field"),
            Appointment.from_time,
            Appointment.to_time,
        )
        .all()
    )

    return appointments


@app.get(
    "/appointments/available/", response_model=List[appointment_schema.Appointment]
)
def get_available_appointments(
    doctor_id: int, month: int = None, db: Session = Depends(get_db)
):
    if month is None:
        month = datetime.now().month

    query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.is_reserved == False,
        extract("month", Appointment.from_time) == month,
    )

    appointments = query.all()
    return appointments


@app.get(
    "/appointments/available_by_specialty/",
    response_model=List[available_appointment_schema.AvailableAppointment],
)
def get_available_appointments_by_specialty(
    specialtyCode: str, month: int = None, db: Session = Depends(get_db)
):
    if month is None:
        month = datetime.now().month

    query = (
        db.query(Appointment)
        .join(Doctor)
        .filter(
            Doctor.specialtyCode == specialtyCode,
            Appointment.is_reserved == False,
            extract("month", Appointment.from_time) == month,
        )
        .with_entities(
            Appointment.id,
            Doctor.name.label("doctor_name"),
            Doctor.id.label("doctor_id"),
            Appointment.from_time,
            Appointment.to_time,
            Appointment.is_reserved,
            Appointment.patient_id,
        )
    )

    appointments = query.all()
    return appointments


@app.delete("/appointments/{appointment_id}")
def cancel_appointment(
    appointment_id: int, user_email: str = Header(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.patient_id != user.id:
        raise HTTPException(
            status_code=403, detail="User is not authorized to cancel this appointment"
        )

    appointment.patient_id = None
    appointment.is_reserved = False
    db.commit()

    return {"message": "Appointment canceled successfully"}
