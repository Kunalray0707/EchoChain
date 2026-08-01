import os
import pandas as pd

def test_gold_circularity_metrics_bounds():
    """Validate circularity metrics CSV produced by the Gold layer."""
    gold_path = os.path.join("data", "gold", "gold_circularity_metrics.csv")
    if os.path.exists(gold_path):
        df = pd.read_csv(gold_path)
        assert len(df) > 0, "Gold circularity metrics CSV is empty"
        # circularity_score must be within [0, 100] bounds
        assert (df["circularity_score"] >= 0).all()
        assert (df["circularity_score"] <= 100).all()
        assert (df["resale_index"] >= 0).all()
        assert "SKU" in df.columns
        assert "Product" in df.columns
        assert "co2_avoided_tons" in df.columns

def test_gold_component_failure_schema():
    """Validate component failure CSV schema and data bounds."""
    gold_comp_path = os.path.join("data", "gold", "gold_component_failure.csv")
    if os.path.exists(gold_comp_path):
        df = pd.read_csv(gold_comp_path)
        assert len(df) > 0, "Gold component failure CSV is empty"
        for col in ["SKU", "Component", "claim_count", "avg_repair_cost_usd", "repairability_index"]:
            assert col in df.columns, f"Missing column: {col}"
        assert (df["claim_count"] >= 0).all()
        assert (df["repairability_index"] >= 0).all()
        assert (df["repairability_index"] <= 10).all()
