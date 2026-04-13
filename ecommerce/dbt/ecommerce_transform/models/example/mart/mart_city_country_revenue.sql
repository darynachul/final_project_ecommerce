{{config(materialized='table', tags=['daily'])}}

select 
    c.country,
    c.city,
    count(distinct f.customer_id) as active_customers,
    count(f.order_id) as total_orders,
    sum(f.total_price) as total_price,
    avg(f.total_price) as avg_order_value
from {{ref("fct_order_items")}} f
join {{ref("dim_customers")}} c on f.customer_id = c.customer_id
group by country, city
order by total_price desc