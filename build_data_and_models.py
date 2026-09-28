import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Set working directory to project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)

print("🚀 1. Generating relational data tables...")

# ----------------------------------------------------
# 1. PRODUCTS TABLE & BRAND SUMMARY
# ----------------------------------------------------
brands_data = [
    {"brand_id": 1, "product_brand": "Hermanos", "category": "Produce & Grocery", "price_tier": "Medium", "transactions": 5341, "profit": 21753, "revenue": 37100, "profit_margin": 0.5864, "return_rate": 0.0095, "returns_count": 51},
    {"brand_id": 2, "product_brand": "Ebony", "category": "Pantry & Spices", "price_tier": "High", "transactions": 5238, "profit": 20354, "revenue": 34030, "profit_margin": 0.5981, "return_rate": 0.0096, "returns_count": 50},
    {"brand_id": 3, "product_brand": "Tell Tale", "category": "Beverages", "price_tier": "Low", "transactions": 5132, "profit": 19982, "revenue": 34420, "profit_margin": 0.5805, "return_rate": 0.0099, "returns_count": 51},
    {"brand_id": 4, "product_brand": "Tri-State", "category": "Dairy & Eggs", "price_tier": "Medium", "transactions": 5000, "profit": 19980, "revenue": 33915, "profit_margin": 0.5891, "return_rate": 0.0110, "returns_count": 55},
    {"brand_id": 5, "product_brand": "High Top", "category": "Bakery & Snacks", "price_tier": "High", "transactions": 4840, "profit": 19810, "revenue": 32785, "profit_margin": 0.6042, "return_rate": 0.0101, "returns_count": 49},
    {"brand_id": 6, "product_brand": "Nationeel", "category": "Frozen Foods", "price_tier": "Medium", "transactions": 4408, "profit": 18617, "revenue": 30800, "profit_margin": 0.6044, "return_rate": 0.0118, "returns_count": 52},
    {"brand_id": 7, "product_brand": "Best Choice", "category": "Household Essentials", "price_tier": "Low", "transactions": 4218, "profit": 18355, "revenue": 30270, "profit_margin": 0.6064, "return_rate": 0.0081, "returns_count": 34},
    {"brand_id": 8, "product_brand": "Horatio", "category": "Personal Care", "price_tier": "High", "transactions": 4195, "profit": 17737, "revenue": 30360, "profit_margin": 0.5842, "return_rate": 0.0125, "returns_count": 52},
    {"brand_id": 9, "product_brand": "Fort West", "category": "Meat & Seafood", "price_tier": "High", "transactions": 4108, "profit": 15834, "revenue": 26478, "profit_margin": 0.5980, "return_rate": 0.0097, "returns_count": 40},
    {"brand_id": 10, "product_brand": "Fast", "category": "Snacks & Confectionery", "price_tier": "Low", "transactions": 4097, "profit": 16469, "revenue": 26985, "profit_margin": 0.6103, "return_rate": 0.0107, "returns_count": 44},
    {"brand_id": 11, "product_brand": "Sunset", "category": "Produce & Fresh", "price_tier": "Medium", "transactions": 3953, "profit": 14018, "revenue": 23190, "profit_margin": 0.6045, "return_rate": 0.0103, "returns_count": 41},
    {"brand_id": 12, "product_brand": "Carrington", "category": "Pantry Staples", "price_tier": "Medium", "transactions": 3891, "profit": 14883, "revenue": 25005, "profit_margin": 0.5952, "return_rate": 0.0078, "returns_count": 30},
    {"brand_id": 13, "product_brand": "Red Wing", "category": "Beverages", "price_tier": "High", "transactions": 3870, "profit": 15870, "revenue": 26735, "profit_margin": 0.5936, "return_rate": 0.0106, "returns_count": 41},
    {"brand_id": 14, "product_brand": "Big Time", "category": "Snacks", "price_tier": "Medium", "transactions": 3816, "profit": 15560, "revenue": 25845, "profit_margin": 0.6020, "return_rate": 0.0105, "returns_count": 40},
    {"brand_id": 15, "product_brand": "Cormorant", "category": "Canned Goods", "price_tier": "Low", "transactions": 3744, "profit": 15749, "revenue": 25565, "profit_margin": 0.6160, "return_rate": 0.0087, "returns_count": 33},
    {"brand_id": 16, "product_brand": "Imagine", "category": "Organic", "price_tier": "High", "transactions": 3634, "profit": 15102, "revenue": 24595, "profit_margin": 0.6140, "return_rate": 0.0106, "returns_count": 39},
    {"brand_id": 17, "product_brand": "Super", "category": "Household", "price_tier": "Low", "transactions": 3618, "profit": 13868, "revenue": 22888, "profit_margin": 0.6059, "return_rate": 0.0096, "returns_count": 35},
    {"brand_id": 18, "product_brand": "Denny", "category": "Dairy", "price_tier": "Medium", "transactions": 3584, "profit": 16015, "revenue": 27602, "profit_margin": 0.5802, "return_rate": 0.0099, "returns_count": 35},
    {"brand_id": 19, "product_brand": "High Quality", "category": "Meat & Poultry", "price_tier": "High", "transactions": 3577, "profit": 16139, "revenue": 28325, "profit_margin": 0.5698, "return_rate": 0.0115, "returns_count": 41},
    {"brand_id": 20, "product_brand": "Golden", "category": "Bakery", "price_tier": "Low", "transactions": 3550, "profit": 13256, "revenue": 22575, "profit_margin": 0.5872, "return_rate": 0.0088, "returns_count": 31},
    {"brand_id": 21, "product_brand": "BBB Best", "category": "Pantry", "price_tier": "Medium", "transactions": 3514, "profit": 12991, "revenue": 20912, "profit_margin": 0.6212, "return_rate": 0.0080, "returns_count": 28},
    {"brand_id": 22, "product_brand": "PigTail", "category": "Sweets", "price_tier": "Low", "transactions": 3467, "profit": 11617, "revenue": 19145, "profit_margin": 0.6068, "return_rate": 0.0104, "returns_count": 36},
    {"brand_id": 23, "product_brand": "Plato", "category": "Pet Supplies", "price_tier": "High", "transactions": 3352, "profit": 12748, "revenue": 20060, "profit_margin": 0.6355, "return_rate": 0.0106, "returns_count": 36},
    {"brand_id": 24, "product_brand": "Landslide", "category": "Paper Goods", "price_tier": "Low", "transactions": 3270, "profit": 10647, "revenue": 18155, "profit_margin": 0.5865, "return_rate": 0.0098, "returns_count": 32},
    {"brand_id": 25, "product_brand": "CDR", "category": "Health & First Aid", "price_tier": "Medium", "transactions": 3078, "profit": 12062, "revenue": 20450, "profit_margin": 0.5898, "return_rate": 0.0111, "returns_count": 34}
]

