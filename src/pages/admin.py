"""
src/pages/admin.py
System administration for farm metadata, global alert rules, and batch defaults.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/admin", name="Admin")

layout = dbc.Container([
    html.H2("Administration & Settings", className="mb-4"),
    dbc.Tabs([
        dbc.Tab(label="Global Settings", children=[
            dbc.Card(dbc.CardBody(
                "Farm info, polling interval, and language toggle."), className="mt-3")
        ]),
        dbc.Tab(label="Alert Rules", children=[
            dbc.Card(dbc.CardBody(
                "Temperature/humidity thresholds and persistence duration."), className="mt-3")
        ]),
        dbc.Tab(label="Batch Defaults", children=[
            dbc.Card(dbc.CardBody(
                "Default target ranges and ventilation opening durations."), className="mt-3")
        ]),
    ])
], fluid=True)
