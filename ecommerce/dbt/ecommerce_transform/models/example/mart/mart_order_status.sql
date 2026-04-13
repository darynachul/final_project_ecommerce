{{config(tags=['daily'])}}

with status_data as (select
        status,
        count(distinct order_id) as total_orders,
        sum(total_price) as total_amount
    from {{ref("fct_order_items")}}
    group by status
)
select 
    status,
    total_orders,
    total_amount,
    round(total_orders * 100/ sum(total_orders) over (), 2) as orders_per
from status_data
order by total_orders desc