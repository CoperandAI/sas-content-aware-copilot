/*********************************************************************/
/********* DAILY NEW CUSTOMER REPORT                          ********/
/*********************************************************************/


PROC PRINTTO LOG="&logpath.\ADV_R003_NEW_CUSTOMER_DAILY_&RUN_DATE..LOG" NEW;
RUN;

PROC SQL;
    CREATE TABLE work.new_customers_report AS
    SELECT 
        c.CustomerKey,
        c.FirstName, c.LastName,
        c.EmailAddress,
        g.City, g.StateProvinceName, g.EnglishCountryRegionName AS Country,
        c.DateFirstPurchase
    FROM sas_dw.DimCustomer c
    JOIN sas_dw.DimGeography g ON c.GeographyKey = g.GeographyKey
    WHERE c.DateFirstPurchase = "&report_date";
QUIT;

/* Summary */
PROC FREQ DATA=work.new_customers_report;
    TABLES Country / OUT=work.new_customers_summary NOPRINT;
RUN;

/* Export to CSV */
PROC EXPORT DATA=work.new_customers_report
    OUTFILE="&reportpath\ADV_R003_NEW_CUSTOMER_DAILY_&run_date..csv"
    DBMS=CSV REPLACE;
    PUTNAMES=YES;
RUN;

/* Export to CSV */
PROC EXPORT DATA=work.new_customers_summary
    OUTFILE="&reportpath\ADV_R003_NEW_CUSTOMER_DAILY_SUMMARY_&run_date..csv"
    DBMS=CSV REPLACE;
    PUTNAMES=YES;
RUN;


PROC PRINTTO;
RUN;

