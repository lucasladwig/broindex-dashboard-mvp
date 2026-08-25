"""
seed_data.py
Populates the SQLite database with initial structural entities to facilitate 
UI development and component testing prior to live telemetry ingestion.
"""
from datetime import datetime, timezone
from src.models.database import SessionLocal
from src.models.farm import Farm, Shed, Batch
from src.models.sensors import Sensor
from src.models.admin import AlertRule


def seed_database():
    db = SessionLocal()
    try:
        # Check if database is already seeded to prevent duplication
        if db.query(Farm).first():
            print("Database is already seeded. Skipping.")
            return

        print("Seeding structural data...")

        # 1. Create Default Farm
        farm = Farm(
            name="Sunrise Poultry Farm",
            latitude=-23.5505,
            longitude=-46.6333,
            contact_email="admin@sunrisepoultry.com"
        )
        db.add(farm)
        db.flush()  # Flush to assign an ID to the farm object without committing yet

        # 2. Create Sheds
        shed1 = Shed(
            farm_id=farm.id,
            name="Shed 01 - Broilers",
            grid_rows=5,
            grid_cols=5,
            width_m=12.0,
            length_m=100.0,
            capacity=15000,
            status="active"
        )
        shed2 = Shed(
            farm_id=farm.id,
            name="Shed 02 - Maintenance",
            grid_rows=3,
            grid_cols=10,
            width_m=10.0,
            length_m=80.0,
            capacity=10000,
            status="maintenance"
        )
        db.add_all([shed1, shed2])
        db.flush()

        # 3. Create Sensors and map them to Shed 01's grid
        # sensors = [
        #     Sensor(brand="Sensirion", model="SHT31", mac_address="00:1B:44:11:3A:B7",
        #            shed_id=shed1.id, grid_x=1, grid_y=1, status="active"),
        #     Sensor(brand="Sensirion", model="SHT31", mac_address="00:1B:44:11:3A:B8",
        #            shed_id=shed1.id, grid_x=3, grid_y=3, status="active"),
        #     Sensor(brand="Bosch", model="BME280", mac_address="00:1B:44:11:3A:B9",
        #            shed_id=shed1.id, grid_x=5, grid_y=5, status="active"),
        # ]
        # db.add_all(sensors)

        # 4. Create an Active Batch in Shed 01
        batch = Batch(
            shed_id=shed1.id,
            batch_number="B-2026-08",
            bird_strain="Cobb 500",
            initial_count=14500,
            start_date=datetime.now(timezone.utc),
            status="active"
        )
        db.add(batch)

        # 5. Create Baseline Alert Rules
        rules = [
            AlertRule(name="High Temp Warning", metric="temperature", operator=">",
                      threshold_min=28.0, severity="warning", duration_mins=15),
            AlertRule(name="High Temp Critical", metric="temperature", operator=">",
                      threshold_min=32.0, severity="critical", duration_mins=5),
            AlertRule(name="Low Temp Warning", metric="temperature", operator="<",
                      threshold_max=20.0, severity="warning", duration_mins=15),
            AlertRule(name="High Humidity", metric="humidity", operator=">",
                      threshold_min=75.0, severity="warning", duration_mins=30)
        ]
        db.add_all(rules)

        db.commit()
        print("Database seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
