"""
Standalone PyTest Test Runner Fallback for EchoChain Suite
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scrapy_project")))


def run_all_tests():
    print("=== EchoChain Data Quality & Unit Test Suite ===")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover and add test files
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run simple custom assertions
    import test_data_generator
    import test_scrapers
    import test_pyspark_pipeline
    import test_data_quality
    from conftest import sample_listing_item

    print("[TEST] Running test_data_generator...")
    test_data_generator.test_manufacturing_bom_file_exists()
    test_data_generator.test_warranty_claims_file_exists()
    test_data_generator.test_marketplace_listings_file_exists()
    print("  [PASSED] test_data_generator")

    print("[TEST] Running test_scrapers...")
    item = sample_listing_item()
    test_scrapers.test_data_cleaning_pipeline(item)
    test_scrapers.test_currency_normalizer_pipeline(item)
    print("  [PASSED] test_scrapers")

    print("[TEST] Running test_pyspark_pipeline...")
    test_pyspark_pipeline.test_silver_table_outputs()
    test_pyspark_pipeline.test_fuzzy_sku_matching_output()
    print("  [PASSED] test_pyspark_pipeline")

    print("[TEST] Running test_data_quality...")
    test_data_quality.test_gold_circularity_metrics_bounds()
    test_data_quality.test_gold_component_failure_schema()
    print("  [PASSED] test_data_quality")

    print("=================================================================")
    print("[SUCCESS] All 9 Data Quality & Unit Tests Passed Successfully.")
    print("=================================================================")

if __name__ == "__main__":
    run_all_tests()
