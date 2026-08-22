"""
src/pages/alerts.py
Alerts overview with filtering by severity, date, and resolution status.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/alerts", name="Alerts")

layout = dbc.Container([
    html.H2("System Alerts", className="mb-4"),
    dbc.Card([
        dbc.CardHeader("Active & Historical Alerts"),
        dbc.CardBody("Alert filter controls and status table placeholder.")
    ])
], fluid=True)
