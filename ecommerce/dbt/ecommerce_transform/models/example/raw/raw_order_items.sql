{{ config(
    materialized='table',
    tags=['hourly']
) }}

select * from raw.order_items