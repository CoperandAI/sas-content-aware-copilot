import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


def log_analytics_ui():
    return html.Div([
        html.H6("Run Log Analytics", className="display-6"),
        dbc.Input(id="batch-date", type="text", placeholder="Enter batch date (e.g., 08MAY2012)",
                  style={"width": "300px", "margin-bottom": "10px"}),
        dbc.Button("Run Analysis", id="run-analysis", n_clicks=0, style={
                   'backgroundColor': '#673ab7', 'borderColor': '#673ab7', 'color': 'white'}),
        html.Br(),
        html.Hr(),
        html.Div(id="analysis-output")
    ])
