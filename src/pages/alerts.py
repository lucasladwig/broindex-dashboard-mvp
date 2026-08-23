"""
src/pages/alerts.py
Management of system alert rules and active notifications.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
from src.models.database import SessionLocal
from src.models.admin import AlertRule
from src.components.kpi_cards import create_alert_summary_card

dash.register_page(__name__, path="/alerts", name="Alerts & Rules")

layout = dbc.Container([
    # 5-second polling interval
    dcc.Interval(id="alerts-interval", interval=5000, n_intervals=0),

    dbc.Row([
        dbc.Col(html.H2("Alerts & Rules"), width=8),
        dbc.Col(dbc.Button("Create New Rule", id="btn-add-rule",
                color="primary", className="float-end"), width=4)
    ], className="mb-4"),

    # Summary Row
    dbc.Row(id="alerts-summary-container", className="mb-4"),

    # Active Alerts Section (Triggered Events)
    html.H4("Active System Alerts", className="mb-3 text-danger"),
    dbc.Row(id="active-alerts-container",
            children=dbc.Spinner(color="danger"), className="mb-5"),

    # Alert Rules Section (Configuration)
    html.H4("Configured Alert Rules", className="mb-3 text-secondary"),
    dbc.Row(id="alert-rules-container", children=dbc.Spinner(color="primary"))

], fluid=True)


@callback(
    Output("alerts-summary-container", "children"),
    Output("active-alerts-container", "children"),
    Output("alert-rules-container", "children"),
    Input("alerts-interval", "n_intervals")
)
def update_alerts_page(_):
    with SessionLocal() as db:
        rules = db.query(AlertRule).all()

        # ---------------------------------------------------------
        # 1. Mock Active Triggered Alerts
        # (This will be replaced by a database query to an AlertLog table)
        # ---------------------------------------------------------
        mock_triggered_alerts = [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rule_name": "High Temp Warning",
                "shed_name": "Shed 01 - Broilers",
                "sensor_id": "SEN-002",
                "grid_location": "(X: 3, Y: 3)",
                "reading": "28.5°C",
                "severity": "warning"
            }
        ]

        # 2. Update Summary Card
        summary_ui = dbc.Col(create_alert_summary_card(
            active_count=len(mock_triggered_alerts)), md=6, lg=4)

        # 3. Build Active Alerts Table
        active_header = [
            html.Thead(html.Tr([
                html.Th("Time"), html.Th("Alert"), html.Th("Shed"),
                html.Th("Sensor (Grid)"), html.Th(
                    "Current Reading"), html.Th("Action")
            ]))
        ]

        active_rows = []
        for alert in mock_triggered_alerts:
            badge_color = "danger" if alert["severity"] == "critical" else "warning"

            row = html.Tr([
                html.Td(alert["timestamp"]),
                html.Td(html.Strong(alert["rule_name"],
                        className=f"text-{badge_color}")),
                html.Td(alert["shed_name"]),
                html.Td(f"{alert['sensor_id']} {alert['grid_location']}"),
                html.Td(html.Code(alert["reading"])),
                html.Td(dbc.Button("Acknowledge", size="sm",
                        color="outline-primary", className="py-0"))
            ], className="align-middle bg-light")
            active_rows.append(row)

        active_alerts_ui = [
            dbc.Col(
                dbc.Card(dbc.Table(active_header + [html.Tbody(active_rows)], hover=True, responsive=True,
                         className="mb-0"), className="shadow-sm border-warning overflow-hidden"),
                width=12
            )
        ]

        # ---------------------------------------------------------
        # 4. Build Configured Rules Table
        # ---------------------------------------------------------
        if not rules:
            rules_ui = [
                dbc.Col(html.P("No alert rules configured."), width=12)]
        else:
            rules_header = [
                html.Thead(html.Tr([
                    html.Th("Rule Name"), html.Th(
                        "Metric"), html.Th("Condition"),
                    html.Th("Duration Threshold"), html.Th(
                        "Severity"), html.Th("Actions")
                ]))
            ]

            rules_rows = []
            for r in rules:
                unit = "°C" if r.metric.lower() == "temperature" else "%"
                condition_val = r.threshold_min if r.operator == ">" else r.threshold_max
                condition_str = f"{r.operator} {condition_val}{unit}"
                badge_color = "danger" if r.severity.lower(
                ) == "critical" else "warning" if r.severity.lower() == "warning" else "info"

                row = html.Tr([
                    html.Td(html.Strong(r.name)),
                    html.Td(r.metric.capitalize()),
                    html.Td(html.Code(condition_str)),
                    html.Td(f"{r.duration_mins} mins"),
                    html.Td(dbc.Badge(r.severity.upper(),
                            color=badge_color, pill=True)),
                    html.Td([
                        dbc.Button(
                            "Edit", size="sm", color="outline-secondary", className="me-2 py-0"),
                        dbc.Button("Disable", size="sm",
                                   color="outline-danger", className="py-0")
                    ])
                ], className="align-middle")
                rules_rows.append(row)

            rules_ui = [
                dbc.Col(
                    dbc.Card(dbc.Table(rules_header + [html.Tbody(rules_rows)], hover=True,
                             responsive=True, className="mb-0"), className="shadow-sm overflow-hidden"),
                    width=12
                )
            ]

        return summary_ui, active_alerts_ui, rules_ui
