from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from db.db import Base
from sqlalchemy.orm import relationship



class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    from_time = Column('from', DateTime, nullable=False)
    to_time = Column('to', DateTime, nullable=False)
    is_reserved = Column(Boolean, nullable=False, default=False)
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    doctor = relationship('Doctor')
    patient = relationship('User')
