"""
src/components/charts.py
Reusable Plotly graph components for data visualization.
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_dual_axis_telemetry_chart(df: pd.DataFrame) -> go.Figure:
    """
    Generates a dual-axis line chart for temperature and humidity.
    Takes a DataFrame containing 'recorded_at', 'temperature_c', and 'humidity_rh'.
    """
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if df.empty:
        # Return an empty figure with a message if no data is available
        fig.add_annotation(text="No telemetry data available",
                           showarrow=False, font={"size": 20})
        fig.update_layout(xaxis_visible=False, yaxis_visible=False)
        return fig

    # Add Temperature Trace (Primary Y-Axis)
    # Using red styling to align with the warm temperature cue concept
    fig.add_trace(
        go.Scatter(
            x=df['recorded_at'],
            y=df['temperature_c'],
            name="Temperature (°C)",
            line=dict(color="#d9534f", width=2)
        ),
        secondary_y=False,
    )

    # Add Humidity Trace (Secondary Y-Axis)
    # Using blue styling to align with the humidity cue concept
    fig.add_trace(
        go.Scatter(
            x=df['recorded_at'],
            y=df['humidity_rh'],
            name="Humidity (%)",
            line=dict(color="#0275d8", width=2)
        ),
        secondary_y=True,
    )

    # Update layout and axes titles
    fig.update_layout(
        title_text="24-Hour Environmental Telemetry",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update_yaxes(title_text="<b>Temperature</b> (°C)", secondary_y=False)
    fig.update_yaxes(title_text="<b>Humidity</b> (%)", secondary_y=True)

    return fig
