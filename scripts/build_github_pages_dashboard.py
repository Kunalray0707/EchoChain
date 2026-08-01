"""
EchoChain GitHub Pages Static Dashboard Builder
================================================
Reads the Gold layer CSV tables and builds a self-contained, fully static
HTML dashboard (dark glassmorphism theme, 6 pages, Plotly.js charts) that
mirrors the Streamlit app. The result is served directly by GitHub Pages
with no Python/Streamlit runtime required.

Output: docs/index.html  (GitHub Pages serves /EchoChain from the docs/ folder)
"""

import json
import os

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GOLD_DIR = os.path.join(ROOT, "data", "gold")
OUT_DIR = os.path.join(ROOT, "docs")
OUT_FILE = os.path.join(OUT_DIR, "index.html")

GOLD_FILES = {
    "circularity": "gold_circularity_metrics.csv",
    "marketplace": "gold_marketplace_analytics.csv",
    "component": "gold_component_failure.csv",
    "sustainability": "gold_sustainability_impact.csv",
}


def load_data():
    """Load all Gold CSVs into a JSON-serializable dict."""
    data = {}
    for key, fname in GOLD_FILES.items():
        path = os.path.join(GOLD_DIR, fname)
        if os.path.exists(path):
            df = pd.read_csv(path)
            df = df.where(pd.notnull(df), None)
            data[key] = df.to_dict(orient="records")
        else:
            data[key] = []
    return data


