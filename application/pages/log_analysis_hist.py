
import pandas as pd
import sqlite3
from dash import dash_table
from dash import dcc, html
import plotly.express as px
from application.database.db_connection import conn  # ✅ Import your database connection
  

def log_analytics_history_ui():
    # Fetch batch data from high_level_daily_batch table
    query = """
    SELECT batch_date, total_reports, successful_reports, failed_reports
    FROM high_level_daily_batch
    """
    df_batches = pd.read_sql(query, conn)

    # ✅ Convert batch_date to proper datetime format (from SAS-like format '08MAY2012')
    df_batches["batch_date"] = pd.to_datetime(
        df_batches["batch_date"], format="%d%b%Y", errors="coerce")

    # ✅ Sort by batch_date in descending order
    df_batches = df_batches.sort_values(by="batch_date", ascending=False)

    # ✅ Convert date back to string format for display
    df_batches["batch_date"] = df_batches["batch_date"].dt.strftime(
        "%d%b%Y").str.upper()

    # ✅ Limit to 10 reports (with scrollbar)
    table = dash_table.DataTable(
        id="batch-history-table",
        columns=[
            {"name": "Batch Date", "id": "batch_date"},
            {"name": "Total Reports", "id": "total_reports"},
            {"name": "Successful Reports", "id": "successful_reports"},
            {"name": "Failed Reports", "id": "failed_reports"}
        ],
        data=df_batches.to_dict("records"),  # Show ALL records
        row_selectable="single",
        style_table={"overflowX": "auto", "maxHeight": "400px",
                     "overflowY": "auto", "border": "1px solid #ddd"},
        style_cell={"textAlign": "center",
                    "fontSize": "14px", "padding": "8px"},
    )


# ✅ Bar Chart for Success vs Failure Rate (All Available Batches)
    bar_chart = dcc.Graph(
        figure=px.bar(
            df_batches,  # Use all records (sorted)
            x="batch_date",
            y=["successful_reports", "failed_reports"],
            title="Batch Performance - Latest 10 Batches",
            barmode="group",
            labels={"batch_date": "", "value": "", "variable": "Status"},
            height=400
        ).update_layout(
            # Rotates the x-axis labels by 45 degrees
            xaxis=dict(tickangle=-45),
            # Adjusts margins for better visibility
            margin=dict(l=40, r=40, t=40, b=100)
        )
    )

    return html.Div([
        html.H5(f"Log Analytics History", className="display-6"),
        table,
        html.Hr(),
        bar_chart,
        html.Div(id="log-details-output")  # Placeholder for detailed reports
    ])