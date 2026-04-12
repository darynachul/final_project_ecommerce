{{ config(
    materialized='table',
    tags=['daily']
) }}

select distinct
    trim(lower(method)) as payment_method
from {{ ref('stg_payments') }}