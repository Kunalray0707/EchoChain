"""
EchoChain Screenshot & Visual Asset Generator
Generates high-fidelity SVG graphic visual previews for all 6 Power BI dashboard pages.
"""

import os

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

PAGES_DATA = [
    {
        "filename": "page1_executive_overview.svg",
        "title": "Page 1: Executive Overview Dashboard",
        "kpis": [
            ("Circularity Score", "86.4%", "#10B981"),
            ("Resale Volume USD", "$21.3M", "#06B6D4"),
            ("Landfill Diversion", "95.8%", "#8B5CF6"),
            ("CO2 Avoided", "14,250 Tons", "#F59E0B"),
            ("Buy-Back ROI", "34.2%", "#10B981")
        ],
        "chart1_title": "Cost vs Secondary Recovery (Waterfall)",
        "chart2_title": "Resale Volume by Marketplace (Ribbon)",
        "chart3_title": "Circularity Breakdown (Decomposition Tree)"
    },
    {
        "filename": "page2_sustainability.svg",
        "title": "Page 2: Sustainability & Environmental Impact",
        "kpis": [
            ("CO2 Avoided", "14,250 Tons", "#10B981"),
            ("Carbon Value", "$1.21M", "#06B6D4"),
            ("Material Recovery", "88.2%", "#8B5CF6"),
            ("E-Waste Diversion", "1,840 Tons", "#F59E0B")
        ],
        "chart1_title": "Carbon Footprint vs Resale Retention (Scatter)",
        "chart2_title": "Global Secondary Distribution Map",
        "chart3_title": "Material Composition Tonnage (Treemap)"
    },
    {
        "filename": "page3_marketplace_analytics.svg",
        "title": "Page 3: Secondary Marketplace Analytics",
        "kpis": [
            ("Total Listings", "50,000", "#06B6D4"),
            ("Avg Resale Price", "$425.80", "#10B981"),
            ("Seller Rating", "4.72 / 5.0", "#F59E0B"),
            ("Salvage Rate", "4.1%", "#EF4444")
        ],
        "chart1_title": "Average Resale Price by Condition (Bar)",
        "chart2_title": "Listing Volume & Sold Count Trends",
        "chart3_title": "Seller Rating & Shipping Impact Heatmap"
    },
    {
        "filename": "page4_product_lifecycle.svg",
        "title": "Page 4: Product Lifecycle & Resale Retention",
        "kpis": [
            ("Resale Index", "0.84", "#10B981"),
            ("Price Retention", "84.2%", "#06B6D4"),
            ("Avg Mfg Cost", "$492.10", "#8B5CF6"),
            ("Avg Weight", "2.4 kg", "#F59E0B")
        ],
        "chart1_title": "Price Depreciation Curve (0-36 Months)",
        "chart2_title": "Condition Share Distribution (Donut)",
        "chart3_title": "Top Resalable Products Buy-Back Matrix"
    },
    {
        "filename": "page5_component_analysis.svg",
        "title": "Page 5: Component Failure & Quality Analysis",
        "kpis": [
            ("Warranty Claims", "10,000", "#EF4444"),
            ("Failure Index", "200.0", "#F59E0B"),
            ("Avg Repair Cost", "$145.20", "#06B6D4"),
            ("Repairability Score", "8.4 / 10", "#10B981")
        ],
        "chart1_title": "Most Failed Components by Supplier",
        "chart2_title": "Mfg Cost vs Repair Cost Ratio (Scatter)",
        "chart3_title": "Warranty Issue Breakdown (Decomposition Tree)"
    },
    {
        "filename": "page6_financial_insights.svg",
        "title": "Page 6: Financial & Buy-Back Program Insights",
        "kpis": [
            ("Buy-Back Margin", "$148.50 / unit", "#10B981"),
            ("Buy-Back ROI", "34.2%", "#06B6D4"),
            ("Secondary Market Revenue", "$5.3M / yr", "#8B5CF6"),
            ("Warranty Expense Var", "-4.2%", "#10B981")
        ],
        "chart1_title": "Buy-Back Profitability Waterfall",
        "chart2_title": "3-Year Revenue Recovery Forecast",
        "chart3_title": "Category Trade-in Profitability Matrix"
    }
]

