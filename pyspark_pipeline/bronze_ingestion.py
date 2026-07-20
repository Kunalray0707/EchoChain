"""
Bronze Layer Ingestion Job
Ingests raw CSV/JSON files into Delta Bronze tables with ingestion metadata.
"""

import os
import pandas as pd
from datetime import datetime

def ingest_bronze_tables(spark, raw_dir="data/raw", bronze_dir="data/bronze"):
    """
    Ingests raw datasets into Bronze tables.
    """
    print("=== Starting Bronze Ingestion Layer ===")
    os.makedirs(bronze_dir, exist_ok=True)
    ingested_at = datetime.utcnow().isoformat()

    # 1. BOM Ingestion
    bom_path = os.path.join(raw_dir, "manufacturing_bom.csv")
    if os.path.exists(bom_path):
        df = pd.read_csv(bom_path)
        df["_ingested_at"] = ingested_at
        df["_source_file"] = "manufacturing_bom.csv"
        out_path = os.path.join(bronze_dir, "bronze_bom")
        os.makedirs(out_path, exist_ok=True)
        df.to_csv(out_path + ".csv", index=False)
        try:
            df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
        except Exception:
            pass
        print(f"[OK] Ingested Bronze BOM: {len(df)} records.")

    # 2. Warranty Claims Ingestion
    war_path = os.path.join(raw_dir, "warranty_claims.csv")
    if os.path.exists(war_path):
        df = pd.read_csv(war_path)
        df["_ingested_at"] = ingested_at
        df["_source_file"] = "warranty_claims.csv"
        out_path = os.path.join(bronze_dir, "bronze_warranty")
        os.makedirs(out_path, exist_ok=True)
        df.to_csv(out_path + ".csv", index=False)
        try:
            df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
        except Exception:
            pass
        print(f"[OK] Ingested Bronze Warranty: {len(df)} records.")

    # 3. Marketplace Listings Ingestion
    lst_json = os.path.join(raw_dir, "marketplace_listings.json")
    lst_csv = os.path.join(raw_dir, "marketplace_listings.csv")
    if os.path.exists(lst_json):
        df = pd.read_json(lst_json)
    elif os.path.exists(lst_csv):
        df = pd.read_csv(lst_csv)
    else:
        df = pd.DataFrame()

    if not df.empty:
        df["_ingested_at"] = ingested_at
        df["_source_file"] = "marketplace_listings.json"
        out_path = os.path.join(bronze_dir, "bronze_listings")
        os.makedirs(out_path, exist_ok=True)
        df.to_csv(out_path + ".csv", index=False)
        try:
            df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
        except Exception:
            pass
        print(f"[OK] Ingested Bronze Listings: {len(df)} records.")

    # 4. User E-Waste Dataset Ingestion
    ewaste_path = os.path.join(raw_dir, "e_waste_dataset.csv")
    if os.path.exists(ewaste_path):
        try:
            df = pd.read_csv(ewaste_path)
            df["_ingested_at"] = ingested_at
            df["_source_file"] = "e_waste_dataset.csv"
            out_path = os.path.join(bronze_dir, "bronze_ewaste")
            os.makedirs(out_path, exist_ok=True)
            df.to_csv(out_path + ".csv", index=False)
            try:
                df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
            except Exception:
                pass
            print(f"[OK] Ingested Bronze E-Waste: {len(df)} records.")
        except Exception as e:
            print(f"[WARNING] E-Waste CSV read deferred: {e}")


    print("=== Bronze Ingestion Complete ===")
