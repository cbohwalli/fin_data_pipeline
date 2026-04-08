CREATE TABLE TICKER (
    ticker_name VARCHAR(255),
    unix_time INT,
    high FLOAT,
    low FLOAT,
    start_time FLOAT,
    close_time FLOAT,
    PRIMARY KEY (ticker_name, unix_time)
);