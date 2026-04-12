{{ config(
    materialized='view',
    tags=['hourly']
) }}

select
    product_id,
    name,
    category,
    cast(price as double) as price,
    stock,
    created_at
from {{ ref('raw_products') }}