"""
src/pages/sheds.py
Overview grid of all sheds with CRUD management options.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.farm import Shed

dash.register_page(__name__, path="/sheds", name="Sheds")

layout = dbc.Container([
    # Interval to auto-refresh the sheds list
    dcc.Interval(id="sheds-interval", interval=5000, n_intervals=0),

    dbc.Row([
        dbc.Col(html.H2("Shed Management"), width=8),
        dbc.Col(dbc.Button("Add New Shed", id="btn-add-shed",
                color="primary", className="float-end"), width=4)
    ], className="mb-4"),

    dbc.Row(id="sheds-list-container", children=dbc.Spinner(color="primary"))
], fluid=True)


@callback(
    Output("sheds-list-container", "children"),
    Input("sheds-interval", "n_intervals")
)
def update_sheds_list(n):
    """
    Queries the database for all sheds and generates a grid of management cards.
    """
    with SessionLocal() as db:
        sheds = db.query(Shed).all()

        if not sheds:
            return [dbc.Col(html.P("No sheds found in the database."), width=12)]

        shed_cards = []
        for shed in sheds:
            # Determine badge color based on shed status
            badge_color = "success" if shed.status.lower() == "active" else "secondary"

            card = dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.H5(shed.name, className="d-inline-block mb-0 mt-1"),
                    dbc.Badge(shed.status.upper(), color=badge_color,
                              className="float-end")
                ]),
                dbc.CardBody([
                    html.P([html.Strong("Capacity: "),
                           f"{shed.capacity:,} birds"], className="mb-1"),
                    html.P([html.Strong("Dimensions: "),
                           f"{shed.width_m}m x {shed.length_m}m"], className="mb-1"),
                    html.P([html.Strong(
                        "Grid Layout: "), f"{shed.grid_cols} columns x {shed.grid_rows} rows"], className="mb-3"),

                    # Management Buttons
                    html.Div([
                        dbc.Button(
                            "View Map", href=f"/sheds/{shed.id}", color="primary", size="sm", className="me-2"),
                        dbc.Button("Edit", color="outline-secondary",
                                   size="sm", className="me-2"),
                        dbc.Button("Delete", color="outline-danger", size="sm")
                    ])
                ])
            ], className="shadow-sm mb-4"), md=6, lg=4)

            shed_cards.append(card)

        return shed_cards
