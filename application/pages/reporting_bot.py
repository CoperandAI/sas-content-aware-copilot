import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
# Chatbot UI


def reporting_bot_ui():

    return html.Div([
        html.H6("Ask Your Data", className="display-6"),
        dbc.InputGroup([
            dbc.Input(id='user-input', type='text',
                      placeholder='Type your message...', style={'flex': 1}),
            dbc.Button('Send', id='send-button', n_clicks=0, style={
                       'backgroundColor': '#673ab7', 'borderColor': '#673ab7', 'color': 'white'})
        ], style={"width": "90%", "max-width": "950px", "margin": "10px auto"}),
        html.Div(id="chat-output", style={
            "width": "90%", "max-width": "1000px", "height": "70vh",
            "margin": "auto", "overflow-y": "auto", "border": "1px solid #ccc",
            "padding": "10px", "borderRadius": "5px"
        })

    ])
