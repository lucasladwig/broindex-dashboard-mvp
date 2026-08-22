"""
src/models/database.py
Database connection setup and declarative base.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ensure the data/db directory exists
DB_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "db")
os.makedirs(DB_DIR, exist_ok=True)

# SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'broindex.sqlite3')}"

# Create the SQLAlchemy engine.
# check_same_thread is False to allow access across different Dash threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
