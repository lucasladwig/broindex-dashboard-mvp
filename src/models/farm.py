"""
src/models/farm.py
Data models for the Farm, Sheds, and Batches.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String, default='America/Sao_Paulo')
    contact_email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sheds = relationship("Shed", back_populates="farm")


class Shed(Base):
    __tablename__ = "sheds"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    name = Column(String, nullable=False)
    grid_rows = Column(Integer, default=1)
    grid_cols = Column(Integer, default=1)
    width_m = Column(Float)
    length_m = Column(Float)
    capacity = Column(Integer)
    status = Column(String, default='active')

    farm = relationship("Farm", back_populates="sheds")
    sensors = relationship("Sensor", back_populates="shed")
    batches = relationship("Batch", back_populates="shed")


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    shed_id = Column(Integer, ForeignKey("sheds.id"))
    batch_number = Column(String, nullable=False)
    bird_strain = Column(String)
    initial_count = Column(Integer, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default='planned')
    first_opening = Column(DateTime(timezone=True), nullable=True)
    second_opening = Column(DateTime(timezone=True), nullable=True)
    third_opening = Column(DateTime(timezone=True), nullable=True)
    fourth_opening = Column(DateTime(timezone=True), nullable=True)
    fifth_opening = Column(DateTime(timezone=True), nullable=True)

    shed = relationship("Shed", back_populates="batches")
