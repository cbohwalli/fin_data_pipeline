with source as (
    select * from {{ source('polygon_api', 'ticker_data') }}
)

select
    -- 1. Identity
    ticker_symbol as ticker,

    -- 2. Timestamps
    received_at as extraction_timestamp,

    -- 3. Data Blobs
    json_payload as raw_json

from source