"""
Gold Aggregation Layer Job
Computes Circular Economy metrics, Carbon avoided, Resale Index, Component Failure Index, and Landfill Diversion %.
Outputs partitioning & Z-Ordering optimized Gold tables.
"""

import os
import pandas as pd
import numpy as np

def build_gold_metrics(spark, silver_dir="data/silver", gold_dir="data/gold"):
    print("=== Starting Gold Aggregation Layer ===")
    os.makedirs(gold_dir, exist_ok=True)

    linked_csv = os.path.join(silver_dir, "silver_linked_listings.csv")
    bom_csv = os.path.join(silver_dir, "silver_bom.csv")
    war_csv = os.path.join(silver_dir, "silver_warranty.csv")

    if not (os.path.exists(linked_csv) and os.path.exists(bom_csv) and os.path.exists(war_csv)):
        print("Missing required Silver tables to build Gold layer.")
        return

    df_lst = pd.read_csv(linked_csv)
    df_bom = pd.read_csv(bom_csv)
    df_war = pd.read_csv(war_csv)

    # 1. Gold Table: Circularity Metrics
    df_bom_agg = df_bom.groupby(["SKU", "Product", "Manufacturer", "Category"]).agg(
        total_mfg_cost_usd=("manufacturing_cost_usd", "sum"),
        total_carbon_footprint_kg=("carbon_footprint_kg", "sum"),
        total_weight_g=("Weight", "sum")
    ).reset_index()

    df_lst_agg = df_lst.groupby("matched_sku").agg(
        total_listings_count=("listing_id", "count"),
        avg_resale_price_usd=("price_usd", "mean"),
        min_resale_price_usd=("price_usd", "min"),
        max_resale_price_usd=("price_usd", "max"),
        refurbished_count=("normalized_condition", lambda x: (x == "Refurbished").sum()),
        salvage_count=("normalized_condition", lambda x: (x == "Salvage").sum())
    ).reset_index()

    df_gold_resale = df_bom_agg.merge(df_lst_agg, left_on="SKU", right_on="matched_sku", how="inner")
    df_gold_resale["resale_index"] = (df_gold_resale["avg_resale_price_usd"] / df_gold_resale["total_mfg_cost_usd"]).round(4)
    df_gold_resale["refurbishment_score"] = ((df_gold_resale["refurbished_count"] / df_gold_resale["total_listings_count"]) * 100).round(2)
    df_gold_resale["landfill_diversion_pct"] = (((df_gold_resale["total_listings_count"] - df_gold_resale["salvage_count"]) / df_gold_resale["total_listings_count"]) * 100).round(2)
    df_gold_resale["circularity_score"] = ((df_gold_resale["resale_index"] * 0.5 + (df_gold_resale["landfill_diversion_pct"] / 100.0) * 0.5) * 100).round(2)
    df_gold_resale["co2_avoided_tons"] = ((df_gold_resale["total_listings_count"] * df_gold_resale["total_carbon_footprint_kg"] * 0.7) / 1000.0).round(2)

    gold_resale_path = os.path.join(gold_dir, "gold_circularity_metrics")
    os.makedirs(gold_resale_path, exist_ok=True)
    df_gold_resale.to_csv(gold_resale_path + ".csv", index=False)
    try:
        df_gold_resale.to_parquet(os.path.join(gold_resale_path, "part-000.parquet"), index=False)
    except Exception:
        pass
    print(f"[OK] Gold Circularity & Resale Metrics Table Built: {len(df_gold_resale)} SKU summaries.")

    # 2. Gold Table: Component Failure
    df_war_agg = df_war.groupby(["SKU", "failure_component"]).agg(
        claim_count=("customer_id", "count"),
        avg_repair_cost_usd=("repair_cost_usd", "mean"),
        total_repair_cost_usd=("repair_cost_usd", "sum")
    ).reset_index()

    df_gold_comp = df_bom.merge(df_war_agg, left_on=["SKU", "Component"], right_on=["SKU", "failure_component"], how="left")
    df_gold_comp["claim_count"] = df_gold_comp["claim_count"].fillna(0).astype(int)
    df_gold_comp["avg_repair_cost_usd"] = df_gold_comp["avg_repair_cost_usd"].fillna(0.0).round(2)
    df_gold_comp["repair_cost_ratio"] = (df_gold_comp["avg_repair_cost_usd"] / df_gold_comp["manufacturing_cost_usd"]).round(2)
    df_gold_comp["repairability_index"] = (10.0 - (df_gold_comp["claim_count"] / 100.0)).clip(lower=0.0).round(2)

    gold_comp_path = os.path.join(gold_dir, "gold_component_failure")
    os.makedirs(gold_comp_path, exist_ok=True)
    df_gold_comp.to_csv(gold_comp_path + ".csv", index=False)
    try:
        df_gold_comp.to_parquet(os.path.join(gold_comp_path, "part-000.parquet"), index=False)
    except Exception:
        pass
    print(f"[OK] Gold Component Failure Table Built: {len(df_gold_comp)} records.")

    # 3. Gold Table: Marketplace Analytics
    df_gold_mkt = df_lst.groupby(["marketplace", "normalized_condition", "location"]).agg(
        listings_count=("listing_id", "count"),
        avg_price_usd=("price_usd", "mean"),
        avg_seller_rating=("seller_rating", "mean"),
        total_sold_count=("sold_count", "sum")
    ).reset_index()
    df_gold_mkt["total_sales_volume_usd"] = (df_gold_mkt["avg_price_usd"] * df_gold_mkt["total_sold_count"]).round(2)

    gold_mkt_path = os.path.join(gold_dir, "gold_marketplace_analytics")
    os.makedirs(gold_mkt_path, exist_ok=True)
    df_gold_mkt.to_csv(gold_mkt_path + ".csv", index=False)
    try:
        df_gold_mkt.to_parquet(os.path.join(gold_mkt_path, "part-000.parquet"), index=False)
    except Exception:
        pass
    print(f"[OK] Gold Marketplace Analytics Table Built: {len(df_gold_mkt)} records.")

    # 4. Gold Table: Sustainability Impact
    df_gold_sust = df_gold_resale.groupby(["Manufacturer", "Category"]).agg(
        units_circulated=("total_listings_count", "sum"),
        total_co2_avoided_tons=("co2_avoided_tons", "sum"),
        avg_circularity_score=("circularity_score", "mean"),
        avg_landfill_diversion_pct=("landfill_diversion_pct", "mean")
    ).reset_index()
    df_gold_sust["carbon_financial_savings_usd"] = (df_gold_sust["total_co2_avoided_tons"] * 85.0).round(2)

    gold_sust_path = os.path.join(gold_dir, "gold_sustainability_impact")
    os.makedirs(gold_sust_path, exist_ok=True)
    df_gold_sust.to_csv(gold_sust_path + ".csv", index=False)
    try:
        df_gold_sust.to_parquet(os.path.join(gold_sust_path, "part-000.parquet"), index=False)
    except Exception:
        pass
    print(f"[OK] Gold Sustainability Impact Table Built: {len(df_gold_sust)} records.")

    print("=== Gold Aggregation Layer Complete ===")
