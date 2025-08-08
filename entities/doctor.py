from sqlalchemy import Column, Integer, String
from db.db import Base

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialtyCode = Column(String, nullable=False)
