{{ config(
    materialized='table',
    tags=['daily']
) }}

select distinct
    product_id,
    trim(name) as name,
    trim(category) as category,
    cast(price as numeric) as price,
    cast(stock as integer) as stock,
    cast(created_at as date) as created_at
from {{ ref('stg_products') }}