"""
src/pages/batch_detail.py
Detailed view of flock lifecycle, mortality, and ventilation openings.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path_template="/batches/<batch_id>", name="Batch Detail")


def layout(batch_id=None):
    return dbc.Container([
        html.H2(f"Batch Details: {batch_id}", className="mb-4"),
        dbc.Card([
            dbc.CardHeader("Batch Specifications & Ventilation Schedule"),
            dbc.CardBody(
                f"Bird count, strain, mortality rate, and opening periods for batch {batch_id}.")
        ])
    ], fluid=True)
