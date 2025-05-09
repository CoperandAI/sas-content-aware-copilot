import os
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# ✅ Reconciliation Function: Daily to Weekly CSV
def reconcile__weekly_sales(REPORT_PATH, DB_PATH, TABLE_NAME, weekly_report_date, weekly_report, daily_report, var1, var2):

    """
    Reconciles daily sales data for a week against the weekly sales summary.

    Args:
    - weekly_report_date (str): Date in 'DDMMMYYYY' format (e.g., "14MAY2012")

    Returns:
    - str: Reconciliation result.
    """
    try:
        # ✅ Convert weekly report date to datetime
        weekly_date_obj = datetime.strptime(weekly_report_date, "%d%b%Y")

        # ✅ Initialize reconciliation totals
        daily_total_sales = 0.0
        daily_total_orders = 0.0

        # ✅ Load Daily Reports (for past 7 days)
        for i in range(7):
            daily_date = (weekly_date_obj - timedelta(days=i)).strftime("%d%b%Y")
            daily_report_path = os.path.join(REPORT_PATH, f"{daily_report}_{daily_date}.csv")

            if os.path.exists(daily_report_path):
                daily_df = pd.read_csv(daily_report_path)

                # ✅ Ensure correct numeric format
                daily_df[f"{var1}"] = daily_df[f"{var1}"].replace('[\$,]', '', regex=True).astype(float)
                daily_df[f"{var2}"] = daily_df[f"{var2}"].astype(float)

                # ✅ Accumulate sales and order totals
                daily_total_sales += daily_df[f"{var1}"].sum()
                daily_total_orders += daily_df[f"OrderQuantity_Sum"].sum()

        # ✅ Load Weekly Report
        weekly_report_path = os.path.join(REPORT_PATH, f"{weekly_report}_{weekly_report_date}.csv")

        if not os.path.exists(weekly_report_path):
            return f"❌ Weekly report not found: {weekly_report_path}"

        weekly_df = pd.read_csv(weekly_report_path)

        # ✅ Ensure correct numeric format
        weekly_df[f"{var1}"] = weekly_df[f"{var1}"].replace('[\$,]', '', regex=True).astype(float)
        weekly_df[f"{var2}"] = weekly_df[f"{var2}"].astype(float)

        weekly_total_sales = weekly_df[f"{var1}"].sum()
        weekly_total_orders = weekly_df[f"OrderQuantity_Sum"].sum()

        # ✅ Compare Totals
        sales_match = abs(daily_total_sales - weekly_total_sales) < 0.1  # Allow slight rounding difference
        orders_match = abs(daily_total_orders - weekly_total_orders) < 0.1

        reconciliation_status = "PASSED" if sales_match and orders_match else "FAILED"
        description = f"Daily {var1}: {daily_total_sales:.1f}, Weekly {var1}: {weekly_total_sales:.1f} | "
        description += f"Daily {var2}: {daily_total_orders:.1f}, Weekly {var2}: {weekly_total_orders:.1f}"

        # ✅ Save Results to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                report_name TEXT,
                report_date TEXT,
                status TEXT,
                description TEXT
            )
        ''')

        # ✅ Overwrite any existing record for this weekly report
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE report_date = ?", (weekly_report_date,))
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} (report_name, report_date, status, description) 
            VALUES (?, ?, ?, ?)
        ''', ("Sales Daily to Weekly Reconciliation", weekly_report_date, reconciliation_status, description))

        conn.commit()
        conn.close()

        return f"Reconciliation {reconciliation_status}: {description}"

    except Exception as e:
        return f"❌ Error during reconciliation: {str(e)}"