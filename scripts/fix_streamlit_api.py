"""Migrate Streamlit API in dashboards/streamlit_app.py to the modern `width` arg.

Streamlit >= 1.49 deprecates `use_container_width` (scheduled for removal after
2025-12-31) in favour of `width`.  Correct replacements:
- st.plotly_chart(fig, use_container_width=True) -> st.plotly_chart(fig, width='stretch')
- st.dataframe(df, use_container_width=True)     -> st.dataframe(df, width='stretch')
"""

import io

path = "dashboards/streamlit_app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

before = content

# Replace legacy use_container_width=True with the modern width='stretch'
content = content.replace("use_container_width=True", "width='stretch'")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

count = before.count("use_container_width=True")
print(f"Replaced {count} occurrences of use_container_width=True with width='stretch'")
