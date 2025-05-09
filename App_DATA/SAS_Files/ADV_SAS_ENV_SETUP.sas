/*********************************************************************/
/******** Setup SAS Environment                              *********/
/*********************************************************************/

/* Paths */

%let rootpath=Z:\Shared with VM\Log_Analytics;
%let logpath=&rootpath\sas_logs;

%let stgpath=&rootpath\sas_data\staging;
%let dwpath=&rootpath\sas_data\ADV_DW;
%let martpath=&rootpath\sas_data\data_mart;
%let control_lib=&rootpath\sas_data\control_lib;
%let reportpath=&rootpath\reports;
%let reconcilpath=&rootpath\reconciliation;
%let codepath=&rootpath\sas_code;
%put 
&=stgpath
&=dwpath
&=martpath
&=control_lib
&=reportpath
&=codepath
;

/* libraries */

libname adv_dw oledb init_string="Provider=SQLOLEDB;
Password=sas_user123;
Persist Security Info=True;
User ID=sas_user;
Initial Catalog=AdventureWorksDW2022;
Data Source=192.168.121.1;";

libname adv_OLTP oledb init_string="Provider=SQLOLEDB;
Password=sas_user123;
Persist Security Info=True;
User ID=sas_user;
Initial Catalog=AdventureWorks2022;
Data Source=192.168.121.1;";

libname stg "&stgpath.";
libname mart "&martpath.";
libname sas_dw "&dwpath";
libname cntl_lib "&control_lib";

/* macro variables*/
%LET run_date=&sysdate;

