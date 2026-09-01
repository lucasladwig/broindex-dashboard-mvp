"""
src/pages/sheds.py
Overview grid of all sheds.
"""

import dash
from dash import html, dcc, callback, Input, Output, ctx, ALL
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.farm import Shed
from src.components.shed_modal import shed_modal

dash.register_page(__name__, path="/sheds", name="Sheds")

layout = dbc.Container([
    dcc.Interval(id="sheds-interval", interval=5000, n_intervals=0),
    html.Div(id="delete-feedback", style={"display": "none"}),
    shed_modal,  # Injected Shared Component

    dbc.Row([
        dbc.Col(html.H2("Shed Management"), width=8),
        # Updated to pattern-matching ID
        dbc.Col(dbc.Button("Add New Shed", id={
                'type': 'add-shed-btn', 'index': 'new'}, color="primary", className="float-end"), width=4)
    ], className="mb-4"),

    dbc.Row(id="sheds-list-container", children=dbc.Spinner(color="primary"))
], fluid=True)


@callback(
    Output("sheds-list-container", "children"),
    Input("sheds-interval", "n_intervals")
)
def update_sheds_list(_):
    with SessionLocal() as db:
        sheds = db.query(Shed).all()
        if not sheds:
            return [dbc.Col(html.P("No sheds found in the database."), width=12)]

        shed_cards = []
        for shed in sheds:
            badge_color = "success" if shed.status.lower() == "active" else "secondary"
            card = dbc.Col(dbc.Card([
                dbc.CardHeader([html.H5(shed.name, className="d-inline-block mb-0 mt-1"),
                               dbc.Badge(shed.status.upper(), color=badge_color, className="float-end")]),
                dbc.CardBody([
                    html.P([html.Strong("Capacity: "),
                           f"{shed.capacity:,} birds"], className="mb-1"),
                    html.P([html.Strong("Dimensions: "),
                           f"{shed.width_m}m x {shed.length_m}m"], className="mb-1"),
                    html.P([html.Strong(
                        "Grid Layout: "), f"{shed.grid_cols} columns x {shed.grid_rows} rows"], className="mb-3"),
                    html.Div([
                        dbc.Button(
                            "View Map", href=f"/sheds/{shed.id}", color="primary", size="sm", className="me-2"),
                        dbc.Button("Edit", id={'type': 'edit-shed-btn', 'index': shed.id},
                                   color="outline-secondary", size="sm", className="me-2"),
                        dbc.Button("Delete", id={
                                   'type': 'delete-shed-btn', 'index': shed.id}, color="outline-danger", size="sm")
                    ])
                ])
            ], className="shadow-sm mb-4"), md=6, lg=4)
            shed_cards.append(card)
        return shed_cards


@callback(
    Output("delete-feedback", "children"),
    Input({'type': 'delete-shed-btn', 'index': ALL}, "n_clicks"),
    prevent_initial_call=True
)
def delete_shed(delete_clicks):
    # Guard: Prevent execution if triggered by dynamic component insertion
    if not ctx.triggered or ctx.triggered[0]['value'] is None:
        return dash.no_update

    trigger = ctx.triggered_id
    if isinstance(trigger, dict) and trigger.get('type') == 'delete-shed-btn':
        with SessionLocal() as db:
            shed = db.query(Shed).filter(
                Shed.id == trigger.get('index')).first()
            if shed:
                db.delete(shed)
                db.commit()
    return ""
