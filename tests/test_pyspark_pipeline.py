import os
import pandas as pd

def test_silver_table_outputs():
    silver_listings_path = os.path.join("data", "silver", "silver_listings")
    assert os.path.exists(silver_listings_path) or os.path.exists(silver_listings_path + ".csv")

def test_fuzzy_sku_matching_output():
    linked_path = os.path.join("data", "silver", "silver_linked_listings")
    assert os.path.exists(linked_path) or os.path.exists(linked_path + ".csv")

