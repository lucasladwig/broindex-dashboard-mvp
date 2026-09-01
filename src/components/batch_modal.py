"""
src/components/batch_modal.py
Reusable modal and callback for creating and editing farm batches.
"""

import dash
from dash import html, dcc, callback, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.farm import Batch
from datetime import datetime

batch_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(id="modal-batch-title")),
    dbc.ModalBody([
        # Hidden store to track if we are editing an existing batch
        dcc.Store(id="edit-batch-id", data=None),

        dbc.Row([
            dbc.Col([
                dbc.Label("Shed ID Assignment"),
                dbc.Input(id="input-batch-shed-id", type="number",
                          min=1, step=1, placeholder="e.g. 1")
            ], md=6),
            dbc.Col([
                dbc.Label("Initial Bird Count"),
                dbc.Input(id="input-batch-size", type="number",
                          min=1, step=1, placeholder="e.g. 15000")
            ], md=6)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Start Date"),
                dbc.Input(id="input-batch-start", type="date")
            ], md=6),
            dbc.Col([
                dbc.Label("Status"),
                dbc.Select(
                    id="input-batch-status",
                    options=[
                        {"label": "Planned", "value": "planned"},
                        {"label": "Active", "value": "active"},
                        {"label": "Completed", "value": "completed"},
                    ],
                    value="planned"
                )
            ], md=6)
        ], className="mb-3"),

        html.Div(id="modal-batch-feedback", className="text-danger mt-2")
    ]),
    dbc.ModalFooter([
        dbc.Button("Cancel", id="btn-cancel-batch",
                   color="secondary", className="me-2"),
        dbc.Button("Save Batch", id="btn-save-batch", color="success")
    ]),
], id="modal-batch", is_open=False, backdrop="static")


@callback(
    Output("modal-batch", "is_open"),
    Output("modal-batch-title", "children"),
    Output("edit-batch-id", "data"),
    Output("input-batch-shed-id", "value"),
    Output("input-batch-size", "value"),
    Output("input-batch-start", "value"),
    Output("input-batch-status", "value"),
    Output("modal-batch-feedback", "children"),

    Input({'type': 'add-batch-btn', 'index': ALL}, "n_clicks"),
    Input({'type': 'edit-batch-btn', 'index': ALL}, "n_clicks"),
    Input("btn-cancel-batch", "n_clicks"),
    Input("btn-save-batch", "n_clicks"),

    State("edit-batch-id", "data"),
    State("input-batch-shed-id", "value"),
    State("input-batch-size", "value"),
    State("input-batch-start", "value"),
    State("input-batch-status", "value"),
    prevent_initial_call=True
)
def handle_batch_modal(add_clicks, edit_clicks, cancel_clicks, save_clicks,
                       edit_id, shed_id, size, start_date, status):

    # Guard against dynamic component injection phantom clicks
    if not ctx.triggered or ctx.triggered[0]['value'] is None:
        return tuple([dash.no_update] * 8)

    trigger = ctx.triggered_id

    if trigger == "btn-cancel-batch":
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    if isinstance(trigger, dict):
        if trigger.get('type') == 'add-batch-btn':
            today_str = datetime.today().strftime('%Y-%m-%d')
            return True, "Start New Batch", None, "", "", today_str, "planned", ""

        if trigger.get('type') == 'edit-batch-btn':
            target_id = trigger.get('index')
            with SessionLocal() as db:
                batch = db.query(Batch).filter(Batch.id == target_id).first()
                if batch:
                    start_str = str(
                        batch.start_date) if batch.start_date else ""
                    # 1. FIXED: Changed batch.bird_count to batch.initial_count
                    return True, f"Edit Batch {batch.id}", target_id, batch.shed_id, batch.initial_count, start_str, batch.status, ""
            return dash.no_update

    if trigger == "btn-save-batch":
        if not all([shed_id, size, start_date, status]):
            return True, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "Shed ID, Bird Count, Start Date, and Status are required."

        try:
            parsed_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return True, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "Invalid date format."

        with SessionLocal() as db:
            if edit_id is None:
                # 2. FIXED: Changed bird_count=size to initial_count=size
                new_batch = Batch(shed_id=shed_id, initial_count=size,
                                  start_date=parsed_date, status=status)
                db.add(new_batch)
            else:
                batch = db.query(Batch).filter(Batch.id == edit_id).first()
                if batch:
                    # 3. FIXED: Changed batch.bird_count to batch.initial_count
                    batch.shed_id, batch.initial_count = shed_id, size
                    batch.start_date, batch.status = parsed_date, status
            db.commit()

        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    return tuple([dash.no_update] * 8)
