"""
EchoChain Streamlit Analytics Dashboard
========================================
Interactive 6-page executive dashboard visualizing Gold layer analytics:
1. Executive Overview
2. Sustainability & Environmental Impact
3. Secondary Marketplace Analytics
4. Product Lifecycle & Resale Retention
5. Component Failure & Quality Analysis
6. Financial & Buy-Back Program Insights

Data source: data/gold/*.csv (produced by the PySpark Medallion pipeline).
Theme: Dark glassmorphism matching dashboards/echochain_theme.json.
"""

import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Paths & Configuration
# ---------------------------------------------------------------------------
# Resolve the repo root regardless of whether the CWD is the repo root (local)
# or the app runs from a subpath (Streamlit Community Cloud).
if os.path.exists(os.path.join(os.getcwd(), "data", "gold")):
    ROOT_DIR = os.getcwd()
else:
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

GOLD_DIR = os.path.join(ROOT_DIR, "data", "gold")

GOLD_FILES = {
    "circularity": os.path.join(GOLD_DIR, "gold_circularity_metrics.csv"),
    "marketplace": os.path.join(GOLD_DIR, "gold_marketplace_analytics.csv"),
    "component": os.path.join(GOLD_DIR, "gold_component_failure.csv"),
    "sustainability": os.path.join(GOLD_DIR, "gold_sustainability_impact.csv"),
}

# EchoChain brand colors (from dashboards/echochain_theme.json)
COLORS = {
    "bg": "#0F172A",
    "card": "#1E293B",
    "border": "#334155",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
    "primary": "#10B981",   # emerald
    "secondary": "#06B6D4",  # cyan
    "tertiary": "#8B5CF6",  # violet
    "warning": "#F59E0B",   # amber
    "danger": "#EF4444",    # red
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": COLORS["text"], "family": "Segoe UI, sans-serif"},
        "colorway": [COLORS["primary"], COLORS["secondary"], COLORS["tertiary"], COLORS["warning"], COLORS["danger"]],
        "xaxis": {"gridcolor": "rgba(148,163,184,0.15)", "zerolinecolor": "rgba(148,163,184,0.2)"},
        "yaxis": {"gridcolor": "rgba(148,163,184,0.15)", "zerolinecolor": "rgba(148,163,184,0.2)"},
        "legend": {"bgcolor": "rgba(0,0,0,0)", "orientation": "h", "yanchor": "bottom", "y": 1.02},
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40},
    }
}

# ---------------------------------------------------------------------------
# Data Loading (cached)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_gold_data():
    """Load all Gold layer CSV tables into a dict of DataFrames."""
    data = {}
    for key, path in GOLD_FILES.items():
        try:
            if os.path.exists(path):
                data[key] = pd.read_csv(path)
            else:
                data[key] = pd.DataFrame()
        except Exception as e:  # pragma: no cover - defensive
            st.warning(f"Could not load {os.path.basename(path)}: {e}")
            data[key] = pd.DataFrame()
    return data


