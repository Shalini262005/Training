USE shopping;
select*from customer_shopping_data;
select str_to_date(invoice_date, '%d/%m/%Y') as proper_date from customer_shopping_data;
select customer_id, year(str_to_date(invoice_date, '%d/%m/%Y')) as order_year, quarter(str_to_date(invoice_date, '%d/%m/%Y')) as order_quarter from customer_shopping_data;
select max(year(str_to_date(invoice_date, '%d/%m/%Y'))) as latest_year, max(quarter(str_to_date(invoice_date, '%d/%m/%Y'))) as latest_quarter from customer_shopping_data;
# the latest year and quarter are 2023 and 4
with customer_quarters as (
select customer_id, year(str_to_date(invoice_date, '%d/%m/%Y')) as order_year,
quarter(str_to_date(invoice_date, '%d/%m/%Y')) as order_quarter from customer_shopping_data),
latest_customers as (
select distinct customer_id from customer_quarters where order_year = 2023 and order_quarter = 4),
previous_customers as (
select distinct customer_id from customer_quarters where order_year = 2023 and order_quarter = 3)
select count(*) as repeat_customers from latest_customers where customer_id in (select customer_id from previous_customers);