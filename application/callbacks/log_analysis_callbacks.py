import sqlite3
import pandas as pd
import re
import os
import dash_table
import plotly.express as px
from dash import html, dcc, Input, Output, State
from application.database.db_connection import conn, cursor
from application.functions.log_analysis_functions import analyze_log, get_llm_analysis
import markdown


def register_log_analysis_callbacks(app):
    @app.callback(
        Output("analysis-output", "children"),
        Input("run-analysis", "n_clicks"),
        State("batch-date", "value")
    )
    def log_analytics_run(n_clicks, batch_date):
        if n_clicks > 0 and batch_date:
            log_dir = "APP_DATA/Logs"
            total_reports = 0
            successful_reports = 0
            failed_reports = 0
            summary_data = []
            detailed_data = []

            # ✅ Clear existing data for the batch date
            cursor.execute(
                "DELETE FROM summary_report WHERE batch_date = ?", (batch_date,))
            cursor.execute(
                "DELETE FROM detailed_report WHERE batch_date = ?", (batch_date,))
            conn.commit()

            log_files = [f for f in os.listdir(
                log_dir) if batch_date.lower() in f.lower()]

            for log_file in log_files:
                log_path = os.path.join(log_dir, log_file)
                total_reports += 1

                # ✅ Extract errors & warnings from log
                warnings, errors, error_msgs, warning_msgs = analyze_log(
                    log_path)

                # ✅ Add to summary report
                summary_data.append((batch_date, log_file, warnings, errors))

                if errors > 0 or warnings > 0:
                    failed_reports += 1

                    # ✅ Get AI-powered error analysis
                    analysis_results = get_llm_analysis(
                        log_path, error_msgs, warning_msgs)

                    # ✅ Store analysis & resolutions in detailed report
                    for issue_type, analysis, resolution in analysis_results:
                        detailed_data.append(
                            (batch_date, log_file, issue_type, analysis, resolution))

                        # ✅ Insert into `detailed_report` in SQLite
                        cursor.execute("""
                            INSERT INTO detailed_report (batch_date, report_name, issue_type, analysis, resolution)
                            VALUES (?, ?, ?, ?, ?)
                        """, (batch_date, log_file, issue_type, analysis, resolution))
                    conn.commit()

                else:
                    successful_reports += 1

            # ✅ Store Summary in Database
            if summary_data:
                df_summary = pd.DataFrame(summary_data, columns=[
                    "batch_date", "report_name", "warnings", "errors"])
                # Delete only records with the same batch date to prevent overwriting all data
                cursor.execute(
                    "DELETE FROM summary_report WHERE batch_date = ?", (batch_date,))
                conn.commit()
                # Append new batch data
                df_summary.to_sql("summary_report", conn,
                                  if_exists="append", index=False)

                cursor.execute("REPLACE INTO high_level_daily_batch VALUES (?, ?, ?, ?)",
                               (batch_date, len(log_files), successful_reports, failed_reports))
                conn.commit()

            # ✅ Ensure df_detailed is always initialized
            if detailed_data:
                df_detailed = pd.DataFrame(detailed_data, columns=[
                    "batch_date", "report_name", "issue_type", "analysis", "resolution"])
                # Delete only records for the same batch date to prevent overwriting all data
                cursor.execute(
                    "DELETE FROM detailed_report WHERE batch_date = ?", (batch_date,))
                conn.commit()
                # Append new batch data
                df_detailed.to_sql("detailed_report", conn,
                                   if_exists="append", index=False)
            else:
                df_detailed = pd.DataFrame(columns=[
                    "batch_date", "report_name", "issue_type", "analysis", "resolution"])  # Empty DataFrame

            # ✅ Remove "Analysis:" and "Resolution:" but preserve bullet points
            df_detailed["analysis"] = df_detailed["analysis"].apply(lambda x: re.sub(
                r"^- \*\*Analysis\*\*:\s*", "", x) if isinstance(x, str) else x)
            df_detailed["resolution"] = df_detailed["resolution"].apply(lambda x: re.sub(
                r"^- \*\*Resolution\*\*:\s*", "", x) if isinstance(x, str) else x)

            # ✅ Ensure Markdown Formatting
            detailed_df_table = dash_table.DataTable(
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
                style_table={
                    "overflowX": "auto",
                    "maxHeight": "400px", "overflowY": "auto"
                },
                style_cell={
                    "whiteSpace": "normal", "textAlign": "left"
                },
                style_data=[
                    {"if": {"column_id": "analysis"}, "textAlign": "left"},
                    {"if": {"column_id": "resolution"}, "textAlign": "left"}               
                ],
                style_header={
                    "fontWeight": "bold",  # Make headers bold
                    "backgroundColor": "#f2f2f2"  # Light gray header background
                }
            )

            # ✅ Dash Tables for UI Output
            summary_table = dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in df_summary.columns],
                data=df_summary.to_dict("records"),
                style_table={"overflowX": "auto"}
            )

            # ✅ Dash Table for Detailed Report
            detailed_table = dash_table.DataTable(
                columns=[
                    {"name": "Batch Date", "id": "batch_date"},
                    {"name": "Report", "id": "report_name"},
                    {"name": "Issue Type", "id": "issue_type"},
                    {"name": "Root Cause", "id": "analysis", "presentation": "markdown"},
                    {"name": "Suggested Fix", "id": "resolution", "presentation": "markdown"}       
                ],
                data=df_detailed.to_dict("records"),
                style_table={"overflowX": "auto", "maxHeight": "400px", "overflowY": "auto"},
                style_cell={"whiteSpace": "normal", "textAlign": "left"},
                style_data_conditional=[
                    {"if": {"column_id": "analysis"}, "textAlign": "left"},
                    {"if": {"column_id": "resolution"}, "textAlign": "left"}
                ]
            )

            # ✅ Pie Chart (Success vs Failure Rate)
            pie_chart = dcc.Graph(figure=px.pie(
                values=[successful_reports, failed_reports],
                names=["Successful", "Failed"],
                title=f"Daily Batch {batch_date} Success Rate"
            ))

            return html.Div([
                html.P(f"Log analysis for {batch_date} completed."),
                summary_table,
                html.Br(),
                html.P(f"Datailed Report On Errors and Warnings for {batch_date}"),
                detailed_table,
                pie_chart
            ])

        return ""
