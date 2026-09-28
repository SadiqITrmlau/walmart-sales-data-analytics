# 📈 Walmart Market Tableau Analytics Architecture

> **Author: Sadiq Khan**  
> *Tableau Desktop / Tableau Public Implementation Guide*

This document provides the exact blueprints, calculated fields, Level of Detail (LOD) expressions, and layout parameters to build and publish the **Walmart Market Dashboard** in **Tableau Desktop / Tableau Public**.

---

## 🗂️ Data Connections & Model in Tableau
1. Connect to `data/weekly_revenue.csv`, `data/brand_summary.csv`, and `data/stores.csv` (or connect directly to SQLite `walmart_analytics.db`).
2. Join `stores.csv` and `regions.csv` on `region_id = region_id`.

---

## 📐 Tableau Calculated Fields & LOD Expressions

### 1. Profit Margin (%)
```tableau
SUM([Profit]) / SUM([Revenue])
```
*Format: Percentage with 2 decimals.*

### 2. Return Rate (%)
```tableau
SUM([Returns Count]) / SUM([Transactions])
```
*Format: Percentage with 2 decimals.*

### 3. Level of Detail (LOD) — Total Regional Revenue
```tableau
{ FIXED [Store Country] : SUM([Revenue]) }
```

### 4. Month-over-Month (MoM) Growth Calculation
```tableau
(ZN(SUM([Revenue])) - LOOKUP(ZN(SUM([Revenue])), -1)) / ABS(LOOKUP(ZN(SUM([Revenue])), -1))
```
*Compute using: Table (Across)*

### 5. Return Rate Anomaly Flag (Color Encoding)
```tableau
IF [Return Rate (%)] >= 0.0110 THEN "High Risk Anomaly"
ELSEIF [Return Rate (%)] >= 0.0100 THEN "Moderate Risk"
ELSE "Healthy (<1.00%)"
END
```

### 6. Portland 1,000+ Milestone Highlighter
```tableau
IF [Store City] = "Portland" AND [December Txns] >= 1000 THEN "Target Met (1,000+)"
ELSE "Standard"
END
```

---

## 📊 Tableau Worksheet Layout & Design

| Sheet Name | Visual Type | Shelves & Marks Configuration |
| :--- | :--- | :--- |
| **1. Executive KPI Strip** | BAN (Big Numbers) | Text Marks: `SUM([Transactions])`, `SUM([Profit])`, `[Return Rate (%)]` with MoM indicators. |
| **2. Brand Profitability Matrix** | Highlight Table / Bar in Table | Rows: `[Product Brand]`, Columns: `Measure Names`. Colors: `[Profit Margin]` (Green Gradient) and `[Return Rate]` (Red alert). |
| **3. Geographic Symbol Map** | Map | Longitude / Latitude with Marks: Circle. Size: `SUM([Transactions])`, Color: `[Store Country]`. |
| **4. 52-Week Revenue Area Chart** | Line / Area Chart | Columns: `WEEK([Date])`, Rows: `SUM([Revenue])`. Analytics Pane &rarr; Add Linear Trend Line (OLS). |
| **5. Revenue vs Target Bullet Chart** | Bullet Graph | Columns: `SUM([Current Profit])`, Reference Line: `SUM([Target Profit])` (Band at 60%, 80%, 100%). |

---

## 🚀 How to Publish to Tableau Public
1. Open Tableau Desktop &rarr; File &rarr; Open & build worksheets using `data/`.
2. Assemble onto a Dashboard Canvas (1366 x 768 px).
3. Add Country Parameter / Filter Actions.
4. Click **Server** &rarr; **Tableau Public** &rarr; **Save to Tableau Public As...**
5. Paste your Tableau Public URL into `README.md` and `index.html`!
