"""
src/services/crud_service.py
Centralized service for managing the creation, reading, updating, and deleting (CRUD)
of core database entities (Farms, Sheds, Sensors, Batches). Includes data validation.
"""
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.farm import Shed
from src.models.sensors import Sensor


def create_shed(farm_id: int, name: str, grid_rows: int, grid_cols: int,
                width_m: float, length_m: float, capacity: int) -> dict:
    """
    Creates a new shed and returns its ID.
    """
    with SessionLocal() as db:
        new_shed = Shed(
            farm_id=farm_id,
            name=name,
            grid_rows=grid_rows,
            grid_cols=grid_cols,
            width_m=width_m,
            length_m=length_m,
            capacity=capacity
        )
        db.add(new_shed)
        db.commit()
        db.refresh(new_shed)
        return {"id": new_shed.id, "status": "success"}


def assign_sensor_to_shed(sensor_id: int, shed_id: int, target_x: int, target_y: int) -> dict:
    """
    Assigns an existing sensor to a specific coordinate within a shed's grid layout.
    Validates that the target coordinates do not exceed the shed's defined dimensions.
    """
    with SessionLocal() as db:
        shed = db.query(Shed).filter(Shed.id == shed_id).first()
        sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()

        if not shed or not sensor:
            return {"status": "error", "message": "Shed or Sensor not found."}

        # Validation: Check if the target coordinates are within the shed's allowed grid
        if target_x > shed.grid_cols or target_x < 1:
            return {"status": "error", "message": f"X-coordinate {target_x} is out of bounds (Max: {shed.grid_cols})."}

        if target_y > shed.grid_rows or target_y < 1:
            return {"status": "error", "message": f"Y-coordinate {target_y} is out of bounds (Max: {shed.grid_rows})."}

        # Update the sensor's assignment
        sensor.shed_id = shed_id
        sensor.grid_x = target_x
        sensor.grid_y = target_y

        db.commit()
        return {"status": "success", "message": "Sensor assigned successfully."}


def delete_shed(shed_id: int) -> bool:
    """
    Safely deletes a shed.
    """
    # TODO: Implement deletion logic, handling related batches and unassigning sensors.
    pass
