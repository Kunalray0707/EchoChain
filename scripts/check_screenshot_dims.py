"""Print dimensions of captured Streamlit screenshot PNGs."""
import os
import struct

FILES = [
    "screenshots/streamlit_page1_executive_overview.png",
    "screenshots/streamlit_page2_sustainability.png",
    "screenshots/streamlit_page3_marketplace_analytics.png",
    "screenshots/streamlit_page4_product_lifecycle.png",
    "screenshots/streamlit_page5_component_quality.png",
    "screenshots/streamlit_page6_financial_insights.png",
]


def png_size(path):
    """Return (width, height) of a PNG by reading its IHDR chunk."""
    with open(path, "rb") as f:
        data = f.read(33)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


for f in FILES:
    if os.path.exists(f):
        w, h = png_size(f)
        size = os.path.getsize(f)
        print(f"{os.path.basename(f):<50} {w}x{h}  ({size:,} bytes)")
    else:
        print(f"{os.path.basename(f):<50} MISSING")

