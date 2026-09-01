"""
src/components/shed_modal.py
Reusable modal and callback for creating and editing sheds.
"""

import dash
from dash import html, dcc, callback, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.farm import Shed

# Define the Shared Add/Edit Modal UI
shed_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(id="modal-shed-title")),
    dbc.ModalBody([
        dcc.Store(id="edit-shed-id", data=None),

        dbc.Label("Shed Name"),
        dbc.Input(id="input-shed-name", type="text",
                  placeholder="e.g. Shed 01", className="mb-3"),

        dbc.Row([
            dbc.Col([dbc.Label("Grid Columns (X)"), dbc.Input(
                id="input-shed-cols", type="number", min=1, step=1)]),
            dbc.Col([dbc.Label("Grid Rows (Y)"), dbc.Input(
                id="input-shed-rows", type="number", min=1, step=1)])
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([dbc.Label("Width (m)"), dbc.Input(
                id="input-shed-width", type="number", min=1, step=0.1)]),
            dbc.Col([dbc.Label("Length (m)"), dbc.Input(
                id="input-shed-length", type="number", min=1, step=0.1)]),
        ], className="mb-3"),

        dbc.Label("Maximum Bird Capacity"),
        dbc.Input(id="input-shed-capacity", type="number",
                  min=1, step=1, className="mb-3"),

        html.Div(id="modal-shed-feedback", className="text-danger mt-2")
    ]),
    dbc.ModalFooter([
        dbc.Button("Cancel", id="btn-cancel-shed",
                   color="secondary", className="me-2"),
        dbc.Button("Save Shed", id="btn-save-shed", color="success")
    ]),
], id="modal-shed", is_open=False, backdrop="static")


# Global Callback for the Modal
@callback(
    Output("modal-shed", "is_open"),
    Output("modal-shed-title", "children"),
    Output("edit-shed-id", "data"),
    Output("input-shed-name", "value"),
    Output("input-shed-cols", "value"),
    Output("input-shed-rows", "value"),
    Output("input-shed-width", "value"),
    Output("input-shed-length", "value"),
    Output("input-shed-capacity", "value"),
    Output("modal-shed-feedback", "children"),

    # Pattern matching safely handles buttons regardless of which page the user is on
    Input({'type': 'add-shed-btn', 'index': ALL}, "n_clicks"),
    Input({'type': 'edit-shed-btn', 'index': ALL}, "n_clicks"),
    Input("btn-cancel-shed", "n_clicks"),
    Input("btn-save-shed", "n_clicks"),

    State("edit-shed-id", "data"),
    State("input-shed-name", "value"),
    State("input-shed-cols", "value"),
    State("input-shed-rows", "value"),
    State("input-shed-width", "value"),
    State("input-shed-length", "value"),
    State("input-shed-capacity", "value"),
    prevent_initial_call=True
)
def handle_shed_modal(add_clicks, edit_clicks, cancel_clicks, save_clicks,
                      shed_id, name, cols, rows, width, length, capacity):

    # Guard: Prevent execution if triggered by dynamic component insertion
    if not ctx.triggered or ctx.triggered[0]['value'] is None:
        return tuple([dash.no_update] * 10)

    trigger = ctx.triggered_id

    if trigger == "btn-cancel-shed":
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    if isinstance(trigger, dict):
        if trigger.get('type') == 'add-shed-btn':
            return True, "Add New Shed", None, "", "", "", "", "", "", ""

        if trigger.get('type') == 'edit-shed-btn':
            edit_id = trigger.get('index')
            with SessionLocal() as db:
                shed = db.query(Shed).filter(Shed.id == edit_id).first()
                if shed:
                    return True, f"Edit {shed.name}", edit_id, shed.name, shed.grid_cols, shed.grid_rows, shed.width_m, shed.length_m, shed.capacity, ""
            return dash.no_update

    if trigger == "btn-save-shed":
        if not all([name, cols, rows, width, length, capacity]):
            return True, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "All fields are required."

        with SessionLocal() as db:
            if shed_id is None:  # Insert New
                new_shed = Shed(farm_id=1, name=name, grid_cols=cols, grid_rows=rows,
                                width_m=width, length_m=length, capacity=capacity, status="active")
                db.add(new_shed)
            else:  # Update Existing
                shed = db.query(Shed).filter(Shed.id == shed_id).first()
                if shed:
                    shed.name, shed.grid_cols, shed.grid_rows = name, cols, rows
                    shed.width_m, shed.length_m, shed.capacity = width, length, capacity
            db.commit()

        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    return tuple([dash.no_update] * 10)
