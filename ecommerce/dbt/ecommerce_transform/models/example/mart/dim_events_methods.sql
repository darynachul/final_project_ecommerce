{{ config(
    materialized='table',
    tags=['daily']
) }}

select distinct
    trim(lower(event_type)) as event_type
from {{ ref('stg_web_events') }}