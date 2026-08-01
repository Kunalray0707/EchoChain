"""
Full-page dashboard screenshot capture
======================================
Starts the EchoChain Streamlit server (if not running), captures FULL-PAGE
screenshots of all 6 dashboard pages using Selenium + Edge, then cleans up.

Fixes the previous viewport-only captures by using CDP (Chrome DevTools
Protocol) Page.captureScreenshot with captureBeyondViewport=true, which
captures the ENTIRE scrollable page height (all charts, tables, footer).
"""

import base64
import os
import subprocess
import sys
import time
import urllib.request

from selenium import webdriver

OUT_DIR = "screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

PAGES = [
    ("streamlit_page1_executive_overview.png", "Executive Overview"),
    ("streamlit_page2_sustainability.png", "Sustainability"),
    ("streamlit_page3_marketplace_analytics.png", "Marketplace Analytics"),
    ("streamlit_page4_product_lifecycle.png", "Product Lifecycle"),
    ("streamlit_page5_component_quality.png", "Component Quality"),
    ("streamlit_page6_financial_insights.png", "Financial Insights"),
]

URL = "http://localhost:8501"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8501


def server_ready(timeout=60):
    """Poll the Streamlit server until it responds with HTTP 200."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(URL, timeout=3) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False


def start_server():
    """Start the Streamlit server as a background process."""
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "dashboards/streamlit_app.py",
        "--server.headless",
        "true",
        "--server.port",
        str(PORT),
        "--browser.gatherUsageStats",
        "false",
        "--server.fileWatcherType",
        "none",
    ]
    print(f"[START] Launching Streamlit: {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.getcwd(),
    )
    return proc


def capture_full_page(driver, path):
    """
    Use CDP Page.captureScreenshot with captureBeyondViewport=true to grab the
    entire scrollable page — not just the visible viewport.
    """
    # Force any lazy content to load by scrolling through the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    # Resize window to a tall canvas so the page renders fully
    page_height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);"
    )
    page_height = min(int(page_height), 20000)
    driver.set_window_size(1920, max(page_height, 1080))
    time.sleep(2)

    # Use CDP to capture beyond viewport
    result = driver.execute_cdp_cmd(
        "Page.captureScreenshot",
        {"format": "png", "captureBeyondViewport": True, "fromSurface": True},
    )
    # CDP returns base64-encoded PNG data — decode it, don't latin-1 encode it!
    with open(path, "wb") as f:
        f.write(base64.b64decode(result["data"]))
    print(f"  [OK] Saved {path} ({os.path.getsize(path)} bytes)", flush=True)


def main():
    # 1. Start the Streamlit server
    proc = start_server()
    print("[WAIT] Waiting for Streamlit server to become ready...", flush=True)
    if not server_ready(timeout=90):
        print("[ERROR] Streamlit server did not start in time.", flush=True)
        proc.terminate()
        sys.exit(1)
    print("[OK] Streamlit server is up.", flush=True)

    # 2. Launch Edge driver
    options = webdriver.EdgeOptions()
    options.binary_location = EDGE_PATH
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--hide-scrollbars")
    driver = webdriver.Edge(options=options)
    driver.set_window_size(1920, 1080)

    try:
        for filename, page_label in PAGES:
            print(f"[CAPTURE] {filename} — {page_label}", flush=True)
            driver.get(URL)
            time.sleep(8)  # Streamlit boot + first render

            # Click the sidebar radio for this page
            try:
                radios = driver.find_elements(
                    "css selector",
                    '[data-testid="stSidebar"] [role="radio"], [data-testid="stSidebar"] label',
                )
                for radio in radios:
                    if page_label.lower() in radio.text.lower():
                        radio.click()
                        time.sleep(6)
                        break
            except Exception as e:
                print(f"  [WARN] Sidebar click failed: {e}", flush=True)

            time.sleep(4)  # let charts/tables settle
            path = os.path.join(OUT_DIR, filename)
            capture_full_page(driver, path)

        print("=== All full-page screenshots captured ===", flush=True)
    finally:
        driver.quit()
        proc.terminate()
        print("[CLEANUP] Streamlit server stopped.", flush=True)


if __name__ == "__main__":
    main()

