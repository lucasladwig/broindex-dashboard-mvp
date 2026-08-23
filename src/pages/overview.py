"""
src/pages/overview.py
Main overview dashboard showing active sheds, active alerts, and batch KPIs.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.farm import Shed, Batch
from src.models.admin import AlertRule

dash.register_page(__name__, path="/", name="Overview")

layout = dbc.Container([
    # Hidden interval component to trigger data loading and refresh every 5 seconds
    dcc.Interval(id="overview-interval", interval=5000, n_intervals=0),

    html.H2("Farm Overview", className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Batch KPIs"),
            dbc.CardBody(id="batch-kpis-content",
                         children=dbc.Spinner(color="primary"))
        ]), md=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Active Alerts"),
            dbc.CardBody(id="active-alerts-content",
                         children=dbc.Spinner(color="primary"))
        ]), md=8),
    ], className="mb-4"),
    html.H4("Active Sheds", className="mb-3"),
    dbc.Row(id="overview-sheds-grid", children=dbc.Spinner(color="primary"))
], fluid=True)


@callback(
    Output("batch-kpis-content", "children"),
    Output("active-alerts-content", "children"),
    Output("overview-sheds-grid", "children"),
    Input("overview-interval", "n_intervals")
)
def update_overview(n):
    """
    Queries the database to populate the Overview page components.
    """
    with SessionLocal() as db:
        # 1. Fetch Active Batches
        active_batches = db.query(Batch).filter(Batch.status == "active").all()
        total_birds = sum(batch.initial_count for batch in active_batches)

        batch_html = html.Div([
            html.H3(f"{len(active_batches)} Active Batches",
                    className="text-primary"),
            html.P(f"Total Birds: {total_birds:,}")
        ])

        # 2. Fetch Alerts (For now, we just count the baseline rules to show connection)
        rules_count = db.query(AlertRule).count()
        alerts_html = html.Div([
            html.H3("0 Critical Alerts", className="text-success"),
            html.P(
                f"Monitoring {rules_count} active alert rules across the farm.")
        ])

        # 3. Fetch Active Sheds and generate cards
        active_sheds = db.query(Shed).filter(Shed.status == "active").all()

        if not active_sheds:
            sheds_html = [dbc.Col(html.P("No active sheds found."), width=12)]
        else:
            sheds_html = []
            for shed in active_sheds:
                card = dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H5(shed.name, className="mb-0")),
                    dbc.CardBody([
                        html.P(f"Capacity: {shed.capacity:,} birds"),
                        html.P(
                            f"Dimensions: {shed.width_m}m x {shed.length_m}m"),
                        dbc.Button(
                            "View Details", href=f"/sheds/{shed.id}", color="primary", size="sm")
                    ])
                ], className="shadow-sm mb-3"), md=4)
                sheds_html.append(card)

        return batch_html, alerts_html, sheds_html
