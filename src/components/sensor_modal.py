"""
src/components/sensor_modal.py
Reusable modal and callback for creating and editing sensors.
"""

import dash
from dash import html, dcc, callback, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.sensors import Sensor

sensor_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(id="modal-sensor-title")),
    dbc.ModalBody([
        # Hidden store to track if we are editing an existing sensor
        dcc.Store(id="edit-sensor-id", data=None),

        dbc.Row([
            dbc.Col([
                dbc.Label("Sensor ID"),
                dbc.Input(id="input-sensor-id", type="number",
                          min=1, step=1, placeholder="e.g. 1")
            ], md=6),
            dbc.Col([
                dbc.Label("Shed ID Assignment"),
                dbc.Input(id="input-sensor-shed-id", type="number",
                          min=1, step=1, placeholder="e.g. 1")
            ], md=6)
        ], className="mb-3"),

        dbc.Label("MAC Address"),
        dbc.Input(id="input-sensor-mac", type="text",
                  placeholder="00:11:22:33:44:55", className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Brand"),
                dbc.Input(id="input-sensor-brand", type="text",
                          placeholder="e.g. Generic")
            ]),
            dbc.Col([
                dbc.Label("Model"),
                dbc.Input(id="input-sensor-model", type="text",
                          placeholder="e.g. TempHum-v1")
            ])
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Grid Position (X)"),
                dbc.Input(id="input-sensor-x", type="number", min=1, step=1)
            ]),
            dbc.Col([
                dbc.Label("Grid Position (Y)"),
                dbc.Input(id="input-sensor-y", type="number", min=1, step=1)
            ])
        ], className="mb-3"),

        dbc.Label("Status"),
        dbc.Select(
            id="input-sensor-status",
            options=[
                {"label": "Active", "value": "active"},
                {"label": "Inactive", "value": "inactive"},
                {"label": "Maintenance", "value": "maintenance"},
            ],
            value="active",
            className="mb-3"
        ),

        html.Div(id="modal-sensor-feedback", className="text-danger mt-2")
    ]),
    dbc.ModalFooter([
        dbc.Button("Cancel", id="btn-cancel-sensor",
                   color="secondary", className="me-2"),
        dbc.Button("Save Sensor", id="btn-save-sensor", color="success")
    ]),
], id="modal-sensor", is_open=False, backdrop="static")


@callback(
    Output("modal-sensor", "is_open"),
    Output("modal-sensor-title", "children"),
    Output("edit-sensor-id", "data"),
    Output("input-sensor-id", "value"),
    # Disable ID modification during edits
    Output("input-sensor-id", "disabled"),
    Output("input-sensor-shed-id", "value"),
    Output("input-sensor-mac", "value"),
    Output("input-sensor-brand", "value"),
    Output("input-sensor-model", "value"),
    Output("input-sensor-x", "value"),
    Output("input-sensor-y", "value"),
    Output("input-sensor-status", "value"),
    Output("modal-sensor-feedback", "children"),

    Input({'type': 'add-sensor-btn', 'index': ALL}, "n_clicks"),
    Input({'type': 'edit-sensor-btn', 'index': ALL}, "n_clicks"),
    Input("btn-cancel-sensor", "n_clicks"),
    Input("btn-save-sensor", "n_clicks"),

    State("edit-sensor-id", "data"),
    State("input-sensor-id", "value"),
    State("input-sensor-shed-id", "value"),
    State("input-sensor-mac", "value"),
    State("input-sensor-brand", "value"),
    State("input-sensor-model", "value"),
    State("input-sensor-x", "value"),
    State("input-sensor-y", "value"),
    State("input-sensor-status", "value"),
    prevent_initial_call=True
)
def handle_sensor_modal(add_clicks, edit_clicks, cancel_clicks, save_clicks,
                        edit_id, s_id, shed_id, mac, brand, model, x, y, status):

    # Guard against dynamic component injection phantom clicks
    if not ctx.triggered or ctx.triggered[0]['value'] is None:
        return tuple([dash.no_update] * 13)

    trigger = ctx.triggered_id

    # Action A: Close
    if trigger == "btn-cancel-sensor":
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    if isinstance(trigger, dict):
        # Action B: Open "Add"
        if trigger.get('type') == 'add-sensor-btn':
            return True, "Add New Sensor", None, "", False, 1, "", "", "", "", "", "active", ""

        # Action C: Open "Edit"
        if trigger.get('type') == 'edit-sensor-btn':
            target_id = trigger.get('index')
            with SessionLocal() as db:
                sensor = db.query(Sensor).filter(
                    Sensor.id == target_id).first()
                if sensor:
                    return True, f"Edit Sensor SEN-{sensor.id:03d}", target_id, sensor.id, True, sensor.shed_id, sensor.mac_address, sensor.brand, sensor.model, sensor.grid_x, sensor.grid_y, sensor.status, ""
            return dash.no_update

    # Action D: Save
    if trigger == "btn-save-sensor":
        if not all([s_id, shed_id, mac, x, y, status]):
            return True, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "ID, Shed ID, MAC, Grid X, Grid Y, and Status are required."

        with SessionLocal() as db:
            if edit_id is None:
                # Check for ID collision
                existing = db.query(Sensor).filter(Sensor.id == s_id).first()
                if existing:
                    return True, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, f"Sensor ID {s_id} already exists."

                new_sensor = Sensor(id=s_id, shed_id=shed_id, mac_address=mac,
                                    brand=brand, model=model, grid_x=x, grid_y=y, status=status)
                db.add(new_sensor)
            else:
                sensor = db.query(Sensor).filter(Sensor.id == edit_id).first()
                if sensor:
                    sensor.shed_id, sensor.mac_address, sensor.brand = shed_id, mac, brand
                    sensor.model, sensor.grid_x, sensor.grid_y, sensor.status = model, x, y, status
            db.commit()

        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    return tuple([dash.no_update] * 13)
