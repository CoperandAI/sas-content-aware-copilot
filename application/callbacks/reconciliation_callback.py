import importlib
import sqlite3
import pandas as pd
from dash import Input, Output, State, html, dcc, dash_table
import dash_bootstrap_components as dbc

# ✅ Callback to Run Reconciliation
@app.callback(
    Output("reconciliation-output", "children"),
    Input("run-reconciliation", "n_clicks"),
    State("batch-date", "value"),
    State("reconciliation-type", "value"),
    State("first-report", "value"),
    State("second-report", "value"),
    State("location", "value"),
    prevent_initial_call=True
)
def run_reconciliation(n_clicks, batch_date, reconciliation_type, first_report, second_report, location):
    if not all([batch_date, reconciliation_type, first_report, second_report, location]):
        return html.P("❌ Please fill in all fields before running reconciliation.", style={"color": "red"})

    try:
        # ✅ Connect to SQLite DB
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # ✅ Retrieve module name & function name for the selected reconciliation type
        cursor.execute(
            "SELECT module_name, function_name FROM reconciliation_type WHERE reconciliation_name = ?",
            (reconciliation_type,)
        )
        result = cursor.fetchone()

        if not result:
            return html.P(f"❌ No reconciliation function found for {reconciliation_type}.", style={"color": "red"})

        module_name, function_name = result

        # ✅ Dynamically Import Module & Fetch Function
        module = importlib.import_module(f"application.reconciliation.{module_name}")
        reconciliation_function = getattr(module, function_name)

        # ✅ Define Paths
        REPORT_PATH = "APP_DATA/reports"
        DB_PATH = DB_FILE
        TABLE_NAME = "reconciliation_summary"

        # ✅ Execute Reconciliation Function
        result_message = reconciliation_function(
            REPORT_PATH, DB_PATH, TABLE_NAME, batch_date, first_report, second_report, "SalesAmount_Sum", "OrderQuantity_Sum"
        )

        # ✅ Fetch Updated Results from reconciliation_summary
        df_summary = pd.read_sql("SELECT * FROM reconciliation_summary ORDER BY report_date DESC", conn)
        conn.close()

        # ✅ Convert DataFrame to Dash Table
        reconciliation_table = dash_table.DataTable(
            columns=[
                {"name": "Report Name", "id": "report_name"},
                {"name": "Report Date", "id": "report_date"},
                {"name": "Status", "id": "status"},
                {"name": "Description", "id": "description"}
            ],
            data=df_summary.to_dict("records"),
            style_table={"overflowX": "auto", "maxWidth": "900px"},
            style_cell={"textAlign": "left", "padding": "10px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f2f2f2"}
        )

        return html.Div([
            html.P(f"✅ {result_message}", style={"color": "green", "font-weight": "bold"}),
            html.Hr(),
            html.H4("Reconciliation Summary"),
            reconciliation_table
        ])

    except Exception as e:
        return html.P(f"❌ Error during reconciliation: {str(e)}", style={"color": "red"})
