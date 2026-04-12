{{ config(
    materialized='view',
    tags=['hourly']
) }}

select
    event_id,
    user_id as customer_id,
    lower(event_type) as event_type,
    cast(timestamp as timestamp) as event_time,
    lower(device) as device,
    lower(browser) as browser
from {{ ref('raw_web_events') }}