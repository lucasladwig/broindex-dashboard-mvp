"""
src/pages/shed_detail.py
Detailed shed view showing sensor grid, dual-axis telemetry charts, and sensor placement mapping.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path_template="/sheds/<shed_id>", name="Shed Detail")


def layout(shed_id=None):
    return dbc.Container([
        html.H2(f"Shed Details: {shed_id}", className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Interactive Sensor Grid"),
                dbc.CardBody(
                    f"Grid sensor placement layout for Shed {shed_id}.")
            ]), md=6),
            dbc.Col(dbc.Card([
                dbc.CardHeader("24-Hour Dual-Axis Environmental Chart"),
                dbc.CardBody(
                    "Plotly dual-axis temperature/humidity time-series placeholder.")
            ]), md=6),
        ], className="mb-4"),
        dbc.Button("Edit Sensor Assignments",
                   color="secondary", className="mt-2")
    ], fluid=True)
