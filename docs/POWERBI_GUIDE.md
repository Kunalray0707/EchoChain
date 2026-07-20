# Power BI Dashboard Setup & Deployment Guide

## 1. Connecting Power BI to Delta Lake Tables
1. Open **Power BI Desktop**.
2. Select **Get Data** -> **Folder** (for local Parquet/Delta) or **Databricks / Spark** connector.
3. Load Gold tables from `data/gold/`:
   - `gold_circularity_metrics`
   - `gold_component_failure`
   - `gold_marketplace_analytics`
   - `gold_sustainability_impact`

## 2. Importing Theme & DAX Measures
1. Go to **View** ribbon -> **Themes** -> **Browse for Themes** -> Select `dashboards/echochain_theme.json`.
2. Create a new table named `_DAX_Measures` and copy all formulas from `dashboards/DAX_Measures.dax`.

## 3. Configuring Page Bookmarks & Drill-Through
- Set up drill-through targets from Page 1 (Executive Overview) into Page 5 (Component Failure Analysis) passing `SKU`.
- Configure page navigation buttons targeting the 6 report pages.
