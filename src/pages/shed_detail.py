"""
src/pages/shed_detail.py
Detailed view of a single shed, featuring the interactive sensor grid and telemetry charts.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from src.models.database import SessionLocal
from src.models.farm import Shed
from src.models.sensors import Sensor
from src.components.shed_grid import create_sensor_grid
from src.components.charts import create_dual_axis_telemetry_chart
from src.services.telemetry_service import get_24h_sensor_telemetry

# Register page with a dynamic path variable for the shed ID
dash.register_page(
    __name__, path_template="/sheds/<shed_id>", name="Shed Details")


def layout(shed_id=None, **kwargs):
    """
    Layout function accepts path variables dynamically.
    """
    return dbc.Container([
        dcc.Store(id="current-shed-id", data=shed_id),
        dcc.Interval(id="shed-detail-interval", interval=5000, n_intervals=0),

        # Header Section
        dbc.Row(id="shed-header-container", className="mb-4 mt-2"),

        # Grid Section
        dbc.Card([
            dbc.CardHeader(html.H5("Sensor Floor Plan", className="mb-0")),
            dbc.CardBody(id="shed-grid-container",
                         children=dbc.Spinner(color="primary"))
        ], className="shadow-sm mb-4"),

        # Charts Section
        dbc.Card([
            dbc.CardHeader(html.H5("24-Hour Telemetry", className="mb-0")),
            dbc.CardBody(
                dcc.Graph(id="shed-telemetry-chart",
                          config={'displayModeBar': False})
            )
        ], className="shadow-sm")

    ], fluid=True)


@callback(
    Output("shed-header-container", "children"),
    Output("shed-grid-container", "children"),
    Input("shed-detail-interval", "n_intervals"),
    State("current-shed-id", "data")
)
def update_shed_detail(n, shed_id):
    """
    Fetches the specific shed's details and maps assigned sensors to the visual grid.
    """
    if not shed_id:
        return dbc.Col(html.H4("No Shed ID provided.", className="text-danger")), html.Div()

    with SessionLocal() as db:
        shed = db.query(Shed).filter(Shed.id == shed_id).first()

        if not shed:
            return dbc.Col(html.H4("Shed not found in database.", className="text-danger")), html.Div()

        header = dbc.Col([
            html.H2(shed.name, className="text-primary"),
            html.P([
                html.Strong(
                    "Dimensions: "), f"{shed.width_m}m x {shed.length_m}m",
                html.Span(" | ", className="mx-2 text-muted"),
                html.Strong(
                    "Grid Layout: "), f"{shed.grid_cols} cols x {shed.grid_rows} rows",
                html.Span(" | ", className="mx-2 text-muted"),
                html.Strong("Max Capacity: "), f"{shed.capacity:,} birds"
            ], className="text-muted mb-0")
        ])

        sensors = db.query(Sensor).filter(Sensor.shed_id == shed_id).all()

        assigned_sensors = {}
        for s in sensors:
            assigned_sensors[(s.grid_x, s.grid_y)] = {
                "id": s.id,
                "temp": "--",
                "humidity": "--"
            }

        grid_ui = create_sensor_grid(
            rows=shed.grid_rows,
            cols=shed.grid_cols,
            assigned_sensors=assigned_sensors
        )

        return header, grid_ui


@callback(
    Output("shed-telemetry-chart", "figure"),
    Input("shed-detail-interval", "n_intervals"),
    State("current-shed-id", "data")
)
def update_telemetry_chart(_, shed_id):
    """
    Fetches telemetry data and generates the Plotly chart.
    For now, it grabs the first available sensor in the shed to display.
    """
    if not shed_id:
        return dash.no_update

    with SessionLocal() as db:
        # Grab the first sensor in this shed as a baseline reference
        sensor = db.query(Sensor).filter(Sensor.shed_id == shed_id).first()

    if not sensor:
        # No sensors assigned, return empty chart
        return create_dual_axis_telemetry_chart(pd.DataFrame())

    # Fetch the Pandas DataFrame via the telemetry service
    df = get_24h_sensor_telemetry(sensor.id)

    # Generate and return the Plotly figure
    return create_dual_axis_telemetry_chart(df)
