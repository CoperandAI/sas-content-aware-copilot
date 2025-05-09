# ✅ Import existing database connection
from application.database.db_connection import conn, cursor


def create_all_tables():
    """Creates necessary application tables if they do not exist."""



    # ✅ High-Level Daily Batch Summary
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_level_daily_batch (
            batch_date TEXT PRIMARY KEY,
            total_reports INTEGER,
            successful_reports INTEGER,
            failed_reports INTEGER
        )
    ''')

    # ✅ Summary Report
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summary_report (
            batch_date TEXT,
            report_name TEXT,
            warnings INTEGER,
            errors INTEGER,
            PRIMARY KEY (batch_date, report_name)
        )
    ''')

    # ✅ Detailed Report
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detailed_report (
            batch_date TEXT,
            report_name TEXT,
            issue_type TEXT,
            analysis TEXT,
            resolution TEXT,
            PRIMARY KEY (batch_date, report_name, issue_type)
        )
    ''')

    # reconciliation type
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reconciliation_type (
        reconciliation_name TEXT,
        module_name TEXT,
        function_name TEXT,
        description TEXT,
        json_file TEXT
        )           
    ''')

   # ✅ Reconciliation Summary Table 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reconciliation_summary (
            report_name TEXT,
            report_date TEXT,
            status TEXT,
            description TEXT
        )
    ''')


# ✅ Commit Changes
conn.commit()
print("✅ Database tables created successfully.")
