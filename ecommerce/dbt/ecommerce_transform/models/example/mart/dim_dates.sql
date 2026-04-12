{{ config(
    materialized='table',
    tags=['daily']
) }}

select distinct
    date(ordered_at) as date,
    cast(strftime(ordered_at, '%Y') as integer) as year,
    cast(strftime(ordered_at, '%m') as integer) as month,
    cast(strftime(ordered_at, '%d') as integer) as day,
    strftime(ordered_at, '%Y-%m') as year_month,
    strftime(ordered_at, '%w') as day_of_week
from {{ ref('stg_orders') }}