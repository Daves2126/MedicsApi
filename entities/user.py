from sqlalchemy import Column, Integer, String
from db.db import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), nullable=False, unique=True)