df_brands = pd.DataFrame(brands_data)
df_brands.to_csv(os.path.join(DATA_DIR, "brand_summary.csv"), index=False)

# ----------------------------------------------------
# 2. STORES & REGIONS TABLE
# ----------------------------------------------------
stores_data = [
    {"store_id": 101, "store_name": "Walmart Portland Supercenter", "store_city": "Portland", "store_state": "OR", "store_country": "USA", "region_id": 1, "grocery_sqft": 45000, "first_opened": "1992-05-12", "transactions": 1050, "december_txns": 1050},
    {"store_id": 102, "store_name": "Walmart Seattle Metro", "store_city": "Seattle", "store_state": "WA", "store_country": "USA", "region_id": 1, "grocery_sqft": 42000, "first_opened": "1994-08-15", "transactions": 940, "december_txns": 820},
    {"store_id": 103, "store_name": "Walmart Los Angeles Central", "store_city": "Los Angeles", "store_state": "CA", "store_country": "USA", "region_id": 2, "grocery_sqft": 52000, "first_opened": "1990-11-20", "transactions": 1250, "december_txns": 1180},
    {"store_id": 104, "store_name": "Walmart San Francisco Bay", "store_city": "San Francisco", "store_state": "CA", "store_country": "USA", "region_id": 2, "grocery_sqft": 48000, "first_opened": "1991-03-10", "transactions": 880, "december_txns": 790},
    {"store_id": 105, "store_name": "Walmart Dallas Mega Hub", "store_city": "Dallas", "store_state": "TX", "store_country": "USA", "region_id": 3, "grocery_sqft": 55000, "first_opened": "1989-07-04", "transactions": 1100, "december_txns": 980},
    {"store_id": 106, "store_name": "Walmart Chicago North", "store_city": "Chicago", "store_state": "IL", "store_country": "USA", "region_id": 4, "grocery_sqft": 49000, "first_opened": "1993-09-18", "transactions": 990, "december_txns": 890},
    {"store_id": 107, "store_name": "Walmart New York Midtown", "store_city": "New York", "store_state": "NY", "store_country": "USA", "region_id": 5, "grocery_sqft": 50000, "first_opened": "1995-02-28", "transactions": 1320, "december_txns": 1240},
    {"store_id": 201, "store_name": "Walmart Mexico City Centro", "store_city": "Mexico City", "store_state": "CDMX", "store_country": "Mexico", "region_id": 6, "grocery_sqft": 54000, "first_opened": "1994-10-01", "transactions": 1450, "december_txns": 1390},
    {"store_id": 202, "store_name": "Walmart Guadalajara Hub", "store_city": "Guadalajara", "store_state": "JAL", "store_country": "Mexico", "region_id": 6, "grocery_sqft": 46000, "first_opened": "1996-04-14", "transactions": 890, "december_txns": 820},
    {"store_id": 203, "store_name": "Walmart Monterrey North", "store_city": "Monterrey", "store_state": "NL", "store_country": "Mexico", "region_id": 6, "grocery_sqft": 47000, "first_opened": "1995-06-22", "transactions": 920, "december_txns": 850},
    {"store_id": 301, "store_name": "Walmart Toronto Downtown", "store_city": "Toronto", "store_state": "ON", "store_country": "Canada", "region_id": 7, "grocery_sqft": 43000, "first_opened": "1994-01-19", "transactions": 670, "december_txns": 610},
    {"store_id": 302, "store_name": "Walmart Vancouver West", "store_city": "Vancouver", "store_state": "BC", "store_country": "Canada", "region_id": 7, "grocery_sqft": 41000, "first_opened": "1996-11-05", "transactions": 540, "december_txns": 490},
    {"store_id": 303, "store_name": "Walmart Montreal East", "store_city": "Montreal", "store_state": "QC", "store_country": "Canada", "region_id": 7, "grocery_sqft": 39000, "first_opened": "1997-03-12", "transactions": 480, "december_txns": 430}
]
df_stores = pd.DataFrame(stores_data)
df_stores.to_csv(os.path.join(DATA_DIR, "stores.csv"), index=False)

