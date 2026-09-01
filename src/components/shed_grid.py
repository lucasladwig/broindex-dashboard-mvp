"""
src/components/shed_grid.py
Generates interactive grid layouts for visualizing sensor placement within sheds.
"""
from dash import html


def create_sensor_grid(rows: int, cols: int, assigned_sensors: dict) -> html.Div:
    """
    Creates a visual grid for a shed using CSS Grid.
    assigned_sensors is a dictionary mapping (x, y) coordinates to sensor data.
    """
    grid_cells = []

    # Iterate through Y (rows) and X (columns) to build a flat list of cells
    for y in range(1, rows + 1):
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

            # Create the cell div (no longer wrapped in a dbc.Col)
            cell = html.Div(
                cell_content,
                className=f"border p-2 text-center {cell_color} rounded shadow-sm",
                style={
                    "height": "80px",
                    "cursor": "pointer",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "flexDirection": "column"
                },
                # Retain ID structure for Dash pattern-matching callbacks
                id={"type": "grid-cell", "x": x, "y": y}
            )
            grid_cells.append(cell)

    # Wrap the flat list of cells in a CSS Grid container
    return html.Div(
        grid_cells,
        className="mt-3",
        style={
            "display": "grid",
            # Forces exactly 10 equal columns
            "gridTemplateColumns": f"repeat({cols}, 1fr)",
            "gap": "10px"
        }
    )
