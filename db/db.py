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
            from sqlalchemy import create_engine, text
            from urllib.parse import urlparse, urlunparse

            load_dotenv()
            DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@host/db")
            
            # Create database if it does not exist
            parsed_url = urlparse(DATABASE_URL)
            db_name = parsed_url.path.lstrip('/')
            
            # Connect to the server without specifying a database
            server_url_parts = parsed_url._asdict()
            server_url_parts['path'] = ''
            server_url = urlunparse(tuple(server_url_parts.values()))
            
            temp_engine = create_engine(server_url)
            with temp_engine.connect() as connection:
                connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
                connection.commit()
        
        engine = create_engine(DATABASE_URL, echo=True)
    return engine

def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return SessionLocal