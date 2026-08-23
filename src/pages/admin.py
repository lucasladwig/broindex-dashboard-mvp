"""
src/pages/admin.py
Single-page configuration center for global settings, alert rules, and batch defaults.
"""

import dash
from dash import html, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/admin", name="Admin Configurations")

layout = dbc.Container([
    html.H2("System Configurations", className="mb-4 mt-2"),

    # 1. Global Configurations
    dbc.Card([
        dbc.CardHeader(html.H5("Farm Details", className="mb-0")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Farm Name"),
                    dbc.Input(id="input-farm-name", type="text",
                              placeholder="e.g. Sunrise Poultry Farm")
                ], md=4),
                dbc.Col([
                    dbc.Label("Responsible Person"),
                    dbc.Input(id="input-resp-person", type="text",
                              placeholder="e.g. Lucas")
                ], md=4),
                dbc.Col([
                    dbc.Label("Location Coordinates"),
                    dbc.InputGroup([
                        dbc.InputGroupText("Lat"),
                        dbc.Input(id="input-lat", type="number",
                                  step="any", placeholder="-23.5505"),
                        dbc.InputGroupText("Long"),
                        dbc.Input(id="input-long", type="number",
                                  step="any", placeholder="-46.6333")
                    ])
                ], md=4)
            ])
        ])
    ], className="shadow-sm mb-4"),

    # 2. Batch Defaults Configurations
    dbc.Card([
        dbc.CardHeader(html.H5("Batch Defaults", className="mb-0")),
        dbc.CardBody([
            html.H6("Target Environment", className="mb-3 text-secondary"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Temperature Range (°C)"),
                    dbc.InputGroup([
                        dbc.Input(id="batch-temp-min", type="number",
                                  value=22.0, step=0.1),
                        dbc.InputGroupText("to"),
                        dbc.Input(id="batch-temp-max", type="number",
                                  value=28.0, step=0.1)
                    ])
                ], md=6),
                dbc.Col([
                    dbc.Label("Humidity Range (%)"),
                    dbc.InputGroup([
                        dbc.Input(id="batch-hum-min", type="number",
                                  value=50.0, step=1),
                        dbc.InputGroupText("to"),
                        dbc.Input(id="batch-hum-max",
                                  type="number", value=60.0, step=1)
                    ])
                ], md=6),
            ], className="mb-4"),

            html.Hr(className="my-4"),

            html.H6("Batch Openings Schedule",
                    className="mb-3 text-secondary"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Total Openings"),
                    dbc.Input(id="batch-openings-count",
                              type="number", min=3, max=5, step=1, value=5)
                ], md=3, className="mb-3")
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Opening 1", className="small text-muted"),
                    dbc.InputGroup([dbc.Input(
                        id="op-1-dur", type="number", value=7, min=1), dbc.InputGroupText("days")])
                ]),
                dbc.Col([
                    dbc.Label("Opening 2", className="small text-muted"),
                    dbc.InputGroup([dbc.Input(
                        id="op-2-dur", type="number", value=7, min=1), dbc.InputGroupText("days")])
                ]),
                dbc.Col([
                    dbc.Label("Opening 3", className="small text-muted"),
                    dbc.InputGroup([dbc.Input(
                        id="op-3-dur", type="number", value=14, min=1), dbc.InputGroupText("days")])
                ]),
                dbc.Col([
                    dbc.Label("Opening 4", className="small text-muted"),
                    dbc.InputGroup([dbc.Input(
                        id="op-4-dur", type="number", value=7, min=1), dbc.InputGroupText("days")])
                ]),
                dbc.Col([
                    dbc.Label("Opening 5", className="small text-muted"),
                    dbc.InputGroup([dbc.Input(
                        id="op-5-dur", type="number", value=10, min=1), dbc.InputGroupText("days")])
                ]),
            ])
        ])
    ], className="shadow-sm mb-4"),

    # 3. Alert Rules Configurations
    dbc.Card([
        dbc.CardHeader(html.H5("Alert Rules", className="mb-0")),
        dbc.CardBody([

            # Temperature Sequential Grouping
            html.H6("Temperature Thresholds (°C)",
                    className="mb-3 text-secondary"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Critical Low",
                              className="text-danger fw-bold small"),
                    dbc.Input(id="temp-crit-low", type="number",
                              value=15.0, step=0.1)
                ], md=3),
                dbc.Col([
                    dbc.Label("Warning Low",
                              className="text-warning fw-bold small"),
                    dbc.Input(id="temp-warn-low", type="number",
                              value=20.0, step=0.1)
                ], md=3),
                dbc.Col([
                    dbc.Label("Warning High",
                              className="text-warning fw-bold small"),
                    dbc.Input(id="temp-warn-high", type="number",
                              value=30.0, step=0.1)
                ], md=3),
                dbc.Col([
                    dbc.Label("Critical High",
                              className="text-danger fw-bold small"),
                    dbc.Input(id="temp-crit-high", type="number",
                              value=35.0, step=0.1)
                ], md=3),
            ], className="mb-4 text-center"),

            # Humidity Sequential Grouping
            html.H6("Humidity Thresholds (%)",
                    className="mb-3 text-secondary"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Critical Low",
                              className="text-danger fw-bold small"),
                    dbc.Input(id="hum-crit-low", type="number",
                              value=30.0, step=1)
                ], md=3),
                dbc.Col([
                    dbc.Label("Warning Low",
                              className="text-warning fw-bold small"),
                    dbc.Input(id="hum-warn-low", type="number",
                              value=40.0, step=1)
                ], md=3),
                dbc.Col([
                    dbc.Label("Warning High",
                              className="text-warning fw-bold small"),
                    dbc.Input(id="hum-warn-high",
                              type="number", value=70.0, step=1)
                ], md=3),
                dbc.Col([
                    dbc.Label("Critical High",
                              className="text-danger fw-bold small"),
                    dbc.Input(id="hum-crit-high",
                              type="number", value=85.0, step=1)
                ], md=3),
            ], className="mb-4 text-center"),

            html.Hr(className="my-4"),

            # Time Condition
            dbc.Row([
                dbc.Col([
                    dbc.Label("Trigger Delay"),
                    dbc.InputGroup([
                        dbc.Input(id="input-alert-duration",
                                  type="number", value=15, min=1),
                        dbc.InputGroupText("mins outside thresholds")
                    ])
                ], md=4)
            ])
        ])
    ], className="shadow-sm mb-4"),


    # Save Action
    html.Div([
        dbc.Button("Save Configurations", id="btn-save-admin",
                   color="success", size="lg", className="me-3"),
        html.Span(id="admin-save-feedback")
    ], className="mb-5 d-flex align-items-center")

], fluid=True)


@callback(
    Output("admin-save-feedback", "children"),
    Input("btn-save-admin", "n_clicks"),
    prevent_initial_call=True
)
def save_configurations(n_clicks):
    """
    Mock callback to simulate saving configurations to the database.
    """
    return dbc.Alert("Configurations saved successfully!", color="success", duration=3000, className="mb-0")
