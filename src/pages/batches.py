"""
src/pages/batches.py
Tabular overview of poultry batches and flock lifecycles.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/batches", name="Batches")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Batch Lifecycle Overview"), width=8),
        dbc.Col(dbc.Button("New Batch", color="primary",
                className="float-end"), width=4)
    ], className="mb-4"),
    dbc.Card(dbc.CardBody("Batches table placeholder."))
], fluid=True)
