"""
src/pages/batches.py
Management and overview of poultry batches across the farm.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime, timezone
from src.models.database import SessionLocal
from src.models.farm import Batch, Shed
from src.components.kpi_cards import create_batch_kpi_card

dash.register_page(__name__, path="/batches", name="Batches")

layout = dbc.Container([
    # 5-second polling interval
    dcc.Interval(id="batches-interval", interval=5000, n_intervals=0),

    dbc.Row([
        dbc.Col(html.H2("Batch Management"), width=8),
        dbc.Col(dbc.Button("Register New Batch", id="btn-add-batch",
                color="primary", className="float-end"), width=4)
    ], className="mb-4"),

    html.H4("Active Batches", className="mb-3 text-secondary"),
    dbc.Row(id="active-batches-container",
            children=dbc.Spinner(color="primary")),

    html.Hr(className="my-5"),

    html.H4("Batch History", className="mb-3 text-secondary"),
    dbc.Row(id="historical-batches-container",
            children=dbc.Spinner(color="primary"))

], fluid=True)


@callback(
    Output("active-batches-container", "children"),
    Output("historical-batches-container", "children"),
    Input("batches-interval", "n_intervals")
)
def update_batches_list(_):
    """
    Fetches batches from the database, calculates their age, and separates them 
    into Active (KPI cards) and Historical (Table) UI components.
    """
    with SessionLocal() as db:
        batches = db.query(Batch).all()

        if not batches:
            empty_msg = [
                dbc.Col(html.P("No batches found in the database."), width=12)]
            return empty_msg, empty_msg

        # Lookup dictionary to get Shed Names
        sheds = {shed.id: shed.name for shed in db.query(Shed).all()}

        active_cards = []
        history_rows = []

        for b in batches:
            shed_name = sheds.get(b.shed_id, "Unknown Shed")

            # Calculate age in days
            # Ensure we are using UTC to match our database seed logic
            now = datetime.now(timezone.utc)

            # Make b.start_date timezone-aware if it isn't already (SQLite datetime quirk)
            start_date = b.start_date.replace(
                tzinfo=timezone.utc) if b.start_date.tzinfo is None else b.start_date

            age_delta = now - start_date
            age_days = max(0, age_delta.days)

            # Mocking mortality rate for now (we can build a separate mortality log table later)
            mock_mortality_rate = 1.2

            if b.status.lower() == "active":
                # Combine Batch Number and Shed Name for context on the KPI Card
                display_title = f"{b.batch_number} ({shed_name})"

                # Wrap the KPI card in a dcc.Link to make the whole block clickable
                card = dbc.Col(
                    dcc.Link(
                        create_batch_kpi_card(
                            batch_id=display_title,
                            bird_count=b.initial_count,
                            mortality_rate=mock_mortality_rate,
                            age_days=age_days
                        ),
                        href=f"/batches/{b.id}",
                        # Prevents blue link text/underlines
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    md=6, lg=4,
                    className="mb-3"
                )
                active_cards.append(card)
            else:
                # Add inactive/completed batches to the history table
                history_rows.append(
                    html.Tr([
                        html.Td(html.Strong(b.batch_number)),
                        html.Td(shed_name),
                        html.Td(b.bird_strain),
                        html.Td(f"{b.initial_count:,}"),
                        html.Td(start_date.strftime("%Y-%m-%d")),
                        html.Td(dbc.Badge(b.status.upper(), color="secondary"))
                    ], className="align-middle")
                )

        # Handle empty states gracefully
        if not active_cards:
            active_cards = [dbc.Col(html.P(
                "No active batches running at this time.", className="text-muted"), width=12)]

        if not history_rows:
            history_ui = [dbc.Col(
                html.P("No historical batches found.", className="text-muted"), width=12)]
        else:
            table_header = [html.Thead(html.Tr([
                html.Th("Batch"), html.Th("Location"), html.Th("Strain"),
                html.Th("Initial Count"), html.Th(
                    "Start Date"), html.Th("Status")
            ]))]
            table_body = [html.Tbody(history_rows)]
            history_ui = [
                dbc.Col(
                    dbc.Card(dbc.Table(table_header + table_body, hover=True, responsive=True,
                             className="mb-0"), className="shadow-sm overflow-hidden"),
                    width=12
                )
            ]

        return active_cards, history_ui
