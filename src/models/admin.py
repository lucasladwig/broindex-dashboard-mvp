"""
src/models/admin.py
Data models for Global Alert Rules and Admin Configurations.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from .database import Base


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    metric = Column(String, nullable=False)
    operator = Column(String, nullable=False)
    threshold_min = Column(Float, nullable=True)
    threshold_max = Column(Float, nullable=True)
    duration_mins = Column(Integer, default=0)
    severity = Column(String, default='warning')
    is_active = Column(Boolean, default=True)


class AdminConfig(Base):
    __tablename__ = "admin_configs"

    config_key = Column(String, primary_key=True, index=True)
    config_value = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=True)
