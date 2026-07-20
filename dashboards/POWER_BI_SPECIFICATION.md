# EchoChain Executive Power BI Dashboard Blueprint

## Overview
This specification details the structure, visual layouts, page bookmarks, drill-through actions, and visual mappings for the 6-page enterprise Power BI dashboard suite.

---

## Theme & Canvas Setup
- **Theme**: Dark Glassmorphism (`echochain_theme.json`)
- **Canvas Size**: 16:9 Widescreen (1920 x 1080 px)
- **Background Color**: `#0F172A` (Slate 900)
- **Card Fill Color**: `#1E293B` (Slate 800) with 12px rounded borders & subtle glow.
- **Accent Palette**: Emerald (`#10B981`), Cyan (`#06B6D4`), Violet (`#8B5CF6`), Amber (`#F59E0B`), Rose (`#EF4444`).

---

## Page 1: Executive Overview
**Objective**: High-level summary of circularity score, resale volume, landfill diversion, and top opportunities.

### Key Visuals & Layout:
1. **Header Navigation Bar**: Logo, Current Date, Filter Slicers (Category, Country, Date Range).
2. **KPI Scorecards (Top Row)**:
   - `Circularity Score %` (Target: > 80.0%)
   - `Total Resale Volume USD` ($)
   - `Landfill Diversion %` (%)
   - `Total CO2 Avoided Tons` (Tons)
   - `Buy-Back ROI %` (%)
3. **Main Visual (Left)**: **Waterfall Chart** - Manufacturing Cost vs. Secondary Resale Recovery by Product Category.
4. **Main Visual (Right)**: **Ribbon Chart** - Monthly Resale Volume Ranking across Marketplaces (eBay, FB Marketplace, OLX, BackMarket).
5. **Bottom Visual (Left)**: **Decomposition Tree** - Circularity Score breakdown by Manufacturer -> Category -> SKU.
6. **Bottom Visual (Right)**: **KPI Gauge** - Refurbishment Target vs Actual Rate %.

---

## Page 2: Sustainability & Circular Economy
**Objective**: Environmental impact tracking, CO₂ avoidance, material recovery, and carbon credit financial value.

### Key Visuals & Layout:
1. **KPI Cards**:
   - `Total CO2 Avoided Tons`
   - `Carbon Financial Savings USD`
   - `Material Recovery %`
   - `Avoided E-Waste Tonnage`
2. **Visual 1**: **Bubble Scatter Plot** - Carbon Footprint (kg CO₂) vs. Resale Retention Rate (%) sized by Units Circulated.
3. **Visual 2**: **Map Visual** - Global Distribution of Secondary Listings & Avoided E-Waste by Country/Location.
4. **Visual 3**: **Treemap** - Material Composition Tonnage Breakdown (Aluminum, Lithium, Glass, Copper, Plastics).
5. **Visual 4**: **Area Chart** - Cumulative CO₂ Avoided YTD (Tons) vs Corporate ESG Reduction Target.

---

## Page 3: Secondary Marketplace Analytics
**Objective**: Detailed pricing analysis, seller ratings, condition distribution, and regional secondary demand.

### Key Visuals & Layout:
1. **KPI Cards**:
   - `Total Listings Count` (50,000)
   - `Average Resale Price USD` ($425.80)
   - `Average Seller Rating` (4.72 / 5.0)
   - `Salvage Rate %` (4.1%)
2. **Visual 1**: **Clustered Bar Chart** - Average Resale Price by Condition (Like New, Refurbished, Excellent, Good, Fair, Salvage).
3. **Visual 2**: **Line & Stacked Column Chart** - Listing Frequency & Sold Count by Marketplace over time.
4. **Visual 3**: **Matrix Visual** - Detailed Listing Breakdown (Marketplace, SKU, Condition, Avg Price, Sold Count, Total Volume).
5. **Visual 4**: **Heatmap Visual** - Seller Rating vs Shipping Cost impact on Sold Rate.

---

## Page 4: Product Lifecycle & Resale Retention
**Objective**: End-to-end lifecycle tracking comparing manufacturing cost against secondary market value retention over product age.

### Key Visuals & Layout:
1. **KPI Cards**:
   - `Resale Index` (0.84)
   - `Resale Price Retention %` (84.2%)
   - `Average Manufacturing Cost USD` ($492.10)
   - `Average Product Weight kg` (2.4 kg)
2. **Visual 1**: **Line Chart** - Price Depreciation Curve over Product Age (0-36 Months) by Category.
3. **Visual 2**: **Donut Chart** - Condition Distribution across Product Portfolio.
4. **Visual 3**: **Table Visual** - Top 10 Resalable Products with Buy-Back Opportunity Flag.

---

## Page 5: Component Failure & Quality Analysis
**Objective**: Pinpoint component failures, warranty claim hotspots, repairability scores, and component supplier reliability.

### Key Visuals & Layout:
1. **KPI Cards**:
   - `Total Warranty Claims`
   - `Component Failure Index`
   - `Average Repair Cost USD`
   - `High Risk Component Count`
2. **Visual 1**: **Horizontal Bar Chart** - Most Failed Components by Claim Count & Supplier.
3. **Visual 2**: **Scatter Plot** - Component Manufacturing Cost vs Repair Cost Ratio %.
4. **Visual 3**: **Decomposition Tree** - Warranty Claims by Failure Issue -> Failure Component -> Supplier.
5. **Visual 4**: **Gauge Chart** - Average Repairability Index (Target: > 8.0).

---

## Page 6: Financial & Buy-back Program Insights
**Objective**: Financial modeling for OEM buy-back programs, refurbishment margins, and revenue recovery.

### Key Visuals & Layout:
1. **KPI Cards**:
   - `Buy-Back Program Margin USD`
   - `Buy-Back ROI %`
   - `Secondary Market Revenue Opportunity` ($)
   - `Warranty Expense Variance %`
2. **Visual 1**: **Waterfall Chart** - Buy-Back Margin Breakdown (Resale Value - Refurb Cost - Logistics - Purchase Price).
3. **Visual 2**: **Line Chart** - Projected 3-Year Revenue Recovery from OEM Secondary Channel.
4. **Visual 3**: **Matrix** - Category Profitability Matrix for Refurbishment & Trade-in Programs.
