# PLANNING PHASE: Financial Data Pipeline

---

## 1. What & Why


* **Primary Goal:** To build an automated **ELT pipeline** that fetches stock prices and creates analytical views for decision-making.
* **The Actual Value:** This provides the user with a **"Single Source of Truth."** Instead of calling an API for every query, complex questions can be asked directly against a local database, which is faster and enables advanced historical analysis.

---

## 2. Scope

### User Stories & Logic
1.  **As a** Data Analyst, **I want to** have access to daily closing prices for tech stocks in a SQL database, **so that** I can build dashboards without writing Python code for every new query.
    * **Input:** JSON data from Polygon.io (Daily Aggregates).
    * **Transform:** Python script mapping JSON to a structured table format.
    * **Output:** A **"Raw" table** in PostgreSQL with columns for `ticker`, `close_price`, and `timestamp`.

2.  **As a** Portfolio Manager, **I want to** see a 7-day Simple Moving Average (SMA) for my stocks, **so that** I can identify buy signals despite daily volatility.
    * **Input:** Data from the "Raw" table in SQL.
    * **Transform:** A **dbt model** calculating `AVG(close_price) over 7 days`.
    * **Output:** An **"Analytics" view** or table ready for visualization.

### Non-Goals
* **Feature to avoid:** Real-time streaming (WebSockets). We focus on batch data (Daily) to keep the architecture stable and cost-effective.
* **Feature to avoid:** Advanced prediction using AI/ML. The goal is data engineering, not data science.

---

## 3. System Logic

**Strategy:** 
* If we can automate the retrieval of raw data from Polygon.io via Python, store it in PostgreSQL, and then use dbt to create logical layers for analytic views, then the goal is met because we have built an automated ELT pipeline that fetches Stockprices and creates analytical views for decision-making.

**Dependencies:**
* **API:** Polygon.io (Free tier is sufficient for daily data).
* **Database:** PostgreSQL (running in Docker for easy portability).
* **Transformation:** dbt-core (to run SQL transformations).
* **Orchestration:** Docker Compose (to unify the database and scripts).

---

## 4. Definition of Done

**Completion Mark:** This system is considered complete when the following layers are functional:

### Layer 1: Infrastructure & Storage
* **Action:** `docker-compose up` successfully starts a PostgreSQL database.
* **Success:** A manual SQL query confirms that a `raw_stock_prices` table exists with the correct columns (`ticker`, `price`, `timestamp`).

### Layer 2: Ingestion
* **Action:** A Python script fetches data from Polygon.io and saves it into the database.
* **Success:** Running the script once populates the `raw_stock_prices` table with new rows without manual SQL entry.

### Layer 3: Transformation
* **Action:** `dbt run` executes without errors against the PostgreSQL database.
* **Success:** A new view/table (e.g., `fct_moving_averages`) is created, showing the 7-day SMA calculated from the raw data.

### Layer 4: Presentation
* **Action:** The Streamlit application is launched and connects to the database.
* **Success:** A web browser displays a visual line chart comparing daily prices vs. the 7-day SMA.