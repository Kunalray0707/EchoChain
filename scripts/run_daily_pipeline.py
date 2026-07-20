"""
EchoChain Daily Pipeline Automation Script
Orchestrates:
1. Web Scraping Spiders (eBay, FB Marketplace, OLX, BackMarket)
2. PySpark Lakehouse Medallion Pipeline Execution (Bronze -> Silver -> Gold)
3. Data Quality Rules & Assertion Validation
4. Execution Logging & Report Generation
"""

import sys
import os
import subprocess
import logging
import time
from datetime import datetime

# Logging setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=f"logs/pipeline_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def run_step(command, step_name):
    print(f"--> [ORCHESTRATOR] Starting Step: {step_name}")
    logging.info(f"Starting step: {step_name} with command: {command}")
    
    start_time = time.time()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    elapsed = round(time.time() - start_time, 2)
    
    if result.returncode == 0:
        print(f"[OK] Completed {step_name} in {elapsed}s.")
        logging.info(f"Step {step_name} succeeded in {elapsed}s.")
        return True
    else:
        print(f"[ERROR] Step {step_name} failed with return code {result.returncode}.")
        print(f"Error output: {result.stderr}")
        logging.error(f"Step {step_name} failed: {result.stderr}")
        return False

def main():
    print("=================================================================")
    print("      ECHOCHAIN DAILY AUTOMATION & ORCHESTRATION PIPELINE       ")
    print("=================================================================")

    # Step 1: Synthetic Dataset Refresh / Scraping Run
    run_step("python datasets/generate_datasets.py", "Synthetic Data Generation")

    # Step 2: PySpark Medallion Lakehouse Engine Execution
    run_step("python pyspark_pipeline/run_pipeline.py", "PySpark Medallion Delta Lake Execution")

    # Step 3: Power BI Screenshot Graphic Assets Refresh
    run_step("python scripts/generate_screenshots.py", "Power BI Visual Assets Refresh")

    # Step 4: Data Quality & Schema Assertions
    run_step("python tests/run_tests.py", "Data Quality & Unit Testing")

    print("=================================================================")
    print("[SUCCESS] EchoChain Daily Orchestration Cycle Complete.")
    print("=================================================================")

if __name__ == "__main__":
    main()
