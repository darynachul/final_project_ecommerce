{{ config(
    materialized='view',
    tags=['hourly']
) }}

select
    payment_id,
    order_id,
    lower(method) as method,
    lower(status) as status,
    cast(amount as double) as amount,
    paid_at
from {{ ref('raw_payments') }}