def build_html(data):
    """Return the full static dashboard HTML with embedded JSON data."""
    data_json = json.dumps(data, default=str)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>EchoChain Analytics Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #0F172A;
    color: #F8FAFC;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
  }}
  .app {{ max-width: 1440px; margin: 0 auto; padding: 20px; }}

  /* Header */
  .header {{
    background: linear-gradient(90deg, #111c33 0%, #1E293B 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 18px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }}
  .header h1 {{ font-size: 24px; font-weight: 800; }}
  .header p {{ color: #94A3B8; font-size: 14px; margin-top: 4px; }}
  .live-badge {{
    background: #10B981; color: #0F172A; font-weight: 700; font-size: 12px;
    padding: 5px 14px; border-radius: 20px; letter-spacing: 1px; white-space: nowrap;
  }}

  /* Nav Tabs */
  .nav {{
    display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 22px;
  }}
  .nav button {{
    background: #1E293B; border: 1px solid #334155; color: #F8FAFC;
    padding: 10px 18px; border-radius: 10px; cursor: pointer;
    font-size: 14px; font-weight: 600; transition: all .15s;
  }}
  .nav button:hover {{ border-color: #10B981; }}
  .nav button.active {{ background: #10B981; color: #0F172A; font-weight: 800; }}
  .page {{ display: none; }}
  .page.active {{ display: block; }}

  /* KPI cards */
  .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 24px; }}
  .kpi {{
    background: #1E293B; border: 1px solid #334155; border-radius: 12px;
    padding: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.25);
  }}
  .kpi .label {{ color: #94A3B8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .6px; }}
  .kpi .value {{ color: #10B981; font-size: 26px; font-weight: 800; margin-top: 6px; }}

  .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .chart {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 10px; }}
  .chart.full {{ grid-column: 1 / -1; }}
  .chart h3 {{ color: #06B6D4; font-size: 15px; font-weight: 700; margin: 8px 6px; border-left: 4px solid #10B981; padding-left: 10px; }}
  .plotly {{ width: 100%; height: 380px; }}

  .table-wrap {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 14px; overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ color: #94A3B8; text-align: left; padding: 8px; border-bottom: 1px solid #334155; }}
  td {{ padding: 8px; border-bottom: 1px solid #1E293B; }}

  .footer {{ margin-top: 30px; padding-top: 16px; border-top: 1px solid #334155; color: #94A3B8; font-size: 12px; text-align: center; }}
  @media (max-width: 900px) {{ .charts {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <div>
      <h1>♻️ EchoChain Lakehouse Analytics <span class="live-badge">LIVE DATA</span></h1>
      <p id="page-subtitle">Executive Overview Dashboard — Macro circularity performance, resale volume & buy-back ROI</p>
    </div>
  </div>

  <div class="nav" id="nav"></div>

  <div class="page" id="page-0"></div>
  <div class="page" id="page-1"></div>
  <div class="page" id="page-2"></div>
  <div class="page" id="page-3"></div>
  <div class="page" id="page-4"></div>
  <div class="page" id="page-5"></div>

  <div class="footer">EchoChain · Circular Economy &amp; Secondary Market Lifecycle Analytics · Static GitHub Pages Dashboard (mirrors Streamlit app)</div>
</div>

<script>
const DATA = {data_json};

const COLORS = {{
  primary: '#10B981', secondary: '#06B6D4', tertiary: '#8B5CF6',
  warning: '#F59E0B', danger: '#EF4444', text: '#F8FAFC', muted: '#94A3B8'
}};

const LAYOUT_BASE = {{
  paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
  font: {{ color: COLORS.text, family: 'Segoe UI, sans-serif' }},
  colorway: [COLORS.primary, COLORS.secondary, COLORS.tertiary, COLORS.warning, COLORS.danger],
  xaxis: {{ gridcolor: 'rgba(148,163,184,0.15)', zerolinecolor: 'rgba(148,163,184,0.2)' }},
  yaxis: {{ gridcolor: 'rgba(148,163,184,0.15)', zerolinecolor: 'rgba(148,163,184,0.2)' }},
  legend: {{ bgcolor: 'rgba(0,0,0,0)', orientation: 'h', y: 1.12 }},
  margin: {{ l: 50, r: 20, t: 30, b: 50 }},
  showlegend: false
}};

const PAGES = [
  {{ id: 0, name: '📊 Executive Overview', subtitle: 'Executive Overview Dashboard', render: renderPage0 }},
  {{ id: 1, name: '🌱 Sustainability', subtitle: 'Sustainability & Environmental Impact', render: renderPage1 }},
  {{ id: 2, name: '🏪 Marketplace Analytics', subtitle: 'Secondary Marketplace Analytics', render: renderPage2 }},
  {{ id: 3, name: '🔄 Product Lifecycle', subtitle: 'Product Lifecycle & Resale Retention', render: renderPage3 }},
  {{ id: 4, name: '🔧 Component Quality', subtitle: 'Component Failure & Quality Analysis', render: renderPage4 }},
  {{ id: 5, name: '💰 Financial Insights', subtitle: 'Financial & Buy-Back Program Insights', render: renderPage5 }},
];

const circ = DATA.circularity || [];
const mkt = DATA.marketplace || [];
const comp = DATA.component || [];
const sust = DATA.sustainability || [];

const fmt = (n, d=1) => (n==null? '—' : Number(n).toLocaleString(undefined, {{maximumFractionDigits:d}}));
const money = (n, d=1) => (n==null? '—' : '$' + Number(n).toLocaleString(undefined, {{maximumFractionDigits:d}}));

function kpiGrid(html) {{ return `<div class="kpis">${{html}}</div>`; }}
function kpi(label, value) {{ return `<div class="kpi"><div class="label">${{label}}</div><div class="value">${{value}}</div></div>`; }}
function chart(title, divId, full=false) {{
  return `<div class="chart ${{full?'full':''}}"><h3>${{title}}</h3><div class="plotly" id="${{divId}}"></div></div>`;
}}

function renderPage0() {{
  const el = document.getElementById('page-0');
  const totalListings = circ.reduce((s,r)=>s+Number(r.total_listings_count||0),0);
  const avgCirc = circ.reduce((s,r)=>s+Number(r.circularity_score||0),0)/(circ.length||1);
  const avgDiv = circ.reduce((s,r)=>s+Number(r.landfill_diversion_pct||0),0)/(circ.length||1);
  const totalCO2 = circ.reduce((s,r)=>s+Number(r.co2_avoided_tons||0),0);
  const totalRev = mkt.reduce((s,r)=>s+Number(r.total_sales_volume_usd||0),0);

  el.innerHTML = kpiGrid(
    kpi('Circularity Score', avgCirc.toFixed(1)+'%') +
    kpi('Resale Volume USD', '$'+(totalRev/1e6).toFixed(1)+'M') +
    kpi('Total Listings', fmt(totalListings,0)) +
    kpi('CO₂ Avoided', fmt(totalCO2,0)+' Tons') +
    kpi('Landfill Diversion', avgDiv.toFixed(1)+'%')
  ) + '<div class="charts">' +
    chart('Circularity Score by Product','c0a') +
    chart('Resale Index vs Avg Resale Price','c0b') +
    '</div>';

  const sorted = [...circ].sort((a,b)=>Number(a.circularity_score)-Number(b.circularity_score));
  Plotly.newPlot('c0a', [{{
    type:'bar', x: sorted.map(r=>r.Product), y: sorted.map(r=>Number(r.circularity_score)),
    marker: {{ color: sorted.map(r=>Number(r.circularity_score)), colorscale: [['0','#F59E0B'],['0.5','#06B6D4'],['1','#10B981']] }},
    hovertemplate: '%{{x}}: %{{y:.1f}}%<extra></extra>'
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'Circularity Score (%)'}}}});

  Plotly.newPlot('c0b', [{{
    type:'scatter', mode:'markers',
    x: circ.map(r=>Number(r.avg_resale_price_usd)), y: circ.map(r=>Number(r.resale_index)),
    text: circ.map(r=>r.Product), hovertemplate: '%{{text}}<br>Price: $%{{x:,.0f}}<br>Index: %{{y:.2f}}<extra></extra>',
    marker: {{ size: circ.map(r=>Math.min(40, 8+Number(r.total_listings_count)/200)), color: circ.map(r=>r.Manufacturer) }}
  }}], {{...LAYOUT_BASE, xaxis:{{...LAYOUT_BASE.xaxis, title:'Avg Resale Price (USD)'}}, yaxis:{{...LAYOUT_BASE.yaxis, title:'Resale Index'}}}});

  const perfCols = ['SKU','Product','Manufacturer','Category','resale_index','circularity_score','landfill_diversion_pct','refurbishment_score','co2_avoided_tons'];
  const rows = [...circ].sort((a,b)=>Number(b.circularity_score)-Number(a.circularity_score)).slice(0,10);
  let tbl = `<div class="table-wrap"><table><thead><tr>${{perfCols.map(c=>`<th>${{c}}</th>`).join('')}}</tr></thead><tbody>`;
  rows.forEach(r=>{{ tbl += `<tr>${{perfCols.map(c=>`<td>${{r[c]!=null?r[c]:'—'}}</td>`).join('')}}</tr>`; }});
  el.innerHTML += tbl + '</tbody></table></div>';
}}

function renderPage1() {{
  const el = document.getElementById('page-1');
  const totalCO2 = circ.reduce((s,r)=>s+Number(r.co2_avoided_tons||0),0);
  const carbonVal = sust.reduce((s,r)=>s+Number(r.carbon_financial_savings_usd||0),0);
  const avgRecovery = circ.reduce((s,r)=>s+Number(r.refurbishment_score||0),0)/(circ.length||1);
  const totalUnits = circ.reduce((s,r)=>s+Number(r.total_listings_count||0),0);

  el.innerHTML = kpiGrid(
    kpi('CO₂ Avoided (Tons)', fmt(totalCO2,0)) +
    kpi('Carbon Value', money(carbonVal,0)) +
    kpi('Refurbishment Rate', avgRecovery.toFixed(1)+'%') +
    kpi('Units Circulated', fmt(totalUnits,0))
  ) + '<div class="charts">' +
    chart('CO₂ Avoided by Manufacturer','c1a') +
    chart('Carbon Financial Savings by Category','c1b') +
    chart('Circularity vs Landfill Diversion','c1c', true) +
    '</div>';

  const byMfg = [...sust].sort((a,b)=>Number(a.total_co2_avoided_tons)-Number(b.total_co2_avoided_tons));
  Plotly.newPlot('c1a', [{{
    type:'bar', x: byMfg.map(r=>r.Manufacturer), y: byMfg.map(r=>Number(r.total_co2_avoided_tons)),
    marker: {{ color: byMfg.map(r=>Number(r.total_co2_avoided_tons)), colorscale:'Viridis' }},
    hovertemplate: '%{{y:,.0f}} tons<extra></extra>'
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'CO₂ Avoided (Tons)'}}}});

  const byCat = [...sust].sort((a,b)=>Number(a.carbon_financial_savings_usd)-Number(b.carbon_financial_savings_usd));
  Plotly.newPlot('c1b', [{{
    type:'bar', x: byCat.map(r=>r.Category), y: byCat.map(r=>Number(r.carbon_financial_savings_usd)),
    marker: {{ color: byCat.map(r=>r.Category) }},
    hovertemplate: '$%{{y:,.0f}}<extra></extra>'
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'Savings (USD)'}}}});

  Plotly.newPlot('c1c', [{{
    type:'scatter', mode:'markers',
    x: circ.map(r=>Number(r.landfill_diversion_pct)), y: circ.map(r=>Number(r.circularity_score)),
    text: circ.map(r=>r.Product), hovertemplate:'%{{text}}<extra></extra>',
    marker: {{ size: circ.map(r=>Math.min(40, 8+Number(r.co2_avoided_tons)/50)), color: circ.map(r=>r.Category) }}
  }}], {{...LAYOUT_BASE, xaxis:{{...LAYOUT_BASE.xaxis, title:'Landfill Diversion (%)'}}, yaxis:{{...LAYOUT_BASE.yaxis, title:'Circularity Score (%)'}}}});
}}

function renderPage2() {{
  const el = document.getElementById('page-2');
  const totalListings = mkt.reduce((s,r)=>s+Number(r.listings_count||0),0);
  const avgPrice = mkt.reduce((s,r)=>s+Number(r.avg_price_usd||0),0)/(mkt.length||1);
  const avgRating = mkt.reduce((s,r)=>s+Number(r.avg_seller_rating||0),0)/(mkt.length||1);
  const totalSales = mkt.reduce((s,r)=>s+Number(r.total_sales_volume_usd||0),0);

  el.innerHTML = kpiGrid(
    kpi('Total Listings', fmt(totalListings,0)) +
    kpi('Avg Resale Price', money(avgPrice,2)) +
    kpi('Avg Seller Rating', avgRating.toFixed(2)+' / 5.0') +
    kpi('Sales Volume', money(totalSales,0))
  ) + '<div class="charts">' +
    chart('Average Resale Price by Condition','c2a') +
    chart('Listing Volume by Marketplace','c2b') +
    chart('Seller Rating Heatmap (Marketplace × Condition)','c2c', true) +
    '</div>';

  const condAgg = {{}};
  mkt.forEach(r=>{{
    const c = r.normalized_condition||'Unknown';
    condAgg[c] = condAgg[c]||{{n:0,sum:0}};
    condAgg[c].n++; condAgg[c].sum += Number(r.avg_price_usd||0);
  }});
  const conds = Object.entries(condAgg).map(([k,v])=>({{c:k, price:v.sum/v.n}}));
  conds.sort((a,b)=>a.price-b.price);
  Plotly.newPlot('c2a', [{{
    type:'bar', x: conds.map(r=>r.c), y: conds.map(r=>r.price),
    marker: {{ color: conds.map(r=>r.price), colorscale:'Blues' }},
    hovertemplate:'$%{{y:,.2f}}<extra></extra>'
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'Avg Price (USD)'}}}});

  const mktAgg = {{}};
  mkt.forEach(r=>{{ mktAgg[r.marketplace] = (mktAgg[r.marketplace]||0)+Number(r.listings_count||0); }});
  const mkts = Object.entries(mktAgg).map(([k,v])=>({{name:k,val:v}}));
  Plotly.newPlot('c2b', [{{
    type:'pie', labels: mkts.map(r=>r.name), values: mkts.map(r=>r.val), hole:.45,
    marker: {{ colors: [COLORS.primary, COLORS.secondary, COLORS.tertiary, COLORS.warning, COLORS.danger] }},
    textinfo:'percent+label', textposition:'inside'
  }}], {{...LAYOUT_BASE, showlegend:true}});

  // Heatmap
  const condList = [...new Set(mkt.map(r=>r.normalized_condition||'Unknown'))];
  const mktList = [...new Set(mkt.map(r=>r.marketplace))];
  const z = mktList.map(m=>condList.map(c=>{{
    const hits = mkt.filter(r=>r.marketplace===m && (r.normalized_condition||'Unknown')===c);
    return hits.length? hits.reduce((s,r)=>s+Number(r.avg_seller_rating||0),0)/hits.length : 0;
  }}));
  Plotly.newPlot('c2c', [{{
    type:'heatmap', z, x: condList, y: mktList, colorscale:'Tealgrn',
    texttemplate:'%{{z:.2f}}', textfont:{{color:COLORS.text, size:11}}
  }}], {{...LAYOUT_BASE, xaxis:{{...LAYOUT_BASE.xaxis, title:'Condition'}}, yaxis:{{...LAYOUT_BASE.yaxis, title:'Marketplace'}}}});
}}

function renderPage3() {{
  const el = document.getElementById('page-3');
  const avgIndex = circ.reduce((s,r)=>s+Number(r.resale_index||0),0)/(circ.length||1);
  const avgRet = circ.reduce((s,r)=>s+(Number(r.avg_resale_price_usd||0)/Math.max(Number(r.total_mfg_cost_usd||1),1))*100,0)/(circ.length||1);
  const avgMfg = circ.reduce((s,r)=>s+Number(r.total_mfg_cost_usd||0),0)/(circ.length||1);
  const avgW = circ.reduce((s,r)=>s+Number(r.total_weight_g||0),0)/(circ.length||1)/1000;

  el.innerHTML = kpiGrid(
    kpi('Resale Index', avgIndex.toFixed(2)) +
    kpi('Price Retention', avgRet.toFixed(1)+'%') +
    kpi('Avg Mfg Cost', money(avgMfg,2)) +
    kpi('Avg Product Weight', avgW.toFixed(2)+' kg')
  ) + '<div class="charts">' +
    chart('Mfg Cost vs Avg Resale Price','c3a') +
    chart('Resale Index by Product (Buy-Back Candidate)','c3b') +
    chart('Condition Distribution (Refurbished vs Salvage)','c3c', true) +
    '</div>';

  Plotly.newPlot('c3a', [
    {{ type:'bar', name:'Mfg Cost', x: circ.map(r=>r.Product), y: circ.map(r=>Number(r.total_mfg_cost_usd)), marker:{{color:COLORS.secondary}} }},
    {{ type:'bar', name:'Avg Resale Price', x: circ.map(r=>r.Product), y: circ.map(r=>Number(r.avg_resale_price_usd)), marker:{{color:COLORS.primary}} }}
  ], {{...LAYOUT_BASE, barmode:'group', showlegend:true, yaxis:{{...LAYOUT_BASE.yaxis, title:'USD'}}}});

  const sortedIdx = [...circ].sort((a,b)=>Number(a.resale_index)-Number(b.resale_index));
  Plotly.newPlot('c3b', [{{
    type:'bar', x: sortedIdx.map(r=>r.Product), y: sortedIdx.map(r=>Number(r.resale_index)),
    marker: {{ color: sortedIdx.map(r=>Number(r.resale_index)), colorscale:'RdYlGn' }},
    hovertemplate:'%{{y:.2f}}<extra></extra>'
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'Resale Index'}}}});

  const condData = [];
  circ.forEach(r=>{{
    condData.push({{Product:r.Product, Type:'Refurbished', Count:Number(r.refurbished_count||0)}});
    condData.push({{Product:r.Product, Type:'Salvage', Count:Number(r.salvage_count||0)}});
  }});
  Plotly.newPlot('c3c', [{{
    type:'bar', x: condData.map(r=>r.Product), y: condData.map(r=>r.Count),
    color: condData.map(r=>r.Type),
    colors: [COLORS.primary, COLORS.danger],
    transforms: [{{ type:'groupby', groups: condData.map(r=>r.Type) }}],
    hovertemplate:'%{{y:,.0f}}<extra></extra>'
  }}], {{...LAYOUT_BASE, barmode:'group', showlegend:true, yaxis:{{...LAYOUT_BASE.yaxis, title:'Count'}}}});
}}

function renderPage4() {{
  const el = document.getElementById('page-4');
  const totalClaims = comp.reduce((s,r)=>s+Number(r.claim_count||0),0);
  const avgRepair = comp.reduce((s,r)=>s+Number(r.avg_repair_cost_usd||0),0)/(comp.length||1);
  const avgRepairIdx = comp.reduce((s,r)=>s+Number(r.repairability_index||0),0)/(comp.length||1);
  const failureIdx = totalClaims / Math.max((comp.reduce((s,r)=>s+Number(r.warranty_claims_count||0),0)),1) * 1000;

  el.innerHTML = kpiGrid(
    kpi('Total Warranty Claims', fmt(totalClaims,0)) +
    kpi('Avg Repair Cost', money(avgRepair,2)) +
    kpi('Repairability Index', avgRepairIdx.toFixed(2)+' / 10') +
    kpi('Failure Index', fmt(failureIdx,1))
  ) + '<div class="charts">' +
    chart('Most Failed Components','c4a') +
    chart('Mfg Cost vs Repair Cost Ratio','c4b') +
    chart('Component Failure Detail Table','c4c', true) +
    '</div>';

  const compAgg = {{}};
  comp.forEach(r=>{{ const c = r.Component||'Unknown'; compAgg[c]=(compAgg[c]||0)+Number(r.claim_count||0); }});
  const topComp = Object.entries(compAgg).map(([k,v])=>({{c:k,v}})).sort((a,b)=>b.v-a.v).slice(0,10);
  Plotly.newPlot('c4a', [{{
    type:'bar', orientation:'h', x: topComp.map(r=>r.v), y: topComp.map(r=>r.c),
    marker: {{ color: topComp.map(r=>r.v), colorscale:'Oranges' }},
    hovertemplate:'%{{x:,.0f}} claims<extra></extra>'
  }}], {{...LAYOUT_BASE, xaxis:{{...LAYOUT_BASE.xaxis, title:'Claims'}}}});

  Plotly.newPlot('c4b', [{{
    type:'scatter', mode:'markers',
    x: comp.map(r=>Number(r.manufacturing_cost_usd)), y: comp.map(r=>Number(r.avg_repair_cost_usd)),
    text: comp.map(r=>r.Component), hovertemplate:'%{{text}}<extra></extra>',
    marker: {{ size: comp.map(r=>Math.min(40, 5+Number(r.claim_count)/20)), color: comp.map(r=>Number(r.repair_cost_ratio)), colorscale:'RdYlGn_r' }}
  }}], {{...LAYOUT_BASE, xaxis:{{...LAYOUT_BASE.xaxis, title:'Mfg Cost (USD)'}}, yaxis:{{...LAYOUT_BASE.yaxis, title:'Avg Repair Cost (USD)'}}}});

  const cols4 = ['SKU','Component','Supplier','claim_count','avg_repair_cost_usd','repair_cost_ratio','repairability_index','failure_rate'];
  const rows4 = [...comp].sort((a,b)=>Number(b.claim_count)-Number(a.claim_count)).slice(0,15);
  let tbl = `<div class="table-wrap"><table><thead><tr>${{cols4.map(c=>`<th>${{c}}</th>`).join('')}}</tr></thead><tbody>`;
  rows4.forEach(r=>{{ tbl += `<tr>${{cols4.map(c=>`<td>${{r[c]!=null?r[c]:'—'}}</td>`).join('')}}</tr>`; }});
  el.innerHTML += tbl + '</tbody></table></div>';
}}

function renderPage5() {{
  const el = document.getElementById('page-5');
  const avgRepair = comp.reduce((s,r)=>s+Number(r.avg_repair_cost_usd||0),0)/(comp.length||1);
  const buyback = circ.map(r=>{{
    const margin = Number(r.avg_resale_price_usd||0) - Number(r.total_mfg_cost_usd||0)*0.40 - avgRepair;
    const roi = margin / (Number(r.total_mfg_cost_usd||0)*0.40 + avgRepair) * 100;
    return {{...r, margin, roi}};
  }});
  const avgMargin = buyback.reduce((s,r)=>s+r.margin,0)/(buyback.length||1);
  const avgRoi = buyback.reduce((s,r)=>s+r.roi,0)/(buyback.length||1);
  const secRev = mkt.reduce((s,r)=>s+Number(r.total_sales_volume_usd||0),0);

  el.innerHTML = kpiGrid(
    kpi('Buy-Back Margin', money(avgMargin,2)+' / unit') +
    kpi('Buy-Back ROI', avgRoi.toFixed(1)+'%') +
    kpi('Secondary Revenue', money(secRev,0)) +
    kpi('Avg Resale Price', money(circ.reduce((s,r)=>s+Number(r.avg_resale_price_usd||0),0)/(circ.length||1),2))
  ) + '<div class="charts">' +
    chart('Buy-Back Profitability by Product','c5a') +
    chart('Buy-Back ROI by Category','c5b') +
    chart('Sales Volume by Marketplace & Condition','c5c', true) +
    '</div>';

  Plotly.newPlot('c5a', [{{
    type:'waterfall', orientation:'v',
    x: buyback.map(r=>r.Product), y: buyback.map(r=>r.margin),
    text: buyback.map(r=>'$'+Math.round(r.margin)),
    connector: {{ line: {{ color: COLORS.muted }} }},
    increasing: {{ marker: {{ color: COLORS.primary }} }},
    decreasing: {{ marker: {{ color: COLORS.danger }} }}
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'Buy-Back Margin (USD)'}}}});

  const roiByCat = {{}};
  buyback.forEach(r=>{{ roiByCat[r.Category]=roiByCat[r.Category]||{{n:0,sum:0}}; roiByCat[r.Category].n++; roiByCat[r.Category].sum+=r.roi; }});
  const cats = Object.entries(roiByCat).map(([k,v])=>({{c:k, roi:v.sum/v.n}})).sort((a,b)=>a.roi-b.roi);
  Plotly.newPlot('c5b', [{{
    type:'bar', x: cats.map(r=>r.c), y: cats.map(r=>r.roi),
    marker: {{ color: cats.map(r=>r.roi), colorscale:'Blugrn' }},
    hovertemplate:'%{{y:.1f}}%<extra></extra>'
  }}], {{...LAYOUT_BASE, yaxis:{{...LAYOUT_BASE.yaxis, title:'ROI (%)'}}}});

  const volAgg = {{}};
  mkt.forEach(r=>{{
    const key = r.marketplace + '::' + (r.normalized_condition||'Unknown');
    volAgg[key] = (volAgg[key]||0)+Number(r.total_sales_volume_usd||0);
  }});
  const volRows = Object.entries(volAgg).map(([k,v])=>{{ const [m,c]=k.split('::'); return {{m,c,v}}; }});
  const volMkts = [...new Set(volRows.map(r=>r.m))];
  const volConds = [...new Set(volRows.map(r=>r.c))];
  const traces = volConds.map(cond=>({{
    type:'bar', name: cond, x: volMkts,
    y: volMkts.map(m=>{{ const hit = volRows.find(r=>r.m===m&&r.c===cond); return hit? hit.v : 0; }})
  }}));
  Plotly.newPlot('c5c', traces, {{...LAYOUT_BASE, barmode:'stack', showlegend:true, yaxis:{{...LAYOUT_BASE.yaxis, title:'Sales Volume (USD)'}}}});
}}

function showPage(id) {{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('page-'+id).classList.add('active');
  document.getElementById('page-subtitle').textContent = PAGES[id].subtitle;
  document.querySelectorAll('.nav button').forEach((b,i)=>b.classList.toggle('active', i===id));
}}

function init() {{
  const nav = document.getElementById('nav');
  PAGES.forEach(p=>{{
    const btn = document.createElement('button');
    btn.textContent = p.name;
    btn.onclick = () => {{ showPage(p.id); p.render(); }};
    nav.appendChild(btn);
  }});
  showPage(0);
  PAGES[0].render();
  window.addEventListener('resize', () => {{ PAGES.forEach(p=>{{ const el=document.getElementById('page-'+p.id); if(el.classList.contains('active') && p.render) p.render(); }}); }});
}}

init();
</script>
</body>
</html>
"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    data = load_data()
    html = build_html(data)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Built static dashboard: {OUT_FILE}")
    print(
        f"[OK] Embedded records: circularity={len(data['circularity'])}, "
        f"marketplace={len(data['marketplace'])}, component={len(data['component'])}, "
        f"sustainability={len(data['sustainability'])}"
    )


if __name__ == "__main__":
    main()
