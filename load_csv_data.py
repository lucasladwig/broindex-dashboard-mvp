"""
load_csv_data.py
Script to parse batch-separated CSV files, auto-register sensors, 
and bulk insert telemetry into the SQLite database.
"""

import os
import glob
import pandas as pd
from sqlalchemy import create_engine
from src.models.database import SessionLocal
from src.models.sensors import Sensor
from src.models.farm import Shed

# Configure your database connection
DB_PATH = "sqlite:///broindex.sqlite3"
RAW_DATA_DIR = "data/raw/csv/"


def process_and_load_data():
    engine = create_engine(DB_PATH)

    # Find all batch folders
    batch_folders = glob.glob(os.path.join(RAW_DATA_DIR, "batch_*"))

    if not batch_folders:
        print(f"No batch folders found in {RAW_DATA_DIR}")
        return

    print(f"Found {len(batch_folders)} batch folders. Starting ingestion...")

    total_rows = 0

    # Open a single SQLAlchemy session to handle sensor registration
    with SessionLocal() as db:
        # Default to Shed 1 for these sensors
        default_shed = db.query(Shed).first()
        if not default_shed:
            print("Error: No sheds found in the database. Please run seed_data.py first.")
            return

        for batch_folder in batch_folders:
            batch_name = os.path.basename(batch_folder)
            csv_files = glob.glob(os.path.join(batch_folder, "*.csv"))

            print(
                f"\n--- Processing {batch_name} ({len(csv_files)} files) ---")

            for file in csv_files:
                # 1. Load the CSV into a Pandas DataFrame
                df = pd.read_csv(file)

                # Standardize column names to lowercase and strip whitespace
                df.columns = df.columns.str.strip().str.lower()

                if df.empty:
                    continue

                # 2. Auto-Register the Sensor
                # Grab the sensor info from the very first row of the CSV
                # Assuming current csv file strucure
                s_id = int(df['sensor'].iloc[0])
                s_col = int(df['linha'].iloc[0])
                s_row = int(df['coluna'].iloc[0])

                # Check if this sensor already exists in the database
                existing_sensor = db.query(Sensor).filter(
                    Sensor.id == s_id).first()
                if not existing_sensor:
                    new_sensor = Sensor(
                        id=s_id,
                        shed_id=default_shed.id,
                        # Mock MAC address
                        mac_address=f"AA:BB:CC:DD:{s_id:02d}",
                        brand="Generic",
                        model="TempHum-v1",
                        grid_x=s_col,
                        grid_y=s_row,
                        status="active"
                    )
                    db.add(new_sensor)
                    db.commit()
                    print(
                        f"Registered new Sensor ID {s_id} at Grid ({s_col}, {s_row})")

                # 3. Process the Timestamps
                df['timestamp'] = pd.to_datetime(
                    df['data'] + ' ' + df['hora'], format='%m/%d/%y %H:%M:%S'
                )

                # 4. Map the columns for the database insertion
                df_insert = pd.DataFrame({
                    'sensor_id': df['sensor'],
                    'timestamp': df['timestamp'],
                    'temperature': df['t'],
                    'humidity': df['ur']
                })

                # 5. Bulk insert into SQLite
                df_insert.to_sql('sensor_readings', con=engine,
                                 if_exists='append', index=False, chunksize=10000)

                total_rows += len(df_insert)
                print(
                    f"  Loaded {len(df_insert):,} rows from {os.path.basename(file)}")

    print(
        f"\nSuccess! Inserted {total_rows:,} total telemetry readings into the database.")


if __name__ == "__main__":
    # Ensure the directory structure exists so you can drop your files in
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    process_and_load_data()
