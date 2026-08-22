"""
app.py

Main entry point for the BROIndex Dash application.
Initializes the app, sets up the multi-page routing layout, the persistent sidebar navigation,
and a global interval for simulating 5-second sensor data polling.
"""

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Initialize the Dash app.
# use_pages=True enables Dash's built-in multi-page routing capabilities.
# We include Bootstrap CSS and Bootstrap Icons for styling and UI components.
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)

# Application layout configuration
app.layout = html.Div([
    # Global polling interval: 5 seconds (5000 milliseconds)
    # This component will run in the background and can be used in callbacks
    # to trigger UI and database updates across the application.
    dcc.Interval(
        id='global-interval',
        interval=5000,
        n_intervals=0
    ),

    dbc.Row([
        # Persistent Left Sidebar Navigation
        dbc.Col(
            html.Div([
                html.H3("BROIndex", className="text-center my-4"),
                html.Hr(),
                # dbc.Nav creates a vertical list of navigation links
                dbc.Nav(
                    [
                        dbc.NavLink(
                            [html.I(className="bi bi-house me-2"), "Overview"], href="/", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-building me-2"),
                                    "Sheds"], href="/sheds", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-cpu me-2"),
                                    "Sensors"], href="/sensors", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-box-seam me-2"),
                                    "Batches"], href="/batches", active="exact"),
                        dbc.NavLink([html.I(className="bi bi-exclamation-triangle me-2"),
                                    "Alerts"], href="/alerts", active="exact"),
                        dbc.NavLink(
                            [html.I(className="bi bi-gear me-2"), "Admin"], href="/admin", active="exact"),
                    ],
                    vertical=True,
                    pills=True,  # Active links get a pill-shaped background highlight
                ),
            ], className="bg-light", style={"height": "100vh", "padding": "20px", "position": "fixed", "width": "16.666667%"}),
            width=2,
            className="p-0"
        ),

        # Main Page Content Container
        # Offset by 2 columns to make room for the fixed sidebar
        dbc.Col(
            html.Div(dash.page_container, className="p-4"),
            width={"size": 10, "offset": 2}
        )
    ], className="g-0")  # g-0 removes standard Bootstrap gutter spacing between columns
])

if __name__ == '__main__':
    # Run the local lightweight development server
    app.run(debug=True)
