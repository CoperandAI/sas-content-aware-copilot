/*********************************************************************/
/*****************/
/*********************************************************************/

%let rootpath=Z:\Shared with VM\Log_Analytics;
%let logpath=&rootpath\sas_logs;
%let codepath=&rootpath\sas_code;

%INCLUDE "&CODEPATH.\ADV_SAS_ENV_SETUP.sas";

%let run_date=12Sep2014;
/* Extract Sales Data */
%LET report_date = %SYSFUNC(PUTN("&run_date"d, YYMMDD10.));

%put &=report_date;

PROC PRINTTO LOG="&logpath.\ADV_STG_DAILY_BATCH_&run_date..LOG" NEW;
RUN;


/* load customer operational table to the staging area*/

PROC SQL;
    CONNECT TO OLEDB AS ADV (INIT_STRING="Provider=SQLOLEDB;
        Password=sas_user123;
        Persist Security Info=True;
        User ID=sas_user;
        Initial Catalog=AdventureWorks2022;
        Data Source=192.168.121.1;");
    
    CREATE TABLE stg.customer AS
    SELECT * FROM CONNECTION TO ADV
    (
        SELECT * FROM Sales.Customer

    );

    DISCONNECT FROM ADV;
QUIT;


PROC PRINTTO;
RUN;