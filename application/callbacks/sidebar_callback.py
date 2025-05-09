from dash import Input, Output, html
import os
from application.pages.sidebar import generate_file_tree  # Ensure this function is correctly imported

APP_DATA_DIR = "APP_DATA"

def register_sidebar_callbacks(app):
    """Register sidebar callbacks to avoid circular imports."""
    
    @app.callback(
        Output("file-content", "children"),
        Input("file-explorer", "value")
    )
    def update_file_view(selected_path):
        if not selected_path:
            return "Select a folder to view contents."

        full_path = os.path.join(APP_DATA_DIR, selected_path)

        if os.path.isdir(full_path):
            items = os.listdir(full_path)
            return html.Ul([
                html.Li(
                    html.A(item, href=f"/open-file/{os.path.join(selected_path, item)}", target="_blank")
                ) if os.path.isfile(os.path.join(full_path, item)) else html.Li(item)
                for item in items
            ])
        
        return "No files in this directory."

