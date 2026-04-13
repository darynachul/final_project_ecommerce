{{config(tags=['daily'])}}

with product_sales as (
    select 
        p.category,
        p.name as product_name,
        sum(i.quantity) as units_sold,
        sum(i.total_price) as total_profit
    from {{ref("fct_order_items")}} i
    join {{ref("dim_products")}} p on i.product_id = p.product_id
    group by category, product_name
)

select *, rank() over (partition by category order by total_profit desc) as rank_by_category
from product_sales