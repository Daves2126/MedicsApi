from sqlalchemy import Column, Integer, String
from db.db import Base

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    specialtyCode = Column(String(256), nullable=False)
