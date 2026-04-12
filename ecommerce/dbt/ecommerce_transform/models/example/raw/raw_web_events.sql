{{ config(
    materialized='table',
    tags=['hourly']
) }}

select * from raw.web_events