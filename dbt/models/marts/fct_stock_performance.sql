{{ config(
    materialized='table'
) }}

with historical_data as (
    select * from {{ ref('int_stock_data_unpacked') }}
),

sma_calculations as (
    select
        ticker,
        company_name,
        trading_date,
        open_price,
        close_price,
        high_price,
        low_price,
        
        -- SMA 7 for Close
        avg(close_price) over (
            partition by ticker 
            order by trading_date 
            rows between 6 preceding and current row
        ) as sma_7_close,

        -- SMA 7 for Open
        avg(open_price) over (
            partition by ticker 
            order by trading_date 
            rows between 6 preceding and current row
        ) as sma_7_open,

        -- SMA 7 for High
        avg(high_price) over (
            partition by ticker 
            order by trading_date 
            rows between 6 preceding and current row
        ) as sma_7_high,

        -- SMA 7 for Low
        avg(low_price) over (
            partition by ticker 
            order by trading_date 
            rows between 6 preceding and current row
        ) as sma_7_low

    from historical_data
)

select * from sma_calculations
where sma_7_close is not null
order by ticker, trading_date