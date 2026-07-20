"""
Master Orchestrator Entrypoint for PySpark EchoChain Lakehouse Pipeline
Runs Bronze Ingestion -> Silver Cleaning -> Fuzzy SKU Matching -> Gold Analytics Aggregations.
"""

import sys
import os
import time

vendor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vendor_packages"))
if os.path.exists(vendor_path) and vendor_path not in sys.path:
    sys.path.insert(0, vendor_path)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from spark_session import get_spark_session
from bronze_ingestion import ingest_bronze_tables
from silver_cleaning import clean_silver_tables
from fuzzy_matching import reconcile_sku_matching
from gold_metrics import build_gold_metrics

def main():
    start_time = time.time()
    print("==========================================================")
    print("      ECHOCHAIN LAKEHOUSE MEDALLION PIPELINE ENGINE       ")
    print("==========================================================")

    # 1. Initialize Spark Session
    spark = get_spark_session("EchoChain-Medallion-Job")
    print(f"Spark Session initialized. Version: {spark.version}")

    # 2. Step 1: Bronze Ingestion
    ingest_bronze_tables(spark, raw_dir="data/raw", bronze_dir="data/bronze")

    # 3. Step 2: Silver Cleaning & Standardization
    clean_silver_tables(spark, bronze_dir="data/bronze", silver_dir="data/silver")

    # 4. Step 3: Fuzzy Title-to-SKU Reconciliation
    reconcile_sku_matching(spark, silver_dir="data/silver")

    # 5. Step 4: Gold Business & Circular Economy Metrics
    build_gold_metrics(spark, silver_dir="data/silver", gold_dir="data/gold")

    elapsed = round(time.time() - start_time, 2)
    print("==========================================================")
    print(f"[SUCCESS] EchoChain Lakehouse Pipeline Completed in {elapsed}s.")
    print("==========================================================")

if __name__ == "__main__":
    main()
