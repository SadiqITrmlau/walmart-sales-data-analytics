<div align="center">

  # 🛒 Walmart Market End-to-End Data Analytics Platform
  ### Cross-Border Retail Business Intelligence (USA • Mexico • Canada)

  <!-- Dynamic Typing Animation Banner -->
  <a href="https://github.com/">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&pause=1200&color=0071CE&center=true&vCenter=true&width=720&lines=Walmart+Market+Enterprise+Analytics+Suite;Python+%7C+SQL+%7C+Power+BI+%7C+Excel+%7C+Tableau;Statistical+OLS+Regression+(R2+%3D+0.7302);Architected+and+Developed+by+Sadiq+Khan" alt="Typing SVG" />
  </a>

  <br/><br/>

  <!-- Status & Quick Links Badges -->
  [![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit%20Cloud-0071CE?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/)
  [![GitHub Pages](https://img.shields.io/badge/Web%20Portfolio-GitHub%20Pages-041E42?style=for-the-badge&logo=github&logoColor=white)](https://YOUR_GITHUB_USERNAME.github.io/walmart-data-analytics/)
  [![Author](https://img.shields.io/badge/Author-Sadiq%20Khan-0071CE?style=for-the-badge&logo=linkedin&logoColor=white)](https://github.com/)
  [![License](https://img.shields.io/badge/License-MIT-041E42?style=for-the-badge)](LICENSE)

  <br/>

  <!-- Tech Stack Badges -->
  [![Python](https://img.shields.io/badge/Python-3.13-0071CE?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![SQL](https://img.shields.io/badge/SQL-SQLite%20Star%20Schema-041E42?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
  [![Power BI](https://img.shields.io/badge/Power_BI-Desktop-0071CE?style=flat-square&logo=powerbi&logoColor=white)](https://powerbi.microsoft.com/)
  [![Excel](https://img.shields.io/badge/Excel-Financial_Model-041E42?style=flat-square&logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/excel)
  [![Tableau](https://img.shields.io/badge/Tableau-Public%20%2F%20Desktop-0071CE?style=flat-square&logo=tableau&logoColor=white)](https://public.tableau.com/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-041E42?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS%20CDN-0071CE?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

</div>

---

## 📌 Table of Contents
- [🎯 Executive Overview & KPIs](#-executive-overview--kpis)
- [🏗️ End-to-End Pipeline Architecture](#️-end-to-end-pipeline-architecture)
- [🗄️ Relational Data Model (Star Schema)](#️-relational-data-model-star-schema)
- [🛠️ Tool-by-Tool Technical Deep Dive](#️-tool-by-tool-technical-deep-dive)
  - [1. Python Data Science & OLS Regression](#1-python-data-science--ols-regression)
  - [2. SQL Analytics Studio (Window Functions & CTEs)](#2-sql-analytics-studio-window-functions--ctes)
  - [3. Power BI Desktop & DAX Architecture](#3-power-bi-desktop--dax-architecture)
  - [4. Excel Executive Financial Model](#4-excel-executive-financial-model)
  - [5. Tableau LOD Calculations & Architecture](#5-tableau-lod-calculations--architecture)
  - [6. Dual Live Web Deployments](#6-dual-live-web-deployments)
- [💡 Strategic Business Takeaways](#-strategic-business-takeaways)
- [🚀 Quickstart & How to Run](#-quickstart--how-to-run)
- [📂 Repository Structure](#-repository-structure)
- [👤 Author & Acknowledgments](#-author--acknowledgments)

---

## 🎯 Executive Overview & KPIs

This platform provides an enterprise data analytics and business intelligence solution analyzing Walmart's cross-border retail performance across **Canada, Mexico, and the United States (1998)**. 

The dataset captures **113,668 transactions**, **$449,627 in net revenue**, and **25 product brands** across 13 major commercial hubs.

### 📊 Topline Executive Scorecard (FY 1998)

| Key Metric | Actual Performance | Target Benchmark | Variance (%) | Strategic Status |
| :--- | :---: | :---: | :---: | :---: |
| **Current Month Transactions** | **18,325** | 17,339 | `+5.69%` | 🟢 Target Exceeded |
| **Current Month Net Profit** | **$71,682** | $67,872 | `+5.61%` | 🟢 Profit Expansion |
| **Current Month Returns** | **496** | 482 | `-2.90%` | 🟢 Favorable (Low Returns) |
| **Total Net Revenue** | **$449,627** | $430,000 | `+4.56%` | 🟢 High Revenue Acceleration |
| **Average Gross Profit Margin** | **59.94%** | 58.00% | `+194 bps` | 📈 Premium Margin Retention |
| **Portfolio Return Rate** | **1.00%** | < 1.10% | `-10 bps` | 🛡️ Healthy Portfolio Risk |

---

## 🏗️ End-to-End Pipeline Architecture

```mermaid
flowchart TD
    subgraph S1["1. Data Sourcing & Ingestion"]
        A["Relational Flat CSVs<br/>(Transactions, Brands, Stores, Regions)"]
    end

    subgraph S2["2. Relational Modeling & Analytics"]
        B["SQLite Database Engine<br/>(walmart_analytics.db)"]
        C["Advanced SQL Window Functions & CTEs<br/>(LAG, LEAD, DENSE_RANK, CASE Anomaly Flags)"]
    end

    subgraph S3["3. Statistical Machine Learning & EDA"]
        D["Python SciPy & Statsmodels Suite<br/>(OLS Regression: R² = 0.7302, p < 0.001)"]
    end

    subgraph S4["4. Business Intelligence & Financial Modeling"]
        E["Power BI Desktop (Star Schema & DAX)"]
        F["Excel Financial Model (Dynamic BANs & Formulas)"]
        G["Tableau Architecture (LOD Expressions)"]
    end

    subgraph S5["5. Production Interactive Deployments"]
        H["Streamlit Cloud App (Interactive Python/Plotly)"]
        I["GitHub Pages Web Hub (Tailwind 2-Color UI)"]
    end

    A --> B
    B --> C
    B --> D
    C --> E
    C --> F
    C --> G
    D --> H
    B --> H
    E --> I
    F --> I
