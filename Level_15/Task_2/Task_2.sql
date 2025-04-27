use shopping;
SELECT 
    customer_id,
    COUNT(DISTINCT invoice_no) AS num_orders,
    SUM(quantity * price) AS total_spent
FROM 
    customer_shopping_data
GROUP BY 
    customer_id
HAVING 
    num_orders >= 5
ORDER BY 
    total_spent DESC
LIMIT 1;
