# EchoChain Data Dictionary

## 1. `gold_circularity_metrics` Table
| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `SKU` | String | Internal ERP SKU identifier | `SKU-APP-IP14P-256` |
| `Product` | String | Commercial product name | `iPhone 14 Pro 256GB` |
| `Manufacturer` | String | Brand/Manufacturer name | `Apple` |
| `Category` | String | Product category classification | `Smartphones` |
| `total_mfg_cost_usd` | Double | Sum of manufacturing cost across components | `480.00` |
| `total_carbon_footprint_kg` | Double | Manufacturing CO₂ footprint in kg | `65.5` |
| `total_listings_count` | Long | Total secondary market listings found | `5000` |
| `avg_resale_price_usd` | Double | Average secondary listing price in USD | `520.40` |
| `resale_index` | Double | Ratio of Avg Resale Price to Manufacturing Cost | `1.084` |
| `refurbishment_score` | Double | Percentage of listings sold as refurbished | `24.5%` |
| `landfill_diversion_pct` | Double | Percentage of non-salvage listings diverted | `95.8%` |
| `circularity_score` | Double | Composite circular economy score (0-100%) | `86.4%` |
| `co2_avoided_tons` | Double | Estimated CO₂ tonnage avoided via resale | `229.25` |

## 2. `gold_component_failure` Table
| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `SKU` | String | Internal product SKU | `SKU-SAM-GS23U-512` |
| `Component` | String | Sub-assembly component name | `Dynamic AMOLED Screen` |
| `Material` | String | Primary material composition | `Gorilla Glass` |
| `claim_count` | Long | Total warranty claims logged for component | `412` |
| `avg_repair_cost_usd` | Double | Average repair cost in USD | `185.00` |
| `repair_cost_ratio` | Double | Ratio of repair cost to component cost | `1.42` |
| `repairability_index` | Double | Composite score (0-10) for ease of repair | `8.40` |

## 3. `gold_marketplace_analytics` Table
| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `marketplace` | String | Source platform (`eBay`, `FB`, `OLX`, `BackMarket`) | `eBay` |
| `normalized_condition` | String | Standardized condition tag | `Refurbished` |
| `location` | String | Geographic listing origin | `Berlin, Germany` |
| `listings_count` | Long | Count of active listings | `12500` |
| `avg_price_usd` | Double | Average listing price in USD | `415.50` |
| `total_sales_volume_usd` | Double | Total monetary sales volume | $5,193,750.00 |

## 4. `gold_sustainability_impact` Table
| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `Manufacturer` | String | OEM Manufacturer | `Dell` |
| `Category` | String | Category | `Laptops` |
| `units_circulated` | Long | Total units circulated in secondary market | `4850` |
| `total_co2_avoided_tons` | Double | Total CO₂ avoided in Metric Tons | `950.4` |
| `carbon_financial_savings_usd` | Double | Monetary carbon credit value ($85/ton) | $80,784.00 |
| `avg_circularity_score` | Double | Average circularity score % | `84.1%` |
