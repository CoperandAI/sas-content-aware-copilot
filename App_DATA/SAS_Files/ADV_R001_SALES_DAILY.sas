/*********************************************************************/
/********** DAILY SALES REPORT                                 *******/
/*********************************************************************/




PROC PRINTTO LOG="&logpath.\ADV_R001_SALES_DAILY_&RUN_DATE..LOG" NEW;
RUN;

/* Extract Sales Data */
%LET report_date = %SYSFUNC(PUTN("&run_date"d, YYMMDD10.));

%put &=report_date;

PROC SQL;
    CREATE TABLE work.sales_report AS
    SELECT 
        f.SalesOrderNumber,
        d.FullDateAlternateKey AS OrderDate,
        c.FirstName || ' ' || c.LastName AS CustomerName,
        p.EnglishProductName AS ProductName,
        f.OrderQuantity,
        f.SalesAmount
    FROM sas_dw.FactInternetSales f
    JOIN sas_dw.DimDate d ON f.OrderDateKey = d.DateKey
    JOIN sas_dw.DimCustomer c ON f.CustomerKey = c.CustomerKey
    JOIN sas_dw.DimProduct p ON f.ProductKey = p.ProductKey
    WHERE d.FullDateAlternateKey = "&report_date";
	;
QUIT;


/* Summary Statistics */
PROC MEANS DATA=work.sales_report MEAN SUM MAXDEC=2;
    VAR OrderQuantity SalesAmount;
    OUTPUT OUT=work.sales_report_summary(DROP= _:) 
        MEAN=OrderQuantity_Mean SalesAmount_Mean
        SUM=OrderQuantity_Sum SalesAmount_Sum;
RUN;

/* Export to CSV */
PROC EXPORT DATA=work.sales_report
    OUTFILE="&reportpath\ADV_R001_SALES_DAILY_&run_date..csv"
    DBMS=csv REPLACE;
    PUTNAMES=YES;
RUN;

PROC EXPORT DATA=work.sales_report_summary
    OUTFILE="&reportpath\ADV_R001_SALES_DAILY_SUMMARY_&run_date..csv"
    DBMS=csv REPLACE;
    PUTNAMES=YES;
RUN;

PROC PRINTTO;
RUN;
