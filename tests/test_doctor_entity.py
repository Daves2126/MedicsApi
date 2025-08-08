from entities.doctor import Doctor

def test_doctor_creation():
    doctor = Doctor(name="Dr. Smith", specialtyCode="CARD")
    assert doctor.name == "Dr. Smith"
    assert doctor.specialtyCode == "CARD"
    assert doctor.id is None  # Not persisted yet
