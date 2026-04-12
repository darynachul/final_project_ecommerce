{{ config(
    materialized='table',
    tags=['daily']
) }}

with order_items as (
    select
        item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        quantity * unit_price as total_price
    from {{ ref('stg_order_items') }}
),

orders as (
    select
        order_id,
        customer_id,
        status,
        ordered_at
    from {{ ref('stg_orders') }}
),

payments as (
    select
        order_id,
        amount as revenue,
        method as payment_method
    from {{ ref('stg_payments') }}
)

select
    oi.item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.total_price,
    o.customer_id,
    o.status,
    o.ordered_at,
    p.revenue,
    p.payment_method
from order_items oi
left join orders o
    on oi.order_id = o.order_id
left join payments p
    on oi.order_id = p.order_id