"""
src/pages/sensors.py
Tabular overview of IoT sensors across all sheds with online/offline indicators.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/sensors", name="Sensors")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Sensor Inventory"), width=8),
        dbc.Col(dbc.Button("Register Sensor", color="primary",
                className="float-end"), width=4)
    ], className="mb-4"),
    dbc.Card(dbc.CardBody("Sensors table placeholder."))
], fluid=True)
