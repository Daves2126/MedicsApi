
from entities.appointment import Appointment
from datetime import datetime

def test_appointment_creation():
    from_time = datetime(2025, 8, 8, 10, 0, 0)
    to_time = datetime(2025, 8, 8, 11, 0, 0)
    appointment = Appointment(doctor_id=1, from_time=from_time, to_time=to_time)
    assert appointment.doctor_id == 1
    assert appointment.patient_id is None
    assert appointment.id is None  # Not persisted yet

def test_appointment_reserved_status():
    from_time = datetime(2025, 8, 8, 12, 0, 0)
    to_time = datetime(2025, 8, 8, 13, 0, 0)
    appointment = Appointment(doctor_id=2, from_time=from_time, to_time=to_time, is_reserved=True)
    assert appointment.is_reserved is True

def test_appointment_with_patient():
    from_time = datetime(2025, 8, 8, 14, 0, 0)
    to_time = datetime(2025, 8, 8, 15, 0, 0)
    appointment = Appointment(doctor_id=3, from_time=from_time, to_time=to_time, patient_id=5)
    assert appointment.patient_id == 5

def test_appointment_invalid_times():
    from_time = datetime(2025, 8, 8, 16, 0, 0)
    to_time = datetime(2025, 8, 8, 15, 0, 0)
    appointment = Appointment(doctor_id=4, from_time=from_time, to_time=to_time)
    assert appointment.from_time > appointment.to_time or appointment.from_time != appointment.to_time
