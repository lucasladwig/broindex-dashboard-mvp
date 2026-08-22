"""
src/services/telemetry_service.py
Handles data extraction and aggregation for dashboard visualizations.
Converts raw SQLite time-series data into Pandas DataFrames for Plotly charts.
"""
import pandas as pd
from datetime import datetime, timedelta, timezone
from src.models.database import engine


def get_24h_sensor_telemetry(sensor_id: int) -> pd.DataFrame:
    """
    Retrieves the last 24 hours of temperature and humidity readings for a specific sensor.
    Returns a Pandas DataFrame optimized for Plotly dual-axis charts.
    """
    # Calculate the cutoff time for the last 24 hours
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)

    # We use raw SQL with pandas read_sql for efficient time-series extraction
    query = f"""
        SELECT recorded_at, temperature_c, humidity_rh 
        FROM sensor_readings 
        WHERE sensor_id = {sensor_id} AND recorded_at >= '{cutoff_time.isoformat()}'
        ORDER BY recorded_at ASC
    """

    try:
        # Load the data directly into a DataFrame using the SQLAlchemy engine
        df = pd.read_sql(query, engine)

        if not df.empty:
            # Ensure the timestamp is treated as a proper datetime object for plotting
            df['recorded_at'] = pd.to_datetime(df['recorded_at'])

        return df
    except Exception as e:
        print(f"Error fetching telemetry for sensor {sensor_id}: {e}")
        # Return an empty DataFrame so the UI doesn't crash on failure
        return pd.DataFrame()


def get_shed_average_telemetry(shed_id: int) -> pd.DataFrame:
    """
    Calculates the aggregated average temperature and humidity across all 
    sensors assigned to a specific shed over the last 24 hours.
    Used for the mini-graphs on the Overview page.
    """
    # TODO: Implement the join query between sheds, sensors, and sensor_readings
    # to group by time intervals (e.g., hourly averages) and return the aggregated DataFrame.
    pass
