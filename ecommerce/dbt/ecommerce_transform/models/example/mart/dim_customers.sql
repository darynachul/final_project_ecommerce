{{ config(
    materialized='table',
    tags=['daily']
) }}

select distinct
    customer_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    lower(trim(email)) as email,
    trim(country) as country,
    trim(city) as city,
    cast(created_at as date) as created_at
from {{ ref('stg_customers') }}