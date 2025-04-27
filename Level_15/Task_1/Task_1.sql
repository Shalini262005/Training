create database shopping;
use shopping;
SELECT 
    SUM(quantity * price) / COUNT(DISTINCT invoice_no) AS AOV
FROM 
    customer_shopping_data;
