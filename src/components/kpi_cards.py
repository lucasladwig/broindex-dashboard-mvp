"""
src/components/kpi_cards.py
Standardized UI cards for displaying Key Performance Indicators (KPIs).
"""
from dash import html
import dash_bootstrap_components as dbc


def create_batch_kpi_card(batch_id: str, bird_count: int, mortality_rate: float, age_days: int) -> dbc.Card:
    """
    Generates a summary card for a specific poultry batch.
    """
    return dbc.Card([
        dbc.CardBody([
            html.H5(f"Batch: {batch_id}", className="card-title"),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.Small("Bird Count", className="text-muted"),
                    html.H4(f"{bird_count:,}")
                ]),
                dbc.Col([
                    html.Small("Mortality", className="text-muted"),
                    # Visual cue: red text if mortality is above a certain threshold
                    html.H4(
                        f"{mortality_rate}%", className="text-danger" if mortality_rate > 3.0 else "text-success")
                ]),
                dbc.Col([
                    html.Small("Age", className="text-muted"),
                    html.H4(f"{age_days} Days")
                ]),
            ])
        ])
    ], className="shadow-sm mb-3")


def create_alert_summary_card(active_count: int) -> dbc.Card:
    """
    Generates a quick-glance card for the current alert status.
    """
    card_color = "danger" if active_count > 0 else "success"
    status_text = "Critical Alerts" if active_count > 0 else "All Systems Normal"

    return dbc.Card([
        dbc.CardBody([
            html.H4(f"{active_count} {status_text}",
                    className=f"text-{card_color} text-center mb-0")
        ])
    ], color=card_color, outline=True, className="shadow-sm")
