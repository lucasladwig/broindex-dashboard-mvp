"""
src/models/sensors.py
Data models for Sensors and Time-Series Telemetry Readings.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    mac_address = Column(String, unique=True, index=True)
    shed_id = Column(Integer, ForeignKey("sheds.id"))
    grid_x = Column(Integer, nullable=False)
    grid_y = Column(Integer, nullable=False)
    firmware_version = Column(String)
    status = Column(String, default='active')
    installed_at = Column(DateTime(timezone=True), server_default=func.now())

    shed = relationship("Shed", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    # Composite Primary Key for time-series optimization
    __table_args__ = (
        PrimaryKeyConstraint('sensor_id', 'recorded_at'),
    )

    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    recorded_at = Column(DateTime(timezone=True),
                         nullable=False, default=func.now())
    temperature_c = Column(Float, nullable=False)
    humidity_rh = Column(Float, nullable=False)
    battery_level = Column(Integer, nullable=True)

    sensor = relationship("Sensor", back_populates="readings")
