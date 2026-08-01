"""Verify the embedded JSON data in docs/index.html is complete and valid."""

import json
import os
import re

path = os.path.join(os.path.dirname(__file__), "..", "docs", "index.html")
content = open(path, encoding="utf-8").read()

# Extract the DATA = {...}; JSON block
m = re.search(r"const DATA = (\{.*?\});\n\nconst COLORS", content, re.DOTALL)
if not m:
    print("FAILED: could not find DATA JSON block")
    raise SystemExit(1)

data = json.loads(m.group(1))
print("Keys:", list(data.keys()))
for k, v in data.items():
    print(f"  {k}: {len(v)} records")
    if v:
        print(f"    sample keys: {list(v[0].keys())[:6]}...")

# Verify each section has data
for key in ["circularity", "marketplace", "component", "sustainability"]:
    assert data.get(key), f"Missing data for {key}"
print("\nALL_DATA_PRESENT: True")
