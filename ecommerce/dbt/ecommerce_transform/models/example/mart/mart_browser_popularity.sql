{{config(tags=['daily'])}}

with browser_ as (
    select browser,
        device,
        count(event_id) as clicks
    from {{ref("stg_web_events")}}
    group by browser, device
)

select 
    browser,
    device,
    clicks,
    round(clicks * 100.0 / sum(clicks) over (), 2) as traffic_percent
from browser_
order by clicks desc