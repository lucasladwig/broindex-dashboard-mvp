"""
src/pages/overview.py
Main overview dashboard showing active sheds, active alerts, and batch KPIs.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Overview")

layout = dbc.Container([
    html.H2("Farm Overview", className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Batch KPIs"),
            dbc.CardBody(
                html.P("Active batches summary, bird count, and mortality metrics."))
        ]), md=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Active Alerts"),
            dbc.CardBody(html.P("Real-time alert status and warnings."))
        ]), md=8),
    ], className="mb-4"),
    html.H4("Active Sheds", className="mb-3"),
    dbc.Row(id="overview-sheds-grid", children=[
        dbc.Col(dbc.Card([
            dbc.CardBody("Shed grid cards and 24h mini-charts placeholder.")
        ]), md=12)
    ])
], fluid=True)
