/*********************************************************************/
/**********  DAILY PRODUCT INVENTORY REPORT                    *******/
/*********************************************************************/


PROC PRINTTO LOG="&logpath.\ADV_R002_PRODUCT_INVENTORY_DAILY_&RUN_DATE..LOG" NEW;
RUN;

/* Extract Product Inventory */
PROC SQL;
    CREATE TABLE work.inventory_report AS
    SELECT 
        p.EnglishProductName AS ProductName,
        i.UnitsBalance AS QuantityOnHand,
        i.UnitCost,
        d.FullDateAlternateKey AS InventoryDate
    FROM sas_dw.FactProductInventory i
    JOIN sas_dw.DimProduct p ON i.ProductKey = p.ProductKey
    JOIN sas_dw.DimDate d ON i.DateKey = d.DateKey
    WHERE d.FullDateAlternateKey = "&report_date";
QUIT;

/* Summary Statistics */
PROC MEANS DATA=work.inventory_report MEAN MIN MAX MAXDEC=2;
    VAR QuantityOnHand UnitCost;
RUN;


/* Export to CSV */
PROC EXPORT DATA=work.inventory_report
    OUTFILE="&reportpath\ADV_R002_PRODUCT_INVENTORY_DAILY_&run_date..csv"
    DBMS=CSV REPLACE;
    PUTNAMES=YES;
RUN;

PROC PRINTTO;
RUN;

