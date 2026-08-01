"""Verify Streamlit app: syntax + modern width='stretch' API (Streamlit >= 1.49).

NOTE: Streamlit >= 1.49 deprecates `use_container_width` in favour of `width`
('stretch' | 'content' | int).  use_container_width is scheduled for removal
after 2025-12-31 and emits a "Please replace use_container_width with width"
warning at runtime.  This verifier enforces the MODERN API.
"""

import ast
import sys

path = "dashboards/streamlit_app.py"

# 1. Syntax check
with open(path, encoding="utf-8") as f:
    source = f.read()
ast.parse(source)
print("SYNTAX_OK")

# 2. Confirm modern width='stretch' / width="stretch" present
stretch_count = source.count("width='stretch'") + source.count('width="stretch"')
print(f"width='stretch' count: {stretch_count}")
if stretch_count == 0:
    print("NO_WIDTH_STRETCH_FOUND")
    sys.exit(1)

# 3. Reject deprecated use_container_width (removed in Streamlit 1.60 era)
deprecated = source.count("use_container_width")
print(f"use_container_width count (deprecated): {deprecated}")
if deprecated > 0:
    print("DEPRECATED_USE_CONTAINER_WIDTH_PRESENT")
    sys.exit(1)

print("ALL_CHECKS_PASSED")
