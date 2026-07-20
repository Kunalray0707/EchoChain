import os
import pandas as pd
import json

def test_manufacturing_bom_file_exists():
    path = os.path.join("data", "raw", "manufacturing_bom.csv")
    assert os.path.exists(path), "Manufacturing BOM file missing"
    
    df = pd.read_csv(path)
    assert len(df) > 0, "BOM dataset is empty"
    assert "SKU" in df.columns
    assert "Manufacturing Cost" in df.columns

def test_warranty_claims_file_exists():
    path = os.path.join("data", "raw", "warranty_claims.csv")
    assert os.path.exists(path), "Warranty claims file missing"
    
    df = pd.read_csv(path)
    assert len(df) >= 1000, "Warranty dataset smaller than expected"
    assert "Customer ID" in df.columns
    assert "Repair Cost" in df.columns

def test_marketplace_listings_file_exists():
    path = os.path.join("data", "raw", "marketplace_listings.json")
    assert os.path.exists(path), "Marketplace listings JSON missing"
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 1000, "Marketplace listings count smaller than expected"
    assert data[0]["marketplace"] in ["eBay", "Facebook Marketplace", "OLX", "BackMarket"]
