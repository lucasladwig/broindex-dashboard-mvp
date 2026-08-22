"""
src/pages/sheds.py
Overview grid of all sheds with CRUD management modals.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/sheds", name="Sheds")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Shed Management"), width=8),
        dbc.Col(dbc.Button("Add New Shed", color="primary",
                className="float-end"), width=4)
    ], className="mb-4"),
    dbc.Row(id="sheds-list-container", children=[
        dbc.Col(dbc.Card(dbc.CardBody(
            "Grid of all active and inactive shed cards.")), width=12)
    ])
], fluid=True)
