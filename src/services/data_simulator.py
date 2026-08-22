"""
src/services/data_simulator.py
Service for simulating the IoT data pipeline by reading telemetry from local CSV files
and writing it to the database to mimic real-time MQTT/HTTP payloads.
"""

import os
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models.sensors import SensorReading
from src.models.database import SessionLocal

# Define where the CSV files are located
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(__file__))), "data", "simulated_csv")


def get_latest_telemetry(csv_filename: str) -> dict:
    """
    Reads the designated CSV file and returns the most recent telemetry row.
    Assumes the CSV has columns: timestamp, temperature_c, humidity_rh, battery_level.
    """
    file_path = os.path.join(DATA_DIR, csv_filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Telemetry file {file_path} not found.")

    # Read only the last row to simulate fetching a real-time data point
    df = pd.read_csv(file_path)
    if df.empty:
        return None

    latest_record = df.iloc[-1]

    return {
        "temperature_c": float(latest_record.get("temperature_c", 0.0)),
        "humidity_rh": float(latest_record.get("humidity_rh", 0.0)),
        "battery_level": int(latest_record.get("battery_level", 100))
    }


def process_sensor_payload(sensor_id: int, csv_filename: str):
    """
    Ingests the latest telemetry from the CSV and commits it to the database.
    """
    try:
        telemetry = get_latest_telemetry(csv_filename)

        if not telemetry:
            return False

        with SessionLocal() as db:
            new_reading = SensorReading(
                sensor_id=sensor_id,
                recorded_at=datetime.now(timezone.utc),
                temperature_c=telemetry["temperature_c"],
                humidity_rh=telemetry["humidity_rh"],
                battery_level=telemetry["battery_level"]
            )
            db.add(new_reading)
            db.commit()

        return True

    except Exception as e:
        print(f"Error processing payload for sensor {sensor_id}: {e}")
        return False