def generate_svg(page):
    kpi_blocks = ""
    for idx, (label, val, color) in enumerate(page["kpis"]):
        x_offset = 50 + idx * 220
        kpi_blocks += f"""
        <g transform="translate({x_offset}, 90)">
            <rect width="200" height="90" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
            <text x="15" y="30" fill="#94A3B8" font-family="Segoe UI, sans-serif" font-size="12" font-weight="600">{label.upper()}</text>
            <text x="15" y="68" fill="{color}" font-family="Segoe UI, sans-serif" font-size="26" font-weight="700">{val}</text>
        </g>
        """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
    <rect width="1200" height="675" fill="#0F172A"/>
    
    <!-- Top Header -->
    <rect x="0" y="0" width="1200" height="65" fill="#1E293B"/>
    <text x="30" y="42" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="22" font-weight="700">EchoChain Lakehouse Analytics</text>
    <text x="400" y="42" fill="#10B981" font-family="Segoe UI, sans-serif" font-size="16" font-weight="600">| {page["title"]}</text>
    <rect x="1050" y="18" width="120" height="30" rx="6" fill="#10B981"/>
    <text x="1075" y="38" fill="#0F172A" font-family="Segoe UI, sans-serif" font-size="12" font-weight="700">LIVE DATA</text>
    
    <!-- KPI Row -->
    {kpi_blocks}
    
    <!-- Main Visual Left -->
    <rect x="50" y="210" width="540" height="200" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="70" y="240" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="15" font-weight="600">{page["chart1_title"]}</text>
    <!-- Chart Mock Lines -->
    <path d="M 80 370 L 150 320 L 220 340 L 290 280 L 360 300 L 430 250 L 550 270" fill="none" stroke="#10B981" stroke-width="3"/>
    <path d="M 80 380 L 150 350 L 220 360 L 290 310 L 360 330 L 430 290 L 550 310" fill="none" stroke="#06B6D4" stroke-width="2" stroke-dasharray="4"/>
    
    <!-- Main Visual Right -->
    <rect x="610" y="210" width="540" height="200" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="630" y="240" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="15" font-weight="600">{page["chart2_title"]}</text>
    <!-- Bar Mock -->
    <rect x="640" y="270" width="380" height="20" rx="4" fill="#10B981"/>
    <rect x="640" y="305" width="310" height="20" rx="4" fill="#06B6D4"/>
    <rect x="640" y="340" width="240" height="20" rx="4" fill="#8B5CF6"/>
    <rect x="640" y="375" width="180" height="20" rx="4" fill="#F59E0B"/>

    <!-- Bottom Visual -->
    <rect x="50" y="430" width="1100" height="210" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="70" y="460" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="15" font-weight="600">{page["chart3_title"]}</text>
    
    <!-- Tree/Table Mock -->
    <rect x="70" y="480" width="220" height="40" rx="6" fill="#334155"/>
    <text x="85" y="505" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="13">Smartphones (88.4%)</text>
    
    <rect x="320" y="480" width="220" height="40" rx="6" fill="#334155"/>
    <text x="335" y="505" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="13">Laptops (84.1%)</text>

    <rect x="570" y="480" width="220" height="40" rx="6" fill="#334155"/>
    <text x="585" y="505" fill="#F8FAFC" font-family="Segoe UI, sans-serif" font-size="13">Home Appliances (79.2%)</text>
    
    <line x1="290" y1="500" x2="320" y2="500" stroke="#10B981" stroke-width="2"/>
    <line x1="540" y1="500" x2="570" y2="500" stroke="#10B981" stroke-width="2"/>
    
    <rect x="70" y="540" width="1060" height="80" rx="6" fill="#0F172A"/>
    <text x="90" y="570" fill="#10B981" font-family="Segoe UI, sans-serif" font-size="13" font-weight="600">[OK] Medallion Delta Lakehouse Pipeline Status: Synced &amp; Operational</text>
    <text x="90" y="595" fill="#94A3B8" font-family="Segoe UI, sans-serif" font-size="12">Bronze -> Silver -> Fuzzy Match SKU -> Gold Aggregations (Z-Ordered by Category)</text>
</svg>"""

    filepath = os.path.join(SCREENSHOTS_DIR, page["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated graphic: {filepath}")

def main():
    print("=== Generating Power BI Dashboard Visual Assets ===")
    for page in PAGES_DATA:
        generate_svg(page)
    print("=== Visual Assets Successfully Generated ===")

if __name__ == "__main__":
    main()
