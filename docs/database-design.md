```mermaid
erDiagram
    TICKER {
        string ticker_name PK
        int timestamp PK
        float high
        float low
        float start
        float close
    }
```