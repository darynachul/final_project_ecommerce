{{ config(
    materialized='view',
    tags=['hourly']
) }}

select
    item_id,
    order_id,
    product_id,
    quantity,
    cast(unit_price as double) as unit_price
from {{ ref('raw_order_items') }}