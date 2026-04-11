# Financial Data Pipeline (ELT)

### The Central Concept
**Project Objective:** This repository contains an automated ELT pipeline designed to ingest high-fidelity financial data from the **Polygon.io API** and load it into a **PostgreSQL** warehouse. The primary objective is to calculate a **7-day Simple Moving Average (SMA)** for stock symbols to facilitate trend analysis.

**Function:** It serves as an end-to-end data engineering solution that handles data extraction, containerized database management, and in-warehouse transformations.

---

### Structure
The project is divided into three functional layers:

* **Extraction Layer (Python):** Connects to Polygon.io, handles API authentication, and streams raw financial data.
* **Storage Layer (PostgreSQL):** A containerized relational database that ensures environment parity and persistent storage.
* **Transformation Layer (dbt):** Manages the "T" in ELT by modularizing SQL queries to create the 7-day SMA models.
