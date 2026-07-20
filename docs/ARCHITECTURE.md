# EchoChain Lakehouse Architecture

## Medallion Lakehouse Paradigm
EchoChain implements the Databricks Medallion Architecture (Bronze -> Silver -> Gold) using PySpark and Delta Lake to process internal ERP manufacturing datasets and unstructured web-scraped secondary marketplace data.

```mermaid
flowchart TD
    subgraph Data Sources
        RAW1[Internal ERP BOM CSV]
        RAW2[Warranty Claims CSV]
        RAW3[E-Waste CSV Dataset]
        RAW4[Scraped Marketplace JSON - eBay/FB/OLX/BackMarket]
    end

    subgraph Bronze Layer [Raw Ingestion Delta Lake]
        B1[bronze_bom]
        B2[bronze_warranty]
        B3[bronze_ewaste]
        B4[bronze_listings]
    end

    subgraph Silver Layer [Cleaning & Reconciliation]
        S1[silver_bom]
        S2[silver_warranty]
        S3[silver_ewaste]
        S4[silver_listings]
        FUZZY[Fuzzy Title-to-SKU Reconciliation Engine]
        S5[silver_linked_listings]
    end

    subgraph Gold Layer [Business & Circular Analytics]
        G1[gold_circularity_metrics]
        G2[gold_component_failure]
        G3[gold_marketplace_analytics]
        G4[gold_sustainability_impact]
    end

    subgraph BI & Consumers
        PBI[Power BI Executive Dashboards]
        NB[Jupyter / Databricks Analytics Notebooks]
    end

    RAW1 --> B1
    RAW2 --> B2
    RAW3 --> B3
    RAW4 --> B4

    B1 --> S1
    B2 --> S2
    B3 --> S3
    B4 --> S4

    S4 & S1 --> FUZZY --> S5

    S5 & S1 --> G1
    S2 & S1 --> G2
    S4 --> G3
    G1 --> G4

    G1 & G2 & G3 & G4 --> PBI
    G1 & G2 & G3 & G4 --> NB
```

## Layer Specifications

### Bronze Layer (Raw Storage)
- Stores raw files verbatim with append-only semantics.
- Appends operational audit metadata columns: `_ingested_at` (Timestamp) and `_source_file` (String).

### Silver Layer (Cleaned & Harmonized)
- Normalizes currency exchanges (EUR, GBP, BRL, INR to USD).
- Harmonizes product condition strings into standard taxonomy (*Like New, Refurbished, Excellent, Good, Fair, Salvage*).
- Fuzzy SKU Matching engine links unstructured listing titles to internal ERP SKUs using Levenshtein distance and regex token matching.

### Gold Layer (Aggregated Business Analytics)
- Partitioned by Category and Year.
- Z-Ordered on high cardinality columns (`SKU`, `listing_id`) for ultra-fast query performance.
