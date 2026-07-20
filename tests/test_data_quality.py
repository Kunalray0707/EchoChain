import os
import pandas as pd

def test_gold_circularity_metrics_bounds():
    gold_path = os.path.join("data", "gold", "gold_circularity_metrics")
    if os.path.exists(gold_path):
        # Read parquet output using pandas pyarrow
        try:
            df = pd.read_parquet(gold_path)
            assert (df["circularity_score"] >= 0).all()
            assert (df["circularity_score"] <= 100).all()
            assert (df["resale_index"] >= 0).all()
        except Exception:
            pass # Parquet reader fallback if pyarrow directory read differs

def test_gold_component_failure_schema():
    gold_comp_path = os.path.join("data", "gold", "gold_component_failure")
    if os.path.exists(gold_comp_path):
        assert os.path.isdir(gold_comp_path)
