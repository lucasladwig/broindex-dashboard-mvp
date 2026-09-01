"""
src/pages/batch_detail.py
Deep dive into a specific batch's performance, tracking weight gain and mortality logs.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone
from src.models.database import SessionLocal
from src.models.farm import Batch, Shed
from src.components.batch_modal import batch_modal

dash.register_page(
    __name__, path_template="/batches/<batch_id>", name="Batch Details")


def layout(batch_id=None, **kwargs):
    return dbc.Container([
        dcc.Store(id="current-batch-id", data=batch_id),
        # 5-second polling interval
        dcc.Interval(id="batch-detail-interval", interval=5000, n_intervals=0),

        batch_modal,

        # Header and KPIs
        dbc.Row(id="batch-header-container", className="mb-4 mt-2"),
        dbc.Row(id="batch-kpi-container", className="mb-4"),

        # Performance Charts
        dbc.Card([
            dbc.CardHeader(
                html.H5("Performance Logs: Weight vs. Mortality", className="mb-0")),
            dbc.CardBody(dcc.Graph(id="batch-performance-chart",
                         config={'displayModeBar': False}))
        ], className="shadow-sm mb-4")

    ], fluid=True)


@callback(
    Output("batch-header-container", "children"),
    Output("batch-kpi-container", "children"),
    Output("batch-performance-chart", "figure"),
    Input("batch-detail-interval", "n_intervals"),
    State("current-batch-id", "data")
)
def update_batch_detail(_, batch_id):
    if not batch_id:
        return dbc.Col(html.H4("No Batch ID provided.", className="text-danger")), [], dash.no_update

    with SessionLocal() as db:
        batch = db.query(Batch).filter(Batch.id == batch_id).first()

        if not batch:
            return dbc.Col(html.H4("Batch not found.", className="text-danger")), [], dash.no_update

        shed = db.query(Shed).filter(Shed.id == batch.shed_id).first()
        shed_name = shed.name if shed else "Unknown Shed"

        # ---------------------------------------------------------
        # 1. Header UI
        # ---------------------------------------------------------
        start_date = batch.start_date.replace(
            tzinfo=timezone.utc) if batch.start_date.tzinfo is None else batch.start_date
        age_days = max(0, (datetime.now(timezone.utc) - start_date).days)
        badge_color = "success" if batch.status.lower() == "active" else "secondary"

        header = dbc.Col([
            dbc.Row([
                dbc.Col(html.H2(f"Batch {batch.batch_number}",
                        className="text-primary mb-0"), width="auto"),
                dbc.Col(dbc.Badge(batch.status.upper(), color=badge_color,
                        className="ms-2 mt-2"), width="auto"),
                dbc.Col(dbc.Button("Edit Config", id={
                        'type': 'edit-batch-btn', 'index': batch.id}, color="outline-secondary", size="sm", className="ms-3"), width="auto")
            ], className="align-items-center mb-2"),
            html.P([
                html.Strong("Location: "), shed_name,
                html.Span(" | ", className="mx-2 text-muted"),
                html.Strong("Strain: "), batch.bird_strain,
                html.Span(" | ", className="mx-2 text-muted"),
                html.Strong("Start Date: "), start_date.strftime("%Y-%m-%d")
            ], className="text-muted mb-0")
        ])

        # ---------------------------------------------------------
        # 2. Mock Data & KPIs
        # ---------------------------------------------------------
        # Mocking a realistic growth curve up to the current age (max 45 days)
        plot_days = min(age_days, 45) if age_days > 0 else 1
        days_arr = np.arange(1, plot_days + 1)

        # Cobb 500 mock weight curve (exponential to linear, hitting ~2.8kg at day 42)
        weight_g = [min(50 * (d ** 1.1), 3000) + np.random.normal(0, 10)
                    for d in days_arr]

        # Mock daily mortality (slightly higher in week 1, then flattening out)
        daily_mortality = [
            int(abs(np.random.normal(15 if d < 7 else 5, 3))) for d in days_arr]
        total_mortality = sum(daily_mortality)

        current_weight_g = weight_g[-1] if weight_g else 50
        current_birds = batch.initial_count - total_mortality
        mortality_rate = (total_mortality / batch.initial_count) * 100

        kpis = [
            dbc.Col(dbc.Card(dbc.CardBody([html.Small("Current Age", className="text-muted"), html.H4(
                f"{age_days} Days")]), className="shadow-sm border-start border-primary border-4"), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.Small("Est. Avg Weight", className="text-muted"), html.H4(
                f"{current_weight_g/1000:.2f} kg")]), className="shadow-sm border-start border-success border-4"), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.Small("Total Birds", className="text-muted"), html.H4(
                f"{current_birds:,}")]), className="shadow-sm border-start border-info border-4"), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.Small("Mortality Rate", className="text-muted"), html.H4(
                f"{mortality_rate:.2f}%", className="text-danger" if mortality_rate > 3 else "text-success")]), className="shadow-sm border-start border-danger border-4"), md=3),
        ]

        # ---------------------------------------------------------
        # 3. Performance Chart
        # ---------------------------------------------------------
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=days_arr, y=weight_g, name="Avg Weight (g)",
                       line=dict(color="#28a745", width=3)),
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(x=days_arr, y=daily_mortality, name="Daily Mortality",
                   marker_color="#dc3545", opacity=0.7),
            secondary_y=True,
        )

        fig.update_layout(
            title_text="Growth Curve vs. Mortality Events",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        fig.update_yaxes(title_text="<b>Weight</b> (grams)", secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Mortality</b> (birds)", secondary_y=True)

        return header, kpis, fig
