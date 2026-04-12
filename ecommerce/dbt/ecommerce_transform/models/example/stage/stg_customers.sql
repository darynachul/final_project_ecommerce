{{ config(
    materialized='view',
    tags=['hourly']
) }}

select
    customer_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    lower(email) as email,
    country,
    city,
    cast(created_at as timestamp) as created_at
from {{ ref('raw_customers') }}