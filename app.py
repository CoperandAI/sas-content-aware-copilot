import os
import sys
from dotenv import load_dotenv
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from flask import send_file, Flask

from application.pages.sidebar import sidebar_ui
from application.pages.navbar import navbar_ui
from application.pages.content import content_ui 
from application.callbacks import sidebar_callback
from application.routes.file_routes import register_file_routes
from application.pages.reporting_bot import reporting_bot_ui
from application.callbacks.reporting_bot_callback import register_reporting_bot_callback
from application.database.create_app_tables import create_all_tables
from application.pages.log_analysis import log_analytics_ui
from application.callbacks.log_analysis_callbacks import register_log_analysis_callbacks
from application.pages.log_analysis_hist import log_analytics_history_ui
from application.callbacks.log_analysis_hist_callbacks import register_display_log_hist_details

sys.path.append("application")

load_dotenv()

# ✅ Get OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Initialize Dash app with Flask server
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ✅ Application Data Directory
APP_DATA_DIR = "APP_DATA"


REPORT_PATH = "App_DATA/Reports"
print(os.path.abspath(REPORT_PATH))


# create all tables
create_all_tables()

# ✅ Full Layout
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar_ui(),
    sidebar_ui(),
    content_ui()
])

# ✅ Callback to Update File Explorer View with Clickable Files
sidebar_callback.register_sidebar_callbacks(app)

# ✅ File Download Route
register_file_routes(server) 

# ✅ Page Router
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return reporting_bot_ui()
    elif pathname == "/reporting-bot":
        return reporting_bot_ui()
    elif pathname == "/run-validator":
        return html.H2("Run Validator - Enterprise Feature")
    elif pathname == "/validation-history":
        return html.H2("Validation History -  Enterprise Feature")
    elif pathname == "/log-analytics":
        return log_analytics_ui()
    elif pathname == "/log-analytics-history":
        return log_analytics_history_ui()
    elif pathname == "/automation":
        return html.H2("Automation -  Enterprise Feature")
    elif pathname == "/help":
        return html.H2("Help -  Enterprise Feature")
    return html.H2(" Enterprise Feature")


# ✅ Register chatbot callbacks
register_reporting_bot_callback(app)
register_log_analysis_callbacks(app)
register_display_log_hist_details(app)

# ✅ Run the Dash App
if __name__ == '__main__':
    app.run_server(debug=False)
