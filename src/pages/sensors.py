"""
src/pages/sensors.py
Overview and management of all IoT sensors across the farm, grouped by shed.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from src.models.database import SessionLocal
from src.models.sensors import Sensor
from src.models.farm import Shed

dash.register_page(__name__, path="/sensors", name="Sensors")

layout = dbc.Container([
    # 5-second polling interval
    dcc.Interval(id="sensors-interval", interval=5000, n_intervals=0),

    dbc.Row([
        dbc.Col(html.H2("Sensor Fleet"), width=8),
        dbc.Col(dbc.Button("Register Sensor", id="btn-register-sensor",
                color="primary", className="float-end"), width=4)
    ], className="mb-4"),

    dbc.Row(id="sensors-list-container", children=dbc.Spinner(color="primary"))
], fluid=True)


@callback(
    Output("sensors-list-container", "children"),
    Input("sensors-interval", "n_intervals")
)
def update_sensors_list(_):
    with SessionLocal() as db:
        sensors = db.query(Sensor).all()

        if not sensors:
            return [dbc.Col(html.P("No sensors found in the database."), width=12)]

        # Create a lookup dictionary for Shed Names
        sheds = {shed.id: shed.name for shed in db.query(Shed).all()}

        # Group sensors by Shed Name
        sensors_by_shed = {}
        for s in sensors:
            shed_name = sheds.get(s.shed_id, "Unassigned")
            if shed_name not in sensors_by_shed:
                sensors_by_shed[shed_name] = []
            sensors_by_shed[shed_name].append(s)

        # Sort shed names alphabetically, but force "Unassigned" to the very bottom
        sorted_sheds = sorted(list(sensors_by_shed.keys()))
        if "Unassigned" in sorted_sheds:
            sorted_sheds.remove("Unassigned")
            sorted_sheds.append("Unassigned")

        # Build UI sections for each shed
        sections = []
        for shed_name in sorted_sheds:
            shed_sensors = sensors_by_shed[shed_name]

            table_header = [
                html.Thead(html.Tr([
                    html.Th("ID"),
                    html.Th("MAC Address"),
                    html.Th("Hardware"),
                    html.Th("Grid Location"),
                    html.Th("Status"),
                    html.Th("Actions")
                ]))
            ]

            rows = []
            for s in shed_sensors:
                badge_color = "success" if s.status.lower() == "active" else "warning"
                grid_loc = f"(X: {s.grid_x}, Y: {s.grid_y})" if s.grid_x and s.grid_y else "N/A"

                row = html.Tr([
                    # Wrap the ID in a dcc.Link
                    html.Td(
                        dcc.Link(html.Strong(
                            f"SEN-{s.id:03d}"), href=f"/sensors/{s.id}", className="text-decoration-none")
                    ),
                    html.Td(html.Code(s.mac_address)),
                    html.Td(f"{s.brand} {s.model}"),
                    html.Td(grid_loc),
                    html.Td(dbc.Badge(s.status.upper(),
                            color=badge_color, pill=True)),
                    html.Td([
                        # Add a View button that routes to the details page
                        dbc.Button(
                            "View", href=f"/sensors/{s.id}", size="sm", color="primary", className="me-2 py-0"),
                        dbc.Button("Reassign", size="sm",
                                   color="outline-secondary", className="py-0")
                    ])
                ], className="align-middle")
                rows.append(row)

            table_body = [html.Tbody(rows)]

            # Wrap each Shed's table in its own Card
            section_card = dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H5(shed_name, className="mb-0 text-primary")),
                    dbc.Table(table_header + table_body, hover=True,
                              responsive=True, className="mb-0")
                ], className="shadow-sm mb-4 overflow-hidden"),
                width=12
            )
            sections.append(section_card)

        return sections
