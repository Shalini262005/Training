use shopping;
with customer_spend as (
select customer_id, sum(quantity*price) as total_spent from customer_shopping_data group by customer_id)
select customer_id,total_spent, RANK() OVER (order by total_spent desc) as spend_rank from customer_spend order by spend_rank limit 5;
