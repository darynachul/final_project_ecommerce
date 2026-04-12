{{ config(
    materialized='view',
    tags=['hourly']
) }}
select
    order_id,
    customer_id,
    lower(status) as status,
    ordered_at,
    shipped_at
from {{ ref('raw_orders') }}