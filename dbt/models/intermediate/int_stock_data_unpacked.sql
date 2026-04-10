with staging_data as (
    select * from {{ ref('stg_stock_data') }}
),

unpacked as (
    select
        ticker,
        extraction_timestamp,

        -- Dictionary: Mapping tickers to full names
        case 
            when ticker = 'AAPL'  then 'Apple Inc.'
            when ticker = 'GOOGL' then 'Alphabet Inc.'
            when ticker = 'ORCL'  then 'Oracle Corporation'
            when ticker = 'META'  then 'Meta Platforms, Inc.'
            when ticker = 'MSFT'  then 'Microsoft Corporation'
            else ticker
        end as company_name,

        -- Unix Millis to Date conversion (Atomic)
        to_timestamp((raw_json ->> 't')::bigint / 1000)::date as trading_date,

        (raw_json ->> 'o')::decimal as open_price,
        (raw_json ->> 'c')::decimal as close_price,
        (raw_json ->> 'h')::decimal as high_price,
        (raw_json ->> 'l')::decimal as low_price,
        
    from staging_data
)

select * from unpacked