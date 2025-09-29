"""
This file handles the connection to our PostgreSQL database.
It creates the database engine, session manager, and provides a function
to get database connections that FastAPI can use.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection URL - reads password from environment variable for security
# Format: postgresql://username:password@host/database_name
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{os.getenv('tpass')}@localhost/twiter"

# Create the database engine - this manages the connection pool
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory - sessions are used to interact with the database
# autocommit=False means we control when changes are saved
# autoflush=False means we control when changes are sent to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our database models (tables)
Base = declarative_base()

def get_db():
    """
    Dependency function that provides database sessions to FastAPI routes.
    This ensures each request gets its own database session and that
    the session is properly closed after the request is done.
    """
    db = SessionLocal()
    try:
        yield db  # Provide the session to the route
    finally:
        db.close()  # Always close the session when done