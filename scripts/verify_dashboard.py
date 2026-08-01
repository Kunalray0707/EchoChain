"""Verify the static GitHub Pages dashboard contains expected content."""
import os

path = os.path.join(os.path.dirname(__file__), "..", "docs", "index.html")
content = open(path, encoding="utf-8").read()

checks = [
    "gold_circularity_metrics.csv",
    "Circularity Score by Product",
    "SKU-APP-IP14P-256",
    "renderPage5",
    "Plotly.newPlot",
    "Executive Overview Dashboard",
]

all_ok = True
for c in checks:
    ok = c in content
    all_ok = all_ok and ok
    print(("OK " if ok else "MISSING ") + c)

print("FILE_SIZE", len(content))
print("ALL_OK", all_ok)

