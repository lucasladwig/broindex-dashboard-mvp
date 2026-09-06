"""
src/pages/sensor_detail.py
Deep dive into a specific sensor's hardware specs and individual telemetry stream.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from src.models.database import SessionLocal
from src.models.sensors import Sensor
from src.models.farm import Shed
from src.components.charts import create_dual_axis_telemetry_chart
from src.services.telemetry_service import get_24h_sensor_telemetry

dash.register_page(
    __name__, path_template="/sensors/<sensor_id>", name="Sensor Details")


def layout(sensor_id=None, **kwargs):
    return dbc.Container([
        dcc.Store(id="current-sensor-id", data=sensor_id),
        # 5-second polling interval
        dcc.Interval(id="sensor-detail-interval",
                     interval=5000, n_intervals=0),

        # Header Section
        dbc.Row(id="sensor-header-container", className="mb-4 mt-2"),

        # Telemetry Chart Section
        dbc.Card([
            dbc.CardHeader(
                html.H5("24-Hour Telemetry Stream", className="mb-0")),
            dbc.CardBody(
                dcc.Graph(id="sensor-telemetry-chart",
                          config={'displayModeBar': False})
            )
        ], className="shadow-sm mb-4")

    ], fluid=True)


@callback(
    Output("sensor-header-container", "children"),
    Output("sensor-telemetry-chart", "figure"),
    Input("sensor-detail-interval", "n_intervals"),
    State("current-sensor-id", "data")
)
def update_sensor_detail(_, sensor_id):
    if not sensor_id:
        return dbc.Col(html.H4("No Sensor ID provided.", className="text-danger")), dash.no_update

    with SessionLocal() as db:
        sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()

        if not sensor:
            return dbc.Col(html.H4("Sensor not found in database.", className="text-danger")), dash.no_update

        # Get the shed name for context
        shed = db.query(Shed).filter(
            Shed.id == sensor.shed_id).first() if sensor.shed_id else None
        shed_name = shed.name if shed else "Unassigned"
        grid_loc = f"(X: {sensor.grid_x}, Y: {sensor.grid_y})" if sensor.grid_x and sensor.grid_y else "N/A"

        # 1. Build Header
        badge_color = "success" if sensor.status.lower() == "active" else "warning"

        header = dbc.Col([
            dbc.Badge(sensor.status.upper(), color=badge_color,
                      className="float-end"),
            html.H2(f"Sensor SEN-{sensor.id:03d}", className="text-primary"),
            html.P([
                html.Strong("Hardware: "), f"{sensor.brand} {sensor.model}",
                html.Span(" | ", className="mx-2 text-muted"),
                html.Strong("MAC: "), html.Code(sensor.mac_address),
                html.Span(" | ", className="mx-2 text-muted"),
                html.Strong("Location: "), f"{shed_name} {grid_loc}"
            ], className="text-muted mb-0")
        ])

        # 2. Fetch Telemetry Data
        df = get_24h_sensor_telemetry(sensor.id)

        # 3. Generate Chart
        fig = create_dual_axis_telemetry_chart(df)

        return header, fig
