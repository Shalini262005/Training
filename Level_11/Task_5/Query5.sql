create database HRSystem;
USE hrsystem;
create table sales(sale_id int primary key,sale_date DATE,Amount Decimal(10,2));
INSERT into sales(sale_id,sale_date,Amount) values (1, '2023-10-01', 100),(2, '2023-10-02', 200),(3, '2023-10-03', 150),(4, '2023-10-04', 300);
select * from sales;
with october_sales as ( select sale_date,amount from sales where sale_date between '2023-10-01' and '2023-10-31')
select sale_date,sum(amount) over (order by sale_date) as running_total from october_sales;