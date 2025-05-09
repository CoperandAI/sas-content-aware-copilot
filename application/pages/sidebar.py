import dash
from dash import html, dcc
from application.functions.coperand_file_explorer import generate_file_tree  # Ensure correct import

APP_DATA_DIR = "APP_DATA"  # Define or import as needed

def sidebar_ui():
    return html.Div([
        html.H5("File Explorer", className="display-6"),
        dcc.Dropdown(
            id="file-explorer",
            options=[{"label": node["label"], "value": node["value"]} for node in generate_file_tree(APP_DATA_DIR)],
            placeholder="Select a folder",
            multi=False
        ),
        html.Div(id="file-content")
    ], style={
        "width": "250px", "padding": "20px", "background": "#F4F6F9",
        "height": "100vh", "overflow-y": "auto", "position": "fixed", "top": "56px", "left": "0"
    })