# ---------------------------------------------------------------------------
# UI Helpers
# ---------------------------------------------------------------------------
def inject_css():
    """Inject EchoChain dark glassmorphism theme CSS."""
    st.markdown(
        f"""
        <style>
        /* Global */
        .stApp {{
            background: {COLORS["bg"]};
            color: {COLORS["text"]};
        }}
        [data-testid="stSidebar"] {{
            background: #111c33;
            border-right: 1px solid {COLORS["border"]};
        }}
        [data-testid="stSidebar"] * {{
            color: {COLORS["text"]};
        }}

        /* Header */
        .echochain-header {{
            background: linear-gradient(90deg, #111c33 0%, #1E293B 100%);
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            padding: 18px 24px;
            margin-bottom: 20px;
        }}
        .echochain-header h1 {{
            margin: 0;
            color: {COLORS["text"]};
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        .echochain-header p {{
            margin: 4px 0 0 0;
            color: {COLORS["muted"]};
            font-size: 14px;
        }}
        .live-badge {{
            display: inline-block;
            background: {COLORS["primary"]};
            color: {COLORS["bg"]};
            font-weight: 700;
            font-size: 11px;
            padding: 4px 12px;
            border-radius: 20px;
            margin-left: 12px;
            vertical-align: middle;
            letter-spacing: 1px;
        }}

        /* KPI Cards */
        div[data-testid="stMetric"] {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        }}
        div[data-testid="stMetric"] label {{
            color: {COLORS["muted"]} !important;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {COLORS["primary"]};
            font-size: 26px;
            font-weight: 800;
        }}

        /* Section titles */
        .section-title {{
            color: {COLORS["secondary"]};
            font-size: 17px;
            font-weight: 700;
            margin: 26px 0 10px 0;
            border-left: 4px solid {COLORS["primary"]};
            padding-left: 12px;
        }}

        /* Dataframe */
        .stDataFrame {{
            border: 1px solid {COLORS["border"]};
            border-radius: 10px;
            overflow: hidden;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {COLORS["card"]};
            border-radius: 8px;
            padding: 6px 16px;
            border: 1px solid {COLORS["border"]};
        }}
        .stTabs [aria-selected="true"] {{
            background: {COLORS["primary"]} !important;
            color: {COLORS["bg"]} !important;
            font-weight: 700;
        }}

        /* Footer */
        .echochain-footer {{
            margin-top: 40px;
            padding-top: 16px;
            border-top: 1px solid {COLORS["border"]};
            color: {COLORS["muted"]};
            font-size: 12px;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title, subtitle=""):
    """Render the EchoChain branded page header."""
    st.markdown(
        f"""
        <div class="echochain-header">
            <h1>♻️ EchoChain Lakehouse Analytics <span class="live-badge">LIVE DATA</span></h1>
            <p>{title}{' — ' + subtitle if subtitle else ''}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(label, value, delta=None):
    """Render a styled KPI metric."""
    st.metric(label=label, value=value, delta=delta)


def render_section(title):
    """Render a section heading."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def render_footer():
    """Render page footer."""
    st.markdown(
        '<div class="echochain-footer">EchoChain · Circular Economy &amp; Secondary Market '
        'Lifecycle Analytics · Powered by PySpark Delta Lakehouse Gold Tables</div>',
        unsafe_allow_html=True,
    )


def empty_state(message="No data available. Run `python pyspark_pipeline/run_pipeline.py` to build Gold tables."):
    st.info(message)


# ---------------------------------------------------------------------------
# Plotly style helper
# ---------------------------------------------------------------------------
def style_fig(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    return fig


# ---------------------------------------------------------------------------
# Page 1: Executive Overview
# ---------------------------------------------------------------------------
def page_executive_overview(dfs):
    render_header(
        "Executive Overview Dashboard",
        "Macro circularity performance, resale volume, landfill diversion & buy-back ROI",
    )

    circ = dfs.get("circularity", pd.DataFrame())
    if circ.empty:
        empty_state()
        return

    # ---- KPI Row ----
    total_listings = int(circ["total_listings_count"].sum())
    avg_circularity = circ["circularity_score"].mean()
    avg_diversion = circ["landfill_diversion_pct"].mean()
    total_co2 = circ["co2_avoided_tons"].sum()
    total_resale_vol = dfs.get("marketplace", pd.DataFrame())["total_sales_volume_usd"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Circularity Score", f"{avg_circularity:.1f}%")
    c2.metric("Resale Volume USD", f"${total_resale_vol/1e6:.1f}M")
    c3.metric("Total Listings", f"{total_listings:,}")
    c4.metric("CO₂ Avoided", f"{total_co2:,.0f} Tons")
    c5.metric("Landfill Diversion", f"{avg_diversion:.1f}%")

    # ---- Charts ----
    col_left, col_right = st.columns(2)

    with col_left:
        render_section("Circularity Score by Product")
        fig = px.bar(
            circ.sort_values("circularity_score"),
            x="Product",
            y="circularity_score",
            color="circularity_score",
            color_continuous_scale=["#F59E0B", "#06B6D4", "#10B981"],
            labels={"circularity_score": "Circularity Score (%)"},
        )
        fig.update_traces(marker_line_width=0)
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    with col_right:
        render_section("Resale Index vs Avg Resale Price")
        fig = px.scatter(
            circ,
            x="avg_resale_price_usd",
            y="resale_index",
            size="total_listings_count",
            color="Manufacturer",
            hover_name="Product",
            labels={"avg_resale_price_usd": "Avg Resale Price (USD)", "resale_index": "Resale Index"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    render_section("Product Performance Table")
    cols = ["SKU", "Product", "Manufacturer", "Category", "resale_index", "circularity_score",
            "landfill_diversion_pct", "refurbishment_score", "co2_avoided_tons"]
    available = [c for c in cols if c in circ.columns]
    st.dataframe(circ[available].sort_values("circularity_score", ascending=False), width='stretch')


# ---------------------------------------------------------------------------
# Page 2: Sustainability & Environmental Impact
# ---------------------------------------------------------------------------
def page_sustainability(dfs):
    render_header(
        "Sustainability & Environmental Impact",
        "Carbon avoided, e-waste diversion, material recovery & carbon financial value",
    )

    circ = dfs.get("circularity", pd.DataFrame())
    sust = dfs.get("sustainability", pd.DataFrame())
    if sust.empty and circ.empty:
        empty_state()
        return

    # ---- KPI Row ----
    total_co2 = circ["co2_avoided_tons"].sum() if not circ.empty else 0
    carbon_value = sust["carbon_financial_savings_usd"].sum() if not sust.empty else 0
    avg_recovery = circ["refurbishment_score"].mean() if not circ.empty else 0
    total_units = int(circ["total_listings_count"].sum()) if not circ.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CO₂ Avoided (Tons)", f"{total_co2:,.0f}")
    c2.metric("Carbon Value", f"${carbon_value:,.0f}")
    c3.metric("Refurbishment Rate", f"{avg_recovery:.1f}%")
    c4.metric("Units Circulated", f"{total_units:,}")

    if not sust.empty:
        col_left, col_right = st.columns(2)

        with col_left:
            render_section("CO₂ Avoided by Manufacturer")
            fig = px.bar(
                sust.sort_values("total_co2_avoided_tons"),
                x="Manufacturer",
                y="total_co2_avoided_tons",
                color="total_co2_avoided_tons",
                color_continuous_scale="Viridis",
                labels={"total_co2_avoided_tons": "CO₂ Avoided (Tons)"},
            )
            style_fig(fig)
            st.plotly_chart(fig, width='stretch')

        with col_right:
            render_section("Carbon Financial Savings by Category")
            fig = px.bar(
                sust.sort_values("carbon_financial_savings_usd"),
                x="Category",
                y="carbon_financial_savings_usd",
                color="Category",
                labels={"carbon_financial_savings_usd": "Savings (USD)"},
            )
            style_fig(fig)
            st.plotly_chart(fig, width='stretch')

    if not circ.empty:
        render_section("Circularity vs Landfill Diversion by Product")
        fig = px.scatter(
            circ,
            x="landfill_diversion_pct",
            y="circularity_score",
            size="co2_avoided_tons",
            color="Category",
            hover_name="Product",
            labels={"landfill_diversion_pct": "Landfill Diversion (%)", "circularity_score": "Circularity Score (%)"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')


# ---------------------------------------------------------------------------
# Page 3: Secondary Marketplace Analytics
# ---------------------------------------------------------------------------
def page_marketplace(dfs):
    render_header(
        "Secondary Marketplace Analytics",
        "Pricing, seller ratings & listing volume across eBay, FB Marketplace, OLX & BackMarket",
    )

    mkt = dfs.get("marketplace", pd.DataFrame())
    if mkt.empty:
        empty_state()
        return

    # ---- Filters (Sidebar) ----
    st.sidebar.markdown("### 🔍 Marketplace Filters")
    marketplaces = ["All"] + sorted(mkt["marketplace"].unique().tolist())
    conditions = ["All"] + sorted(mkt["normalized_condition"].unique().tolist())
    locations = ["All"] + sorted(mkt["location"].unique().tolist())

    sel_mkt = st.sidebar.selectbox("Marketplace", marketplaces, key="mkt_sel_mkt")
    sel_cond = st.sidebar.selectbox("Condition", conditions, key="mkt_sel_cond")
    sel_loc = st.sidebar.selectbox("Location", locations, key="mkt_sel_loc")

    df = mkt.copy()
    if sel_mkt != "All":
        df = df[df["marketplace"] == sel_mkt]
    if sel_cond != "All":
        df = df[df["normalized_condition"] == sel_cond]
    if sel_loc != "All":
        df = df[df["location"] == sel_loc]

    # ---- KPIs ----
    total_listings = int(df["listings_count"].sum())
    avg_price = df["avg_price_usd"].mean()
    avg_rating = df["avg_seller_rating"].mean()
    total_sales = df["total_sales_volume_usd"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Listings", f"{total_listings:,}")
    c2.metric("Avg Resale Price", f"${avg_price:,.2f}")
    c3.metric("Avg Seller Rating", f"{avg_rating:.2f} / 5.0")
    c4.metric("Sales Volume", f"${total_sales:,.0f}")

    col_left, col_right = st.columns(2)

    with col_left:
        render_section("Average Resale Price by Condition")
        price_by_cond = df.groupby("normalized_condition")["avg_price_usd"].mean().reset_index()
        fig = px.bar(
            price_by_cond,
            x="normalized_condition",
            y="avg_price_usd",
            color="avg_price_usd",
            color_continuous_scale="Blues",
            labels={"normalized_condition": "Condition", "avg_price_usd": "Avg Price (USD)"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    with col_right:
        render_section("Listing Volume by Marketplace")
        vol_by_mkt = df.groupby("marketplace")["listings_count"].sum().reset_index()
        fig = px.pie(
            vol_by_mkt,
            names="marketplace",
            values="listings_count",
            hole=0.45,
            color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["tertiary"], COLORS["warning"]],
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    render_section("Seller Rating vs Price Heatmap")
    heat_data = df.pivot_table(
        index="marketplace", columns="normalized_condition", values="avg_seller_rating", aggfunc="mean"
    ).fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns,
        y=heat_data.index,
        colorscale="Tealgrn",
        texttemplate="%{z:.2f}",
        textfont={"color": COLORS["text"], "size": 11},
    ))
    style_fig(fig)
    st.plotly_chart(fig, width='stretch')


# ---------------------------------------------------------------------------
# Page 4: Product Lifecycle & Resale Retention
# ---------------------------------------------------------------------------
def page_lifecycle(dfs):
    render_header(
        "Product Lifecycle & Resale Retention",
        "Value retention, price depreciation & buy-back candidates across product portfolio",
    )

    circ = dfs.get("circularity", pd.DataFrame())
    if circ.empty:
        empty_state()
        return

    # ---- KPIs ----
    avg_resale_index = circ["resale_index"].mean()
    avg_price_retention = (circ["avg_resale_price_usd"] / circ["total_mfg_cost_usd"]).mean() * 100
    avg_mfg_cost = circ["total_mfg_cost_usd"].mean()
    avg_weight = circ["total_weight_g"].mean() / 1000

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Resale Index", f"{avg_resale_index:.2f}")
    c2.metric("Price Retention", f"{avg_price_retention:.1f}%")
    c3.metric("Avg Mfg Cost", f"${avg_mfg_cost:,.2f}")
    c4.metric("Avg Product Weight", f"{avg_weight:.2f} kg")

    col_left, col_right = st.columns(2)

    with col_left:
        render_section("Mfg Cost vs Avg Resale Price")
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Mfg Cost", x=circ["Product"], y=circ["total_mfg_cost_usd"], marker_color=COLORS["secondary"]))
        fig.add_trace(go.Bar(name="Avg Resale Price", x=circ["Product"], y=circ["avg_resale_price_usd"], marker_color=COLORS["primary"]))
        fig.update_layout(barmode="group")
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    with col_right:
        render_section("Resale Index by Product (Buy-Back Candidate)")
        fig = px.bar(
            circ.sort_values("resale_index"),
            x="Product",
            y="resale_index",
            color="resale_index",
            color_continuous_scale="RdYlGn",
            labels={"resale_index": "Resale Index"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    render_section("Condition Distribution (Refurbished vs Salvage)")
    cond_df = circ[["Product", "refurbished_count", "salvage_count"]].melt(
        id_vars="Product", var_name="Type", value_name="Count"
    )
    fig = px.bar(
        cond_df,
        x="Product",
        y="Count",
        color="Type",
        barmode="group",
        color_discrete_map={"refurbished_count": COLORS["primary"], "salvage_count": COLORS["danger"]},
    )
    style_fig(fig)
    st.plotly_chart(fig, width='stretch')


# ---------------------------------------------------------------------------
# Page 5: Component Failure & Quality Analysis
# ---------------------------------------------------------------------------
def page_component_failure(dfs):
    render_header(
        "Component Failure & Quality Analysis",
        "Warranty claims, repair cost ratios & repairability indices by component",
    )

    comp = dfs.get("component", pd.DataFrame())
    if comp.empty:
        empty_state()
        return

    # ---- KPIs ----
    total_claims = int(comp["claim_count"].sum())
    failure_idx = (total_claims / max(int(comp["warranty_claims_count"].sum()), 1)) * 1000 if "warranty_claims_count" in comp.columns else 0
    avg_repair = comp["avg_repair_cost_usd"].mean()
    avg_repairability = comp["repairability_index"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Warranty Claims", f"{total_claims:,}")
    c2.metric("Avg Repair Cost", f"${avg_repair:,.2f}")
    c3.metric("Repairability Index", f"{avg_repairability:.2f} / 10")
    c4.metric("Failure Index", f"{failure_idx:,.1f}")

    col_left, col_right = st.columns(2)

    with col_left:
        render_section("Most Failed Components")
        top_components = (
            comp.groupby("Component")["claim_count"].sum().reset_index().sort_values("claim_count", ascending=False).head(10)
        )
        fig = px.bar(
            top_components,
            x="claim_count",
            y="Component",
            orientation="h",
            color="claim_count",
            color_continuous_scale="Oranges",
            labels={"claim_count": "Claims"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    with col_right:
        render_section("Mfg Cost vs Repair Cost Ratio")
        fig = px.scatter(
            comp,
            x="manufacturing_cost_usd",
            y="avg_repair_cost_usd",
            size="claim_count",
            color="repair_cost_ratio",
            hover_name="Component",
            color_continuous_scale="RdYlGn_r",
            labels={"manufacturing_cost_usd": "Mfg Cost (USD)", "avg_repair_cost_usd": "Avg Repair Cost (USD)"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')

    # Supplier filter table
    st.sidebar.markdown("### 🔧 Component Filters")
    suppliers = ["All"] + sorted(comp["Supplier"].dropna().unique().tolist())
    sel_supplier = st.sidebar.selectbox("Supplier", suppliers, key="comp_sel_supplier")
    if sel_supplier != "All":
        comp = comp[comp["Supplier"] == sel_supplier]

    render_section("Component Failure Detail Table")
    cols = ["SKU", "Component", "Supplier", "claim_count", "avg_repair_cost_usd",
            "repair_cost_ratio", "repairability_index", "failure_rate"]
    available = [c for c in cols if c in comp.columns]
    st.dataframe(comp[available].sort_values("claim_count", ascending=False), width='stretch')


# ---------------------------------------------------------------------------
# Page 6: Financial & Buy-Back Program Insights
# ---------------------------------------------------------------------------
def page_financial(dfs):
    render_header(
        "Financial & Buy-Back Program Insights",
        "Buy-back margins, secondary revenue recovery & trade-in profitability",
    )

    circ = dfs.get("circularity", pd.DataFrame())
    mkt = dfs.get("marketplace", pd.DataFrame())
    if circ.empty and mkt.empty:
        empty_state()
        return

    # Buy-back margin = Avg Resale Price - (Mfg Cost * 0.40) - Avg Repair Cost
    # Approximated here using circularity metrics (repair cost proxy from component table).
    comp = dfs.get("component", pd.DataFrame())

    if not circ.empty:
        avg_repair = comp["avg_repair_cost_usd"].mean() if not comp.empty else 0
        circ = circ.copy()
        circ["buyback_margin"] = (
            circ["avg_resale_price_usd"] - (circ["total_mfg_cost_usd"] * 0.40) - avg_repair
        )
        circ["buyback_roi"] = (
            circ["buyback_margin"] / ((circ["total_mfg_cost_usd"] * 0.40) + avg_repair) * 100
        )

    # ---- KPIs ----
    avg_margin = circ["buyback_margin"].mean() if not circ.empty else 0
    avg_roi = circ["buyback_roi"].mean() if not circ.empty else 0
    secondary_rev = mkt["total_sales_volume_usd"].sum() if not mkt.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Buy-Back Margin", f"${avg_margin:,.2f} / unit")
    c2.metric("Buy-Back ROI", f"{avg_roi:.1f}%")
    c3.metric("Secondary Revenue", f"${secondary_rev:,.0f}")
    c4.metric("Avg Resale Price", f"${circ['avg_resale_price_usd'].mean():,.2f}" if not circ.empty else "—")

    col_left, col_right = st.columns(2)

    with col_left:
        render_section("Buy-Back Profitability by Product")
        if not circ.empty:
            fig = go.Figure(go.Waterfall(
                name="Buy-Back Margin",
                orientation="v",
                measure=["relative"] * len(circ),
                x=circ["Product"],
                y=circ["buyback_margin"],
                text=[f"${v:,.0f}" for v in circ["buyback_margin"]],
                connector={"line": {"color": COLORS["muted"]}},
                increasing={"marker": {"color": COLORS["primary"]}},
                decreasing={"marker": {"color": COLORS["danger"]}},
            ))
            style_fig(fig)
            st.plotly_chart(fig, width='stretch')

    with col_right:
        render_section("Buy-Back ROI by Category")
        if not circ.empty:
            roi_by_cat = circ.groupby("Category")["buyback_roi"].mean().reset_index().sort_values("buyback_roi")
            fig = px.bar(
                roi_by_cat,
                x="Category",
                y="buyback_roi",
                color="buyback_roi",
                color_continuous_scale="Blugrn",
                labels={"buyback_roi": "ROI (%)"},
            )
            style_fig(fig)
            st.plotly_chart(fig, width='stretch')

    if not mkt.empty:
        render_section("Sales Volume by Marketplace & Condition")
        vol = mkt.groupby(["marketplace", "normalized_condition"])["total_sales_volume_usd"].sum().reset_index()
        fig = px.bar(
            vol,
            x="marketplace",
            y="total_sales_volume_usd",
            color="normalized_condition",
            barmode="stack",
            labels={"marketplace": "Marketplace", "total_sales_volume_usd": "Sales Volume (USD)"},
        )
        style_fig(fig)
        st.plotly_chart(fig, width='stretch')


# ---------------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="EchoChain Analytics",
        page_icon="♻️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    # Sidebar navigation
    st.sidebar.markdown("## ♻️ EchoChain")
    st.sidebar.markdown("**Circular Economy Analytics**")
    st.sidebar.markdown("---")

    pages = {
        "📊 Executive Overview": page_executive_overview,
        "🌱 Sustainability": page_sustainability,
        "🏪 Marketplace Analytics": page_marketplace,
        "🔄 Product Lifecycle": page_lifecycle,
        "🔧 Component Quality": page_component_failure,
        "💰 Financial Insights": page_financial,
    }
    selection = st.sidebar.radio("Navigation", list(pages.keys()), label_visibility="collapsed")

    st.sidebar.markdown("---")
    st.sidebar.caption("Data: `data/gold/*.csv`")
    st.sidebar.caption("Medallion: Bronze → Silver → Gold")

    # Load data
    dfs = load_gold_data()

    # Render selected page
    pages[selection](dfs)

    render_footer()


if __name__ == "__main__":
    main()

