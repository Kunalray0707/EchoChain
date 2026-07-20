# EchoChain Business KPIs & Circular Economy Formulas

## 1. Circularity Score (%)
Computes the overall circular economy performance of a product based on secondary market value retention and landfill diversion rate.

$$\text{Resale Index} = \frac{\text{Average Resale Price (USD)}}{\text{Total Manufacturing Cost (USD)}}$$

$$\text{Landfill Diversion \%} = \frac{\text{Total Listings} - \text{Salvage Listings}}{\text{Total Listings}} \times 100$$

$$\text{Circularity Score (\%)} = \left(0.5 \times \text{Resale Index} + 0.5 \times \frac{\text{Landfill Diversion \%}}{100}\right) \times 100$$

---

## 2. CO₂ Avoided (Tons)
Quantifies greenhouse gas emissions avoided by extending product lifetime through secondary market circulation instead of new manufacturing.

$$\text{CO}_2\text{ Avoided (Tons)} = \frac{\text{Secondary Units Circulated} \times \text{Mfg Carbon Footprint (kg)} \times 0.70}{1000}$$

---

## 3. Carbon Financial Value (USD)
Monetizes environmental emissions savings using carbon offset credit valuation ($85 / Metric Ton CO₂e).

$$\text{Carbon Financial Value (USD)} = \text{CO}_2\text{ Avoided (Tons)} \times \$85.00$$

---

## 4. Component Failure Index
Identifies component quality risk per 1,000 secondary units.

$$\text{Component Failure Index} = \frac{\text{Warranty Claims Count}}{\text{Total Listed Units}} \times 1000$$

---

## 5. Repairability Index (0-10 Score)
Evaluates component repair feasibility based on claim frequency and relative repair cost.

$$\text{Repair Cost Ratio} = \frac{\text{Average Repair Cost (USD)}}{\text{Component Manufacturing Cost (USD)}}$$

$$\text{Repairability Index} = \max\left(0, 10.0 - \frac{\text{Warranty Claims}}{100.0}\right)$$

---

## 6. OEM Buy-Back Program Margin (USD)
Models net profitability for manufacturers launching direct certified trade-in/buy-back programs.

$$\text{Buy-Back Margin (USD)} = \text{Avg Resale Price} - (\text{Mfg Cost} \times 0.40) - \text{Avg Repair Cost}$$

$$\text{Buy-Back ROI (\%)} = \frac{\text{Buy-Back Margin}}{\text{Trade-in Cost} + \text{Repair Cost}} \times 100$$
