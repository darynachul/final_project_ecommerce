{{ config(
    materialized='table',
    tags=['daily']
) }}

select distinct
    cast(category_id as integer) as category_id,
    trim(category_name) as category_name
from {{ ref('stg_product_categories') }}