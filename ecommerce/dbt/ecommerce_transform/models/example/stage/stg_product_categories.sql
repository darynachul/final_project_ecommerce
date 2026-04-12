{{ config(
    materialized='view',
    tags=['hourly']
) }}

with source as (
    select * from {{ ref('product_categories') }}
)

select
    row_number() over (order by category_name) as category_id,
    category_name,
    department,
    margin_level,
    is_priority
from source