regions_data = [
    {"region_id": 1, "sales_district": "Pacific Northwest", "sales_region": "West USA", "country": "USA"},
    {"region_id": 2, "sales_district": "California", "sales_region": "West USA", "country": "USA"},
    {"region_id": 3, "sales_district": "South Central", "sales_region": "South USA", "country": "USA"},
    {"region_id": 4, "sales_district": "Midwest Metro", "sales_region": "Midwest USA", "country": "USA"},
    {"region_id": 5, "sales_district": "Northeast Corridor", "sales_region": "East USA", "country": "USA"},
    {"region_id": 6, "sales_district": "Mexico Central & North", "sales_region": "Mexico", "country": "Mexico"},
    {"region_id": 7, "sales_district": "Canada East & West", "sales_region": "Canada", "country": "Canada"}
]
df_regions = pd.DataFrame(regions_data)
df_regions.to_csv(os.path.join(DATA_DIR, "regions.csv"), index=False)

# ----------------------------------------------------
# 3. 52-WEEK REVENUE TIME SERIES (1998)
# ----------------------------------------------------
weeks = list(range(1, 53))
base_rev = [
    18.2, 19.1, 21.0, 20.4, 24.1, 26.3, 25.0, 23.4, 22.8, 28.1, 27.5, 26.2,
    25.1, 24.8, 27.3, 29.1, 30.2, 28.4, 27.1, 26.5, 28.3, 31.2, 32.1, 29.5,
    28.4, 27.2, 29.3, 31.1, 30.4, 28.2, 27.5, 29.1, 30.5, 32.4, 31.2, 29.0,
    28.1, 29.6, 32.3, 34.1, 33.2, 31.5, 32.8, 35.2, 36.4, 34.8, 37.1, 39.5,
    42.3, 45.1, 48.6, 52.4
]

