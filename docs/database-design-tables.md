```mermaid
erDiagram
    RAW_TICKER_DATA ||--|{ CLEAN_STOCK_DATA : "transforms into"

    RAW_TICKER_DATA {
        string ticker_symbol PK
        timestamp received_at PK
        jsonb json_payload
    }

    CLEAN_STOCK_DATA {
        string ticker_symbol FK
        timestamp received_at FK
        string name PK
        date date PK
        float open
        float high
        float low
        float close
        float start
        float open_sma
        float high_sma
        float low_sma
        float close_sma
        float start_sma
    }
```