CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS clean;

CREATE TABLE raw.TICKER_DATA (
    ticker_symbol VARCHAR(255),
    received_at timestamp,
    json_payload jsonb,
    PRIMARY KEY (ticker_symbol, received_at)
);