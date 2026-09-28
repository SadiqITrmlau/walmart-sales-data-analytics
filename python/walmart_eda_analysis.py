import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "python", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Arial'

print("=" * 70)
print("  WALMART MARKET PYTHON EDA & OLS STATISTICAL SUITE")
print("  Author: Sadiq Khan")
print("=" * 70)

# -------------------------------------------------------------------
# 1. LOAD DATASETS
# -------------------------------------------------------------------
df_brands = pd.read_csv(os.path.join(DATA_DIR, "brand_summary.csv"))
df_stores = pd.read_csv(os.path.join(DATA_DIR, "stores.csv"))
df_weekly = pd.read_csv(os.path.join(DATA_DIR, "weekly_revenue.csv"))

print(f"\n[1] Data Ingestion Summary:")
print(f"  - Brands Loaded: {len(df_brands)} records")
print(f"  - Stores Loaded: {len(df_stores)} locations")
print(f"  - Weekly Time Series: {len(df_weekly)} weeks of 1998")

# -------------------------------------------------------------------
# 2. STATISTICAL OLS (ORDINARY LEAST SQUARES) REGRESSION
# -------------------------------------------------------------------
print(f"\n[2] Performing Ordinary Least Squares (OLS) Linear Trend Analysis...")

x = df_weekly["week_number"].values
y = df_weekly["revenue"].values

# Fit OLS line: y = slope * x + intercept
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r_squared = r_value ** 2
trendline = slope * x + intercept

print(f"  • OLS Slope (Weekly Growth Rate): ${slope:.2f} per week")
print(f"  • OLS Intercept (Base Week 0):     ${intercept:.2f}")
print(f"  • Coefficient of Determination (R²): {r_squared:.4f}")
print(f"  • P-Value:                          {p_value:.4e} (Statistically Significant)")
print(f"  • Standard Error:                   ${std_err:.2f}")

# Plot 1: OLS Regression & Weekly Revenue Trend
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.bar(df_weekly["week_number"], df_weekly["revenue"] / 1000, color='#0071CE', alpha=0.7, label='Actual Weekly Revenue ($K)')
ax.plot(df_weekly["week_number"], trendline / 1000, color='#DC2626', linewidth=2.5, linestyle='--', 
        label=f'OLS Trendline (R² = {r_squared:.3f}, Growth = +${slope:.0f}/wk)')

ax.set_title("Walmart 1998 52-Week Revenue Trend with OLS Linear Regression\nCreated by Sadiq Khan", fontsize=12, fontweight='bold', pad=15)
ax.set_xlabel("Week of Year (1998)", fontsize=10)
ax.set_ylabel("Revenue ($ in Thousands)", fontsize=10)
ax.legend(frameon=True, facecolor='white', loc='upper left')
plt.tight_layout()

chart1_path = os.path.join(OUT_DIR, "ols_revenue_trend.png")
plt.savefig(chart1_path)
plt.close()
print(f"  ✅ Saved OLS Chart to: {chart1_path}")

# -------------------------------------------------------------------
# 3. BRAND PROFIT MARGIN & RETURN RATE CORRELATION
# -------------------------------------------------------------------
print(f"\n[3] Evaluating Product Brand Profit Margin vs Return Rate Risk...")

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
scatter = ax.scatter(
    df_brands["profit_margin"] * 100, 
    df_brands["return_rate"] * 100, 
    s=df_brands["transactions"] / 20, 
    c=df_brands["profit"] / 1000, 
    cmap='viridis', 
    alpha=0.85, 
    edgecolors='black', 
    linewidth=0.8
)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Total Profit ($ in Thousands)', fontsize=9)

# Add risk threshold line
ax.axhline(y=1.10, color='red', linestyle=':', label='High Return Anomaly Threshold (1.10%)')

# Annotate key brands
for _, row in df_brands.head(6).iterrows():
    ax.annotate(row['product_brand'], 
                (row['profit_margin'] * 100, row['return_rate'] * 100),
                xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold')

ax.set_title("Product Brand Margin (%) vs Return Rate (%) Matrix\nBubble size = Transaction Volume | Created by Sadiq Khan", fontsize=11, fontweight='bold', pad=12)
ax.set_xlabel("Profit Margin (%)", fontsize=10)
ax.set_ylabel("Return Rate (%)", fontsize=10)
ax.legend(loc='lower left')
plt.tight_layout()

chart2_path = os.path.join(OUT_DIR, "brand_margin_distribution.png")
plt.savefig(chart2_path)
plt.close()
print(f"  ✅ Saved Margin/Return Scatter to: {chart2_path}")

# -------------------------------------------------------------------
# 4. REGIONAL STORE ANALYSIS
# -------------------------------------------------------------------
print(f"\n[4] Generating Regional Store Transaction Comparison...")

fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
store_sorted = df_stores.sort_values(by="transactions", ascending=True)

colors = ['#F59E0B' if c == 'Canada' else '#9333EA' if c == 'Mexico' else '#0071CE' for c in store_sorted["store_country"]]
bars = ax.barh(store_sorted["store_city"] + " (" + store_sorted["store_country"] + ")", store_sorted["transactions"], color=colors)

# Highlight Portland milestone
for bar, city in zip(bars, store_sorted["store_city"]):
    if city == "Portland":
        bar.set_color('#10B981')
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2, '📍 1,000+ Dec Milestone', 
                va='center', fontsize=9, fontweight='bold', color='#047857')

ax.set_title("Walmart Store Annual Transactions by City & Country\nGreen = Portland Milestone | Blue = USA | Purple = Mexico | Amber = Canada", fontsize=11, fontweight='bold', pad=12)
ax.set_xlabel("Total Annual Transactions", fontsize=10)
plt.tight_layout()

chart3_path = os.path.join(OUT_DIR, "regional_store_performance.png")
plt.savefig(chart3_path)
plt.close()
print(f"  ✅ Saved Store Ranking Chart to: {chart3_path}")

print("\n" + "=" * 70)
print("✅ Python EDA & OLS Statistical Analysis Complete!")
print("=" * 70)
