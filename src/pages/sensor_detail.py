"""
src/pages/sensor_detail.py
Detailed view for an individual IoT sensor with 24h telemetry trends.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path_template="/sensors/<sensor_id>", name="Sensor Detail")


def layout(sensor_id=None):
    return dbc.Container([
        html.H2(f"Sensor: {sensor_id}", className="mb-4"),
        dbc.Card([
            dbc.CardHeader("Current Telemetry & Status"),
            dbc.CardBody(
                f"Live telemetry and 24-hour reading graph for sensor {sensor_id}.")
        ])
    ], fluid=True)
