{{config(tags=['daily'])}}

with order_sums as (
    select 
        order_id,
        customer_id,
        count(item_id) as items_in_order,
        sum(total_price) as order_amount
    from {{ref("fct_order_items")}}
    group by order_id, customer_id
)

select *,
    avg(order_amount) over (partition by customer_id) as customer_avg_check,
    avg(order_amount) over () as general_avg_check
from order_sums