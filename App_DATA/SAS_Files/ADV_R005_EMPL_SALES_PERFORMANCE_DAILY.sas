/*********************************************************************/
/********   DAILY EMPLOYEE SALES PERFORMANCE REPORT          *********/
/*********************************************************************/



PROC PRINTTO LOG="&logpath.\ADV_R005_EMPL_SALES_PERFORMANCE_DAILY_&RUN_DATE..LOG" NEW;
RUN;

 

/* Extract Employee Sales */
PROC SQL;
    CREATE TABLE work.employee_report AS
    SELECT 
        e.EmployeeKey,
        e.FirstName, e.LastName,
        e.DepartmentName,
        d.FullDateAlternateKey AS SalesDate,
        f.SalesAmountQuota
    FROM sas_dw.FactSalesQuota f
    JOIN sas_dw.DimEmployee e ON f.EmployeeKey = e.EmployeeKey
    JOIN sas_dw.DimDate d ON f.DateKey = d.DateKey
    WHERE d.FullDateAlternateKey = "&report_date";
QUIT;

PROC MEANS DATA=work.employee_report MEAN SUM MAXDEC=2;
    VAR SalesAmountQuota;
    CLASS DepartmentName;
RUN;

/* Export to CSV */
PROC EXPORT DATA=work.employee_report
    OUTFILE="&reportpath\ADV_R005_EMPL_SALES_PERFORMANCE_DAILY_&run_date..csv"
    DBMS=CSV REPLACE;
    PUTNAMES=YES;
RUN;

PROC PRINTTO;
RUN;

