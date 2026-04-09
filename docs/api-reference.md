# JSON Reference Mapping

This document serves as the bridge between the raw API response and our database schema.

---

### Technical Mapping Table

| JSON Key | Technical Name | Logical Definition | Target DB Column |
| :--- | :--- | :--- | :--- |
| **`t`** | Timestamp | Unix Epoch (Seconds) | `date` |
| **`o`** | Open | Price at start of period | `open` |
| **`h`** | High | Highest price in period | `high` |
| **`l`** | Low | Lowest price in period | `low` |
| **`c`** | Close | Price at end of period | `close` |

---
