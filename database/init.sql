CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS clean;

CREATE TABLE raw.TICKER (
    ticker_name VARCHAR(255),
    unix_time BIGINT,
    high FLOAT,
    low FLOAT,
    start_time FLOAT,
    close_time FLOAT,
    PRIMARY KEY (ticker_name, unix_time)
);