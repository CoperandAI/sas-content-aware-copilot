/*********************************************************************/
/**********ADV WEEKLY BATCH                                    *******/
/*********************************************************************/



%let rootpath=Z:\Shared with VM\Log_Analytics;
%let logpath=&rootpath\sas_logs;
%let codepath=&rootpath\sas_code;

%INCLUDE "&CODEPATH.\ADV_SAS_ENV_SETUP.sas";

%let run_date=14may2012;
/* Extract Sales Data */
%LET report_date = %SYSFUNC(PUTN("&run_date"d, YYMMDD10.));
%LET report_pre7 = %SYSFUNC(PUTN(%SYSFUNC(INTNX(day, "&run_date"d, -6)), YYMMDD10.));

%put &=report_date 
     &=report_pre7
;



%INCLUDE "&codepath\ADV_R006_SALES_WEEKLY.SAS";
%INCLUDE "&codepath\ADV_R007_NEW_CUSTOMER_WEEKLY.SAS";
