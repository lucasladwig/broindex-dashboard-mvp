"""
src/components/shed_grid.py
Generates interactive grid layouts for visualizing sensor placement within sheds.
"""
from dash import html
import dash_bootstrap_components as dbc


def create_sensor_grid(rows: int, cols: int, assigned_sensors: dict) -> html.Div:
    """
    Creates a visual grid for a shed.
    assigned_sensors is a dictionary mapping (x, y) coordinates to sensor data.
    """
    grid_rows = []

    for y in range(1, rows + 1):
        row_cells = []
        for x in range(1, cols + 1):
            # Check if a sensor is assigned to this specific (x, y) coordinate
            sensor_info = assigned_sensors.get((x, y))

            if sensor_info:
                # Cell with a sensor assigned
                cell_content = html.Div([
                    html.Strong(f"Sensor {sensor_info['id']}"),
                    html.Br(),
                    html.Small(
                        f"{sensor_info['temp']}°C | {sensor_info['humidity']}%")
                ])
                cell_color = "bg-success text-white"  # Green for active/normal
            else:
                # Empty cell available for assignment
                cell_content = html.Div("Empty", className="text-muted")
                cell_color = "bg-light"

            cell = dbc.Col(
                html.Div(
                    cell_content,
                    className=f"border p-2 text-center {cell_color} rounded",
                    style={"height": "80px", "cursor": "pointer", "display": "flex",
                           "alignItems": "center", "justifyContent": "center", "flexDirection": "column"},
                    # ID structure for Dash pattern-matching callbacks
                    id={"type": "grid-cell", "x": x, "y": y}
                ),
                width=True,
                className="p-1"
            )
            row_cells.append(cell)

        grid_rows.append(dbc.Row(row_cells, className="g-0"))

    return html.Div(grid_rows, className="mt-3")
