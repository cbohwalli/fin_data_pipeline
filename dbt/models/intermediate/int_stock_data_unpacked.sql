with staging_data as (
    select 
        ticker,
        extraction_timestamp,
        jsonb_array_elements(raw_json::jsonb -> 'results') as daily_row
    from {{ ref('stg_stock_data') }}
),

unpacked as (
    select
        ticker,
        extraction_timestamp,

        (daily_row ->> 'c')::decimal as close_price,
        (daily_row ->> 'o')::decimal as open_price,
        (daily_row ->> 'h')::decimal as high_price,
        (daily_row ->> 'l')::decimal as low_price,
        to_timestamp((daily_row ->> 't')::bigint / 1000)::date as trading_date,

        -- Dictionary: Mapping tickers to full names
        case 
            when ticker = 'AAPL'  then 'Apple Inc.'
            when ticker = 'GOOGL' then 'Alphabet Inc.'
            when ticker = 'ORCL'  then 'Oracle Corporation'
            when ticker = 'META'  then 'Meta Platforms, Inc.'
            when ticker = 'MSFT'  then 'Microsoft Corporation'
            else ticker
        end as company_name
        
    from staging_data
)

select * from unpacked