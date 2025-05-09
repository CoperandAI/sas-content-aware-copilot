/*********************************************************************/
/*****************/
/*********************************************************************/



%let rootpath=Z:\Shared with VM\Log_Analytics;
%let logpath=&rootpath\sas_logs;
%let codepath=&rootpath\sas_code;

%INCLUDE "&CODEPATH.\ADV_SAS_ENV_SETUP.sas";

%let run_date=14may2012;
/* Extract Sales Data */
%LET report_date = %SYSFUNC(PUTN("&run_date"d, YYMMDD10.));

%put &=report_date;



%INCLUDE "&codepath\ADV_R001_SALES_DAILY.SAS";
%INCLUDE "&codepath\ADV_R002_PRODUCT_INVENTORY_DAILY.SAS";
%INCLUDE "&codepath\ADV_R003_NEW_CUSTOMER_DAILY.SAS";
%INCLUDE "&codepath\ADV_R004_RESELLERS_PERFORMANCE_DAILY.SAS";
%INCLUDE "&codepath\ADV_R005_EMPL_SALES_PERFORMANCE_DAILY.SAS";