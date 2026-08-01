"""Capture real full-page screenshots of the running Streamlit dashboard (localhost:8501).

Uses Microsoft Edge (always present on Windows 11) with Selenium Manager auto-driver.
Captures the ENTIRE page by expanding the browser window to the full content height,
so all charts, KPIs, tables and the footer are visible — not just the initial viewport.
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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


def get_full_page_height(driver):
    """Return the full scrollable height of the page."""
    return driver.execute_script(
        "return Math.max("
        "document.body.scrollHeight, "
        "document.documentElement.scrollHeight, "
        "document.body.offsetHeight, "
        "document.documentElement.offsetHeight, "
        "document.documentElement.clientHeight"
        ");"
    )


def capture_full_page(driver, path, max_height=20000):
    """
    Capture a full-page screenshot by resizing the browser window to the full
    content height, scrolling to top, then saving the screenshot.
    """
    # Get the scroll width & height of the full page
    page_width = driver.execute_script("return document.body.scrollWidth;")
    page_height = get_full_page_height(driver)
    page_height = min(page_height, max_height)  # safety cap

    # Current viewport dimensions
    cur_width = driver.get_window_size()["width"]
    cur_height = driver.get_window_size()["height"]

    # Resize window to full page height (preserve width). Add margin for scrollbar.
    if page_height > cur_height:
        driver.set_window_size(cur_width, page_height + 200)
        time.sleep(2)

    # Scroll to top
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(2)

    # Wait for lazy-loaded content (Plotly charts, dataframes) to render
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    # Save the full-page screenshot
    driver.save_screenshot(path)
    print(f"  [OK] Saved {path} ({os.path.getsize(path)} bytes)", flush=True)


def main():
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
    wait = WebDriverWait(driver, 45)

    try:
        for filename, page_label in PAGES:
            print(f"[CAPTURE] {filename} — {page_label}", flush=True)
            driver.get(URL)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Wait for Streamlit to boot & render
            time.sleep(8)

            # Click the sidebar radio option by label text
            try:
                radios = driver.find_elements(
                    By.CSS_SELECTOR,
                    '[data-testid="stSidebar"] [role="radio"], [data-testid="stSidebar"] label',
                )
                for radio in radios:
                    if page_label.lower() in radio.text.lower():
                        radio.click()
                        time.sleep(5)
                        break
            except Exception as e:
                print(f"  [WARN] Sidebar click failed: {e}", flush=True)

            # Wait for the page content to fully render
            time.sleep(5)
            path = os.path.join(OUT_DIR, filename)
            capture_full_page(driver, path)
            print(f"  [DIMS] {filename}", flush=True)

        print("=== All screenshots captured ===", flush=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

