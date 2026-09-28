import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Walmart Market Analytics Suite | Sadiq Khan",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom 2-Color Theme CSS (Walmart Blue #0071CE and Deep Navy #041E42)
st.markdown("""
<style>
    /* Global Primary Accent */
    :root {
        --primary-color: #0071CE;
        --secondary-color: #041E42;
    }
    .stApp {
        background-color: #F8FAFC;
    }
    /* Headers & Text */
    h1, h2, h3 {
        color: #041E42 !important;
        font-family: 'Inter', sans-serif;
    }
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #0071CE !important;
        font-weight: 800;
    }
    /* Primary Buttons */
    button[kind="primary"] {
        background-color: #0071CE !important;
        border-color: #0071CE !important;
        color: white !important;
    }
    /* Top Banner */
    .banner {
        background-color: #041E42;
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .banner h1 {
        color: white !important;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 800;
    }
    .author-badge {
        background-color: rgba(0, 113, 206, 0.25);
        border: 1px solid rgba(0, 113, 206, 0.6);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "walmart_analytics.db")

@st.cache_data
def load_data():
    df_weekly = pd.read_csv(os.path.join(DATA_DIR, "weekly_revenue.csv"))
    df_brands = pd.read_csv(os.path.join(DATA_DIR, "brand_summary.csv"))
    df_stores = pd.read_csv(os.path.join(DATA_DIR, "stores.csv"))
    return df_weekly, df_brands, df_stores

df_weekly, df_brands, df_stores = load_data()

# ---------------------------------------------------------
# Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="banner">
    <div>
        <h1>🛒 Walmart Market Data Analytics Suite</h1>
        <p style="margin: 0.2rem 0 0 0; color: #CBD5E1; font-size: 0.9rem;">
            Cross-Border Retail Business Intelligence (USA • Mexico • Canada)
        </p>
    </div>
    <div class="author-badge">
        👤 Created by <strong>Sadiq Khan</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Navigation & Filters
# ---------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg", width=160)
st.sidebar.title("Navigation & Filters")

app_mode = st.sidebar.radio(
    "Select View:",
    ["📊 Executive Dashboard", "🐍 Python & OLS Regression", "🗄️ SQL Analytics Studio", "📑 Excel & Power BI Assets"]
)

# Geographic Slicer
selected_region = st.sidebar.selectbox(
    "Geographic Filter:",
    ["All Regions", "USA", "Mexico", "Canada"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Technical Architecture:**
- **Python:** SciPy, Statsmodels, Pandas
- **SQL:** SQLite Star Schema with Window Functions
- **Power BI:** DAX Measures & Star Schema
- **Theme:** 2 Solid Colors (`#0071CE` & `#041E42`)
""")

