
import pandas as pd
import sqlite3
import re
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
from application.database.db_connection import conn  # ✅ SQLite Connection
from application.functions.log_analysis_hist_functions import clean_markdown_text 

def register_display_log_hist_details(app):

    @app.callback(
        Output("log-details-output", "children"),
        Input("batch-history-table", "selected_rows"),
        State("batch-history-table", "data")
    )
    def display_log_hist_details(selected_rows, table_data):
        if not selected_rows:
            return ""

        row_index = selected_rows[0]  # Get selected row index
        selected_batch_date = table_data[row_index]["batch_date"]

        # Fetch Summary Report
        summary_query = "SELECT * FROM summary_report WHERE batch_date = ?"
        df_summary = pd.read_sql(
            summary_query, conn, params=(selected_batch_date,))

        # Fetch Detailed Report
        detailed_query = "SELECT * FROM detailed_report WHERE batch_date = ?"
        df_detailed = pd.read_sql(detailed_query, conn,
                              params=(selected_batch_date,))

        # Apply function to DataFrame
        df_detailed["analysis"] = df_detailed["analysis"].apply(
            clean_markdown_text)
        df_detailed["resolution"] = df_detailed["resolution"].apply(
            clean_markdown_text)

        # Fetch Success vs Failure Data
        summary_query = "SELECT successful_reports, failed_reports FROM high_level_daily_batch WHERE batch_date = ?"
        batch_data = pd.read_sql(
            summary_query, conn, params=(selected_batch_date,))
        success_count = batch_data["successful_reports"].iloc[0]
        failure_count = batch_data["failed_reports"].iloc[0]

        # Summary Table
        summary_table = dash_table.DataTable(
            columns=[
                {"name": "Batch Date", "id": "batch_date"},
                {"name": "Report", "id": "report_name"},
                {"name": "Warnings", "id": "warnings"},
                {"name": "Errors", "id": "errors"}
            ],
            data=df_summary.to_dict("records"),
            style_table={"overflowX": "auto",
                     "maxHeight": "400px", "overflowY": "auto"},
            # Default center alignment
            style_cell={"whiteSpace": "normal", "textAlign": "center"},
            style_data_conditional=[
                # Left align "Report Name"
                {"if": {"column_id": "report_name"}, "textAlign": "left"}
            ]
        )

        # Detailed Table
        detailed_table = dash_table.DataTable(
            columns=[
                {"name": "Batch Date", "id": "batch_date"},
                {"name": "Report", "id": "report_name"},
                {"name": "Issue Type", "id": "issue_type"},
                {"name": "Root Cause", "id": "analysis",
                 "presentation": "markdown"},  # Markdown applied
                {"name": "Suggested Fix", "id": "resolution",
                 "presentation": "markdown"}  # Markdown applied
            ],
            data=df_detailed.to_dict("records"),
            style_table={"overflowX": "auto",
                     "maxHeight": "400px", "overflowY": "auto"},
            # Wrap text & align left
            style_cell={"whiteSpace": "normal", "textAlign": "left"},
            style_data_conditional=[
                {"if": {"column_id": "analysis"}, "textAlign": "left"},
                {"if": {"column_id": "resolution"}, "textAlign": "left"}
            ]
        )

        # Pie Chart
        pie_chart = dcc.Graph(figure=px.pie(
            values=[success_count, failure_count],
            names=["Successful", "Failed"],
            title=f"Success Rate for {selected_batch_date}"
        ))

        return html.Div([
            html.H5(
                f"Batch Execution Summary for {selected_batch_date}", className="display-6"),
            summary_table,
            html.Hr(),
            html.H5("Detailed Report (Errors/Warnings)", className="display-6"),
            detailed_table,
            html.Hr(),
            pie_chart
        ])
