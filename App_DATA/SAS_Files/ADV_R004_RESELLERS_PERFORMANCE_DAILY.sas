/*********************************************************************/
/***********  DAILY RESELLERS PERFORMANCE REPORT                ******/
/*********************************************************************/


PROC PRINTTO LOG="&logpath.\ADV_R004_RESELLERS_PERFORMANCE_DAILY_&RUN_DATE..LOG" NEW;
RUN;
 

PROC SQL;
    CREATE TABLE work.reseller_report AS
    SELECT 
        r.ResellerName,
        d.FullDateAlternateKey AS OrderDate,
        f.OrderQuantity,
        f.SalesAmount
    FROM sas_dw.FactResellerSales f
    JOIN sas_dw.DimDate d ON f.OrderDateKey = d.DateKey
    JOIN sas_dw.DimReseller r ON f.ResellerKey = r.ResellerKey
    WHERE d.FullDateAlternateKey = "&report_date";
QUIT;

PROC MEANS DATA=work.reseller_report MEAN SUM MAXDEC=2;
    VAR OrderQuantity SalesAmount;
    CLASS ResellerName;
RUN;

/* Export to CSV */
PROC EXPORT DATA=work.reseller_report
    OUTFILE="&reportpath\ADV_R004_RESELLERS_PERFORMANCE_DAILY_&run_date..csv"
    DBMS=CSV REPLACE;
    PUTNAMES=YES;
RUN;

PROC PRINTTO;
RUN;

