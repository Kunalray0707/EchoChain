# EchoChain End-to-End Workflow & Orchestration

## Pipeline Execution Lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant Scraper as Scrapy Spiders
    participant RawData as data/raw Filesystem
    participant Spark as PySpark Medallion Engine
    participant Delta as Delta Lake (Bronze/Silver/Gold)
    participant Tests as Pytest Quality Engine
    participant PBI as Power BI / Assets

    Scraper->>RawData: 1. Crawl eBay, FB, OLX, BackMarket -> Save JSON/CSV
    Spark->>RawData: 2. Read Raw BOM, Warranty, E-Waste & Listings
    Spark->>Delta: 3. Write Bronze Delta Tables (_ingested_at)
    Spark->>Delta: 4. Clean, Deduplicate & Standardize -> Write Silver Tables
    Spark->>Delta: 5. Execute Fuzzy SKU Matching Engine -> Write Linked Listings
    Spark->>Delta: 6. Compute Circularity & Sustainability -> Write Gold Tables
    Tests->>Delta: 7. Run Schema & Boundary Quality Assertions
    PBI->>Delta: 8. Refresh Executive Power BI Dashboards & Visual Assets
```

## Daily Automation Cron / Orchestration
The pipeline is orchestrated daily via `scripts/run_daily_pipeline.py` or containerized execution via Docker Compose.
