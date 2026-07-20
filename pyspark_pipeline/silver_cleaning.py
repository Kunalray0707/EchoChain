"""
Silver Layer Cleaning & Standardization Job
Deduplication, price standardizing to USD, condition mapping, text cleaning.
"""

import os
import pandas as pd

RATES = {"USD": 1.0, "EUR": 1.09, "GBP": 1.27, "BRL": 0.18, "INR": 0.012}
CONDITION_MAP = {
    "New - Open Box": "Like New",
    "Refurbished - Grade A": "Refurbished",
    "Used - Excellent": "Excellent",
    "Used - Good": "Good",
    "Used - Fair": "Fair",
    "For Parts / Non-Functional": "Salvage"
}

def clean_silver_tables(spark, bronze_dir="data/bronze", silver_dir="data/silver"):
    print("=== Starting Silver Cleaning Layer ===")
    os.makedirs(silver_dir, exist_ok=True)

    # 1. Silver BOM
    bom_csv = os.path.join(bronze_dir, "bronze_bom.csv")
    if os.path.exists(bom_csv):
        df = pd.read_csv(bom_csv)
        df.rename(columns={
            "Manufacturing Cost": "manufacturing_cost_usd",
            "Production Date": "production_date",
            "Carbon Footprint": "carbon_footprint_kg",
            "Warranty Period": "warranty_period_months",
            "Warranty Claims": "warranty_claims_count",
            "Failure Rate": "failure_rate"
        }, inplace=True)
        df.drop_duplicates(subset=["SKU", "Component"], inplace=True)
        df.fillna({"manufacturing_cost_usd": 0.0, "carbon_footprint_kg": 0.0, "failure_rate": 0.0}, inplace=True)
        
        out_path = os.path.join(silver_dir, "silver_bom")
        os.makedirs(out_path, exist_ok=True)
        df.to_csv(out_path + ".csv", index=False)
        try:
            df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
        except Exception:
            pass
        print(f"[OK] Silver BOM Cleaned: {len(df)} records.")

    # 2. Silver Warranty
    war_csv = os.path.join(bronze_dir, "bronze_warranty.csv")
    if os.path.exists(war_csv):
        df = pd.read_csv(war_csv)
        df.rename(columns={
            "Customer ID": "customer_id",
            "Failure Component": "failure_component",
            "Claim Date": "claim_date",
            "Repair Cost": "repair_cost_usd"
        }, inplace=True)
        df.dropna(subset=["SKU"], inplace=True)
        df.drop_duplicates(subset=["customer_id", "SKU", "claim_date"], inplace=True)
        
        out_path = os.path.join(silver_dir, "silver_warranty")
        os.makedirs(out_path, exist_ok=True)
        df.to_csv(out_path + ".csv", index=False)
        try:
            df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
        except Exception:
            pass
        print(f"[OK] Silver Warranty Cleaned: {len(df)} records.")

    # 3. Silver Listings
    lst_csv = os.path.join(bronze_dir, "bronze_listings.csv")
    if os.path.exists(lst_csv):
        df = pd.read_csv(lst_csv)
        
        # Price conversion
        df["price_usd"] = df.apply(lambda r: round(r["price"] * RATES.get(str(r.get("currency", "USD")).upper(), 1.0), 2), axis=1)
        df["normalized_condition"] = df["condition"].map(lambda c: CONDITION_MAP.get(c, "Good"))
        df["title_clean"] = df["product_title"].astype(str).str.lower().str.strip()
        df = df[df["price_usd"] > 0]
        df.drop_duplicates(subset=["listing_id"], inplace=True)
        
        out_path = os.path.join(silver_dir, "silver_listings")
        os.makedirs(out_path, exist_ok=True)
        df.to_csv(out_path + ".csv", index=False)
        try:
            df.to_parquet(os.path.join(out_path, "part-000.parquet"), index=False)
        except Exception:
            pass
        print(f"[OK] Silver Listings Cleaned: {len(df)} records.")

    print("=== Silver Cleaning Layer Complete ===")
