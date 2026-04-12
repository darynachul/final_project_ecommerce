{{ config(
    materialized='table',
    tags=['hourly']
) }}

select * from raw.payments