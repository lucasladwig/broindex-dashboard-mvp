"""
init_db.py
Script to initialize the SQLite database and create all tables.
"""
from src.models.database import engine, Base
from src.models import farm, sensors, admin

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
