from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Initialize these as None and create them when needed
engine = None
SessionLocal = None
Base = declarative_base()

def get_engine():
    global engine
    if engine is None:
        # Check if we're running tests
        if "PYTEST_CURRENT_TEST" in os.environ:
            # Use in-memory SQLite for testing
            DATABASE_URL = "sqlite:///:memory:"
        else:
            # Use the database URL from environment variables
            from dotenv import load_dotenv
            load_dotenv()
            DATABASE_URL = os.getenv("DATABASE_URL")
        
        engine = create_engine(DATABASE_URL, echo=True)
    return engine

def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return SessionLocal