weekly_data = []
for w, r in zip(weeks, base_rev):
    month = (w - 1) // 4 + 1
    month = min(month, 12)
    rev_usd = round(r * 1000, 2)
    profit_usd = round(rev_usd * 0.5994, 2)
    txns = int(round(rev_usd / 3.95))
    returns = int(round(txns * 0.01))
    weekly_data.append({
        "week_number": w,
        "month": month,
        "year": 1998,
        "revenue": rev_usd,
        "profit": profit_usd,
        "transactions": txns,
        "returns": returns
    })

df_weekly = pd.DataFrame(weekly_data)
df_weekly.to_csv(os.path.join(DATA_DIR, "weekly_revenue.csv"), index=False)

print("✅ Data tables generated successfully!")

# ----------------------------------------------------
# 4. SQLITE DATABASE CREATION (walmart_analytics.db)
# ----------------------------------------------------
print("🗄️ 2. Building SQLite Database (walmart_analytics.db)...")
db_path = os.path.join(BASE_DIR, "walmart_analytics.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Tables
cursor.execute("DROP TABLE IF EXISTS brands;")
cursor.execute("DROP TABLE IF EXISTS stores;")
cursor.execute("DROP TABLE IF EXISTS regions;")
cursor.execute("DROP TABLE IF EXISTS weekly_revenue;")

cursor.execute("""
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    sales_district TEXT NOT NULL,
    sales_region TEXT NOT NULL,
    country TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL,
    store_city TEXT NOT NULL,
    store_state TEXT NOT NULL,
    store_country TEXT NOT NULL,
    region_id INTEGER,
    grocery_sqft INTEGER,
    first_opened DATE,
    transactions INTEGER,
    december_txns INTEGER,
    FOREIGN KEY(region_id) REFERENCES regions(region_id)
);
""")

cursor.execute("""
CREATE TABLE brands (
    brand_id INTEGER PRIMARY KEY,
    product_brand TEXT NOT NULL,
    category TEXT NOT NULL,
    price_tier TEXT NOT NULL,
    transactions INTEGER,
    profit REAL,
    revenue REAL,
    profit_margin REAL,
    return_rate REAL,
    returns_count INTEGER
);
""")

cursor.execute("""
CREATE TABLE weekly_revenue (
    week_number INTEGER PRIMARY KEY,
    month INTEGER,
    year INTEGER,
    revenue REAL,
    profit REAL,
    transactions INTEGER,
    returns INTEGER
);
""")

# Insert Data
df_regions.to_sql("regions", conn, if_exists="append", index=False)
df_stores.to_sql("stores", conn, if_exists="append", index=False)
df_brands.to_sql("brands", conn, if_exists="append", index=False)
df_weekly.to_sql("weekly_revenue", conn, if_exists="append", index=False)

conn.commit()
conn.close()
print("✅ SQLite database created at:", db_path)

# ----------------------------------------------------
# 5. EXCEL FINANCIAL MODEL (walmart_executive_model.xlsx)
# ----------------------------------------------------
print("📑 3. Building Professional Multi-Sheet Excel Model...")
wb = openpyxl.Workbook()

# Setup Styles
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
title_font = Font(name="Calibri", size=16, bold=True, color="041E42")
subtitle_font = Font(name="Calibri", size=10, italic=True, color="555555")
kpi_num_font = Font(name="Calibri", size=18, bold=True, color="0071CE")
bold_font = Font(name="Calibri", size=11, bold=True)
regular_font = Font(name="Calibri", size=11)

walmart_blue_fill = PatternFill(start_color="0071CE", end_color="0071CE", fill_type="solid")
header_fill = PatternFill(start_color="041E42", end_color="041E42", fill_type="solid")
light_blue_fill = PatternFill(start_color="E6F1FC", end_color="E6F1FC", fill_type="solid")
accent_yellow_fill = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
green_fill = PatternFill(start_color="D1E7DD", end_color="D1E7DD", fill_type="solid")
rose_fill = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

# ----------------------------------------
# Sheet 1: Executive Dashboard
# ----------------------------------------
ws_exec = wb.active
ws_exec.title = "Executive Summary"
ws_exec.views.sheetView[0].showGridLines = True

ws_exec["A1"] = "WALMART MARKET EXECUTIVE BI DASHBOARD (1998)"
ws_exec["A1"].font = title_font
ws_exec["A2"] = "Created by Sadiq Khan | Business Intelligence & Analytics Portfolio"
ws_exec["A2"].font = subtitle_font

# KPI 1: Transactions
ws_exec["A4"] = "Current Month Txns"
ws_exec["A4"].font = bold_font
ws_exec["A4"].fill = light_blue_fill
ws_exec["A5"] = 18325
ws_exec["A5"].font = kpi_num_font
ws_exec["A5"].number_format = "#,##0"
ws_exec["A6"] = "Target: 17,339 (+5.69%)"
ws_exec["A6"].font = subtitle_font

# KPI 2: Profit
ws_exec["C4"] = "Current Month Profit"
ws_exec["C4"].font = bold_font
ws_exec["C4"].fill = light_blue_fill
ws_exec["C5"] = 71682
ws_exec["C5"].font = kpi_num_font
ws_exec["C5"].number_format = "$#,##0"
ws_exec["C6"] = "Target: $67,872 (+5.61%)"
ws_exec["C6"].font = subtitle_font

# KPI 3: Returns
ws_exec["E4"] = "Current Month Returns"
ws_exec["E4"].font = bold_font
ws_exec["E4"].fill = light_blue_fill
ws_exec["E5"] = 496
ws_exec["E5"].font = Font(name="Calibri", size=18, bold=True, color="DC3545")
ws_exec["E5"].number_format = "#,##0"
ws_exec["E6"] = "Target: 482 (-2.9% Alert)"
ws_exec["E6"].font = subtitle_font

# KPI 4: Total Revenue
ws_exec["G4"] = "Total Annual Revenue"
ws_exec["G4"].font = bold_font
ws_exec["G4"].fill = light_blue_fill
ws_exec["G5"] = 449627
ws_exec["G5"].font = kpi_num_font
ws_exec["G5"].number_format = "$#,##0"
ws_exec["G6"] = "Avg Margin: 59.94%"
ws_exec["G6"].font = subtitle_font

# Executive Notes
ws_exec["A8"] = "Key Strategic Takeaways"
ws_exec["A8"].font = Font(name="Calibri", size=13, bold=True, color="041E42")

takeaways = [
    ("1. Portland December Milestone", "Portland store recorded 1,050 transactions in December, achieving the 1,000+ benchmark."),
    ("2. Top 10 Product Brands Driver", "Top 10 brands contribute ~25% of gross revenue with high profit margins (>58%)."),
    ("3. Return Rate Anomaly (+2.9%)", "Total returns rose to 496. Products Horatio (1.25%) and Nationeel (1.18%) require quality audits."),
    ("4. Mexico Market Acceleration", "Mexico recorded 72.81K annual transactions with expanding profit velocity.")
]

for idx, (title, desc) in enumerate(takeaways, start=9):
    ws_exec[f"A{idx}"] = title
    ws_exec[f"A{idx}"].font = bold_font
    ws_exec[f"B{idx}"] = desc
    ws_exec[f"B{idx}"].font = regular_font

# ----------------------------------------
# Sheet 2: Brand Performance Matrix
# ----------------------------------------
ws_brands = wb.create_sheet(title="Brand Performance")
ws_brands.views.sheetView[0].showGridLines = True

headers_b = ["Brand ID", "Product Brand", "Category", "Price Tier", "Transactions", "Revenue ($)", "Profit ($)", "Profit Margin", "Return Rate", "Returns Count"]
ws_brands.append(headers_b)

for col_num in range(1, len(headers_b) + 1):
    cell = ws_brands.cell(row=1, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center" if col_num in [1, 4] else "left" if col_num in [2, 3] else "right")

for row_idx, brand in enumerate(brands_data, start=2):
    ws_brands.cell(row=row_idx, column=1, value=brand["brand_id"]).alignment = Alignment(horizontal="center")
    ws_brands.cell(row=row_idx, column=2, value=brand["product_brand"])
    ws_brands.cell(row=row_idx, column=3, value=brand["category"])
    ws_brands.cell(row=row_idx, column=4, value=brand["price_tier"]).alignment = Alignment(horizontal="center")
    
    # Numbers & Formulas
    c_txns = ws_brands.cell(row=row_idx, column=5, value=brand["transactions"])
    c_txns.number_format = "#,##0"
    
    c_rev = ws_brands.cell(row=row_idx, column=6, value=brand["revenue"])
    c_rev.number_format = "$#,##0"
    
    c_prof = ws_brands.cell(row=row_idx, column=7, value=brand["profit"])
    c_prof.number_format = "$#,##0"
    
    # Excel Formula for Margin: =Profit / Revenue
    c_margin = ws_brands.cell(row=row_idx, column=8, value=f"=G{row_idx}/F{row_idx}")
    c_margin.number_format = "0.00%"
    if brand["profit_margin"] >= 0.60:
        c_margin.fill = green_fill
        
    # Excel Formula for Return Rate: =Returns / Transactions
    c_ret = ws_brands.cell(row=row_idx, column=9, value=f"=J{row_idx}/E{row_idx}")
    c_ret.number_format = "0.00%"
    if brand["return_rate"] >= 0.0110:
        c_ret.fill = rose_fill
        
    c_ret_cnt = ws_brands.cell(row=row_idx, column=10, value=brand["returns_count"])
    c_ret_cnt.number_format = "#,##0"

# Total Row
tot_row = len(brands_data) + 2
ws_brands.cell(row=tot_row, column=2, value="Total / Average").font = bold_font
ws_brands.cell(row=tot_row, column=5, value=f"=SUM(E2:E{tot_row-1})").font = bold_font
ws_brands.cell(row=tot_row, column=5).number_format = "#,##0"

ws_brands.cell(row=tot_row, column=6, value=f"=SUM(F2:F{tot_row-1})").font = bold_font
ws_brands.cell(row=tot_row, column=6).number_format = "$#,##0"

ws_brands.cell(row=tot_row, column=7, value=f"=SUM(G2:G{tot_row-1})").font = bold_font
ws_brands.cell(row=tot_row, column=7).number_format = "$#,##0"

ws_brands.cell(row=tot_row, column=8, value=f"=G{tot_row}/F{tot_row}").font = bold_font
ws_brands.cell(row=tot_row, column=8).number_format = "0.00%"

ws_brands.cell(row=tot_row, column=9, value=f"=J{tot_row}/E{tot_row}").font = bold_font
ws_brands.cell(row=tot_row, column=9).number_format = "0.00%"

ws_brands.cell(row=tot_row, column=10, value=f"=SUM(J2:J{tot_row-1})").font = bold_font
ws_brands.cell(row=tot_row, column=10).number_format = "#,##0"

# ----------------------------------------
# Sheet 3: Weekly Revenue Model (52 Weeks)
# ----------------------------------------
ws_week = wb.create_sheet(title="Weekly Financials")
ws_week.views.sheetView[0].showGridLines = True

headers_w = ["Week #", "Month", "Year", "Gross Revenue ($)", "Gross Profit ($)", "Transactions", "Returns", "Cumulative Revenue ($)"]
ws_week.append(headers_w)

for col_num in range(1, len(headers_w) + 1):
    cell = ws_week.cell(row=1, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center" if col_num in [1, 2, 3] else "right")

for row_idx, item in enumerate(weekly_data, start=2):
    ws_week.cell(row=row_idx, column=1, value=item["week_number"]).alignment = Alignment(horizontal="center")
    ws_week.cell(row=row_idx, column=2, value=item["month"]).alignment = Alignment(horizontal="center")
    ws_week.cell(row=row_idx, column=3, value=item["year"]).alignment = Alignment(horizontal="center")
    
    c_r = ws_week.cell(row=row_idx, column=4, value=item["revenue"])
    c_r.number_format = "$#,##0"
    
    c_p = ws_week.cell(row=row_idx, column=5, value=item["profit"])
    c_p.number_format = "$#,##0"
    
    c_t = ws_week.cell(row=row_idx, column=6, value=item["transactions"])
    c_t.number_format = "#,##0"
    
    c_ret = ws_week.cell(row=row_idx, column=7, value=item["returns"])
    c_ret.number_format = "#,##0"
    
    c_cum = ws_week.cell(row=row_idx, column=8, value=f"=SUM($D$2:D{row_idx})")
    c_cum.number_format = "$#,##0"

# Auto-adjust column widths
for ws in [ws_exec, ws_brands, ws_week]:
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

excel_path = os.path.join(EXCEL_DIR, "walmart_executive_model.xlsx")
wb.save(excel_path)
print("✅ Excel financial model saved at:", excel_path)