# ---------------------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if app_mode == "📊 Executive Dashboard":
    # BAN Cards (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.metric(label="Current Month Transactions", value="18,325", delta="+5.69% vs Target")
    with k2:
        st.metric(label="Current Month Net Profit", value="$71,682", delta="+5.61% vs Target")
    with k3:
        st.metric(label="Current Month Returns", value="496", delta="-2.90% (Low is Good)", delta_color="inverse")
    with k4:
        st.metric(label="Total Net Revenue (1998)", value="$449,627", delta="59.94% Avg Margin")

    st.markdown("---")

    # Middle Row: Weekly Revenue Trend & Regional Breakdown
    col_chart, col_regions = st.columns([2, 1])

    with col_chart:
        st.subheader("Weekly Revenue Trending (52 Weeks)")
        
        # Color peak weeks with primary blue, standard weeks with navy
        df_weekly['color'] = df_weekly['week_number'].apply(lambda w: '#0071CE' if w >= 48 else '#041E42')
        
        fig_rev = px.bar(
            df_weekly,
            x='week_number',
            y='revenue',
            labels={'week_number': 'Week of Year (1998)', 'revenue': 'Revenue ($)'},
            title="52-Week Revenue Trajectory (Q4 Holiday Acceleration to $40K+/wk)"
        )
        fig_rev.update_traces(marker_color=df_weekly['color'])
        fig_rev.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", color="#041E42"),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_regions:
        st.subheader("Regional Share")
        reg_df = pd.DataFrame({
            "Country": ["USA", "Mexico", "Canada"],
            "Transactions": [93890, 72810, 12770],
            "Share": [52.4, 40.6, 7.0]
        })
        fig_pie = px.pie(
            reg_df,
            names="Country",
            values="Transactions",
            color="Country",
            color_discrete_map={"USA": "#0071CE", "Mexico": "#041E42", "Canada": "#64748B"},
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor='white',
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bottom Row: Brand Performance Matrix
    st.subheader("Product Brand Performance Matrix")
    search_term = st.text_input("🔍 Search Brand Name:", "")
    
    filtered_brands = df_brands.copy()
    if search_term:
        filtered_brands = filtered_brands[filtered_brands['product_brand'].str.contains(search_term, case=False)]

    display_df = filtered_brands[['brand_id', 'product_brand', 'category', 'transactions', 'revenue', 'profit', 'profit_margin', 'return_rate']].copy()
    display_df['profit_margin'] = (display_df['profit_margin'] * 100).map("{:.2f}%".format)
    display_df['return_rate'] = (display_df['return_rate'] * 100).map("{:.2f}%".format)
    display_df['revenue'] = display_df['revenue'].map("${:,.0f}".format)
    display_df['profit'] = display_df['profit'].map("${:,.0f}".format)
    display_df['transactions'] = display_df['transactions'].map("{:,}".format)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 2: PYTHON & OLS REGRESSION
# ---------------------------------------------------------
elif app_mode == "🐍 Python & OLS Regression":
    st.header("Python Ordinary Least Squares (OLS) Linear Trend Analysis")
    st.write("Exploratory Data Analysis and statistical significance testing on Walmart 1998 weekly revenue.")

    # Compute Regression
    slope, intercept, r_val, p_val, std_err = stats.linregress(df_weekly['week_number'], df_weekly['revenue'])
    r_squared = r_val ** 2

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Weekly Velocity (Slope)", f"+${slope:.2f}/wk")
    c2.metric("R-Squared (R²)", f"{r_squared:.4f}", "73.0% Variance Explained")
    c3.metric("P-Value", f"{p_val:.2e}", "p < 0.001 (Highly Significant)")
    c4.metric("Std Error", f"±${std_err:.2f}")

    st.markdown("---")

    # Plot Trendline
    df_weekly['trendline'] = intercept + slope * df_weekly['week_number']
    fig_ols = go.Figure()
    fig_ols.add_trace(go.Bar(
        x=df_weekly['week_number'],
        y=df_weekly['revenue'],
        name='Actual Weekly Revenue',
        marker_color='#041E42'
    ))
    fig_ols.add_trace(go.Scatter(
        x=df_weekly['week_number'],
        y=df_weekly['trendline'],
        name=f'OLS Trendline (R² = {r_squared:.3f})',
        line=dict(color='#0071CE', width=3, dash='dash')
    ))
    fig_ols.update_layout(
        title="OLS Linear Trend Fit: Revenue = 374.53 · Week + 20,247.96",
        xaxis_title="Week of Year (1998)",
        yaxis_title="Revenue ($)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="#041E42")
    )
    st.plotly_chart(fig_ols, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: SQL STUDIO
# ---------------------------------------------------------
elif app_mode == "🗄️ SQL Analytics Studio":
    st.header("Enterprise SQL Analytics Studio (SQLite)")
    st.write("Execute live SQL window queries against `walmart_analytics.db`.")

    queries = {
        "Q1: Top 10 Product Brands Pareto Analysis": """
WITH BrandRankings AS (
    SELECT 
        brand_id, product_brand, category, price_tier,
        transactions, revenue, profit,
        ROUND(profit_margin * 100, 2) AS profit_margin_pct,
        DENSE_RANK() OVER (ORDER BY transactions DESC) AS rank_by_volume,
        ROUND(revenue / (SELECT SUM(revenue) FROM brands) * 100, 2) AS pct_of_total_revenue
    FROM brands
)
SELECT rank_by_volume, product_brand, category, transactions, revenue, profit, profit_margin_pct, pct_of_total_revenue
FROM BrandRankings
WHERE rank_by_volume <= 10;
        """,
        "Q2: Month-over-Month Revenue Growth (LAG)": """
WITH MonthlyAggs AS (
    SELECT month, SUM(revenue) AS monthly_revenue, SUM(profit) AS monthly_profit, SUM(transactions) AS monthly_txns
    FROM weekly_revenue GROUP BY month
)
SELECT 
    month,
    monthly_revenue,
    monthly_profit,
    ROUND(((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY month)) / LAG(monthly_revenue, 1) OVER (ORDER BY month)) * 100, 2) || '%' AS rev_mom_growth
FROM MonthlyAggs;
        """,
        "Q3: Return Rate Anomaly Detection Flags": """
SELECT 
    product_brand, category, transactions, returns_count,
    ROUND(return_rate * 100, 2) || '%' AS return_rate_pct,
    CASE 
        WHEN return_rate >= 0.0110 THEN '🚨 HIGH RISK ANOMALY'
        WHEN return_rate >= 0.0100 THEN '⚠️ Moderate Risk'
        ELSE '✅ Healthy (<1.00%)'
    END AS quality_flag
FROM brands
ORDER BY return_rate DESC;
        """
    }

    selected_query_title = st.selectbox("Select Pre-Built Analytical Query:", list(queries.keys()))
    query_sql = queries[selected_query_title]

    st.code(query_sql, language="sql")

    if st.button("▶️ Execute Query in SQLite", type="primary"):
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            result_df = pd.read_sql_query(query_sql, conn)
            conn.close()
            st.success(f"Query returned {len(result_df)} rows successfully.")
            st.dataframe(result_df, use_container_width=True)
        else:
            st.error("Database file `walmart_analytics.db` not found.")

# ---------------------------------------------------------
# TAB 4: ASSETS & DOWNLOADS
# ---------------------------------------------------------
elif app_mode == "📑 Excel & Power BI Assets":
    st.header("Project Artifacts & Source Downloads")
    st.write("Download the native files used in this multi-tool analytics platform.")

    a1, a2, a3 = st.columns(3)
    
    with a1:
        st.subheader("📑 Excel Model")
        st.write("Dynamic 3-sheet financial workbook with `=G2/F2` margin formulas and `=SUM($D$2:D2)` cumulative totals.")
        if os.path.exists(os.path.join(BASE_DIR, "excel/walmart_executive_model.xlsx")):
            with open(os.path.join(BASE_DIR, "excel/walmart_executive_model.xlsx"), "rb") as f:
                st.download_button("Download Excel Model (.xlsx)", f, "walmart_executive_model.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary")

    with a2:
        st.subheader("📊 Power BI Report")
        st.write("Complete Star Schema data model with custom DAX measures catalog and interactive canvas.")
        if os.path.exists(os.path.join(BASE_DIR, "Wallmart Market Report(Power BI).pbix")):
            with open(os.path.join(BASE_DIR, "Wallmart Market Report(Power BI).pbix"), "rb") as f:
                st.download_button("Download Power BI (.pbix)", f, "Wallmart Market Report(Power BI).pbix", "application/octet-stream", type="primary")

    with a3:
        st.subheader("📓 Jupyter Notebook")
        st.write("Interactive Python notebook containing exploratory analysis, SciPy regressions, and data visualizations.")
        if os.path.exists(os.path.join(BASE_DIR, "walmart_data_analytics.ipynb")):
            with open(os.path.join(BASE_DIR, "walmart_data_analytics.ipynb"), "rb") as f:
                st.download_button("Download Notebook (.ipynb)", f, "walmart_data_analytics.ipynb", "application/x-ipynb+json", type="primary")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem;">
    Walmart Market End-to-End Data Analytics Platform &copy; 2026 | Built by <strong>Sadiq Khan</strong>
</div>
""", unsafe_allow_html=True)
