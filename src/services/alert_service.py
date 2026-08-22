"""
src/services/alert_service.py
Evaluates incoming telemetry data against configured global alert thresholds.
"""
from src.models.admin import AlertRule
from src.models.database import SessionLocal


def evaluate_reading(sensor_id: int, temperature: float, humidity: float) -> None:
    """
    Compares current readings against active global alert rules.
    If a threshold is breached for the required duration, an alert state is triggered.
    """
    with SessionLocal() as db:
        # Fetch all active global rules
        active_rules = db.query(AlertRule).filter(
            AlertRule.is_active == True).all()

        for rule in active_rules:
            # TODO: Implement the specific operator logic (>, <, outside_range)
            # TODO: Implement duration_mins tracking to prevent alert flapping
            pass

    return None


def resolve_alert(alert_id: int) -> bool:
    """
    Marks a triggered alert as resolved.
    """
    # TODO: Implement alert resolution logic once the Alert model is fully defined
    return True
