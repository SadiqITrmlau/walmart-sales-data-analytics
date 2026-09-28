import os
import sys
import sqlite3
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "walmart_analytics.db")

print("=" * 75)
print("  WALMART MARKET SQL ANALYTICS RUNNER - CREATED BY SADIQ KHAN")
print("  Database:", DB_PATH)
print("=" * 75)

if not os.path.exists(DB_PATH):
    print("Database not found! Running build_data_and_models.py first...")
    import subprocess
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "build_data_and_models.py")])

conn = sqlite3.connect(DB_PATH)

queries = [
    (
        "QUERY 1: Top 10 Product Brands Pareto Analysis (Volume & Revenue)",
        """
        WITH BrandRankings AS (
            SELECT 
                brand_id,
                product_brand,
                category,
                price_tier,
                transactions,
                revenue,
                profit,
                ROUND(profit_margin * 100, 2) AS profit_margin_pct,
                ROUND(return_rate * 100, 2) AS return_rate_pct,
                DENSE_RANK() OVER (ORDER BY transactions DESC) AS rank_by_volume,
                ROUND(revenue / (SELECT SUM(revenue) FROM brands) * 100, 2) AS pct_of_total_revenue
            FROM brands
        )
        SELECT 
            rank_by_volume AS 'Rank',
            product_brand AS 'Brand',
            category AS 'Category',
            price_tier AS 'Tier',
            transactions AS 'Txns',
            '$' || printf('%,d', CAST(revenue AS INT)) AS 'Revenue ($)',
            '$' || printf('%,d', CAST(profit AS INT)) AS 'Profit ($)',
            profit_margin_pct || '%' AS 'Margin %',
            pct_of_total_revenue || '%' AS 'Share %'
        FROM BrandRankings
        WHERE rank_by_volume <= 10;
        """
    ),
    (
        "QUERY 2: Month-over-Month (MoM) Window Growth Analysis",
        """
        WITH MonthlyAggregates AS (
            SELECT 
                month,
                SUM(revenue) AS monthly_revenue,
                SUM(profit) AS monthly_profit,
                SUM(transactions) AS monthly_txns
            FROM weekly_revenue
            GROUP BY month
        ),
        MoMCalculations AS (
            SELECT 
                month,
                monthly_revenue,
                monthly_profit,
                monthly_txns,
                LAG(monthly_revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
                LAG(monthly_profit, 1) OVER (ORDER BY month) AS prev_month_profit,
                LAG(monthly_txns, 1) OVER (ORDER BY month) AS prev_month_txns
            FROM MonthlyAggregates
        )
        SELECT 
            month AS 'Month',
            '$' || printf('%,d', CAST(monthly_revenue AS INT)) AS 'Revenue ($)',
            '$' || printf('%,d', CAST(monthly_profit AS INT)) AS 'Profit ($)',
            monthly_txns AS 'Txns',
            COALESCE(ROUND(((monthly_revenue - prev_month_revenue) / prev_month_revenue) * 100, 2) || '%', 'N/A') AS 'Rev MoM %',
            COALESCE(ROUND(((monthly_profit - prev_month_profit) / prev_month_profit) * 100, 2) || '%', 'N/A') AS 'Profit MoM %'
        FROM MoMCalculations;
        """
    ),
    (
        "QUERY 3: Store Performance & Regional Ranking (Partitioned by Country)",
        """
        SELECT 
            s.store_country AS 'Country',
            s.store_name AS 'Store Name',
            s.store_city AS 'City',
            s.transactions AS 'Annual Txns',
            s.december_txns AS 'Dec Txns',
            DENSE_RANK() OVER (PARTITION BY s.store_country ORDER BY s.transactions DESC) AS 'Country Rank',
            CASE 
                WHEN s.december_txns >= 1000 THEN '🎯 1,000+ Target Met'
                ELSE 'Standard'
            END AS 'Benchmark'
        FROM stores s
        ORDER BY s.store_country, 'Country Rank';
        """
    ),
    (
        "QUERY 4: Quality & Return Rate Anomaly Detection",
        """
        SELECT 
            product_brand AS 'Brand',
            category AS 'Category',
            transactions AS 'Txns',
            returns_count AS 'Returns',
            ROUND(return_rate * 100, 2) || '%' AS 'Return Rate %',
            CASE 
                WHEN return_rate >= 0.0110 THEN '🚨 HIGH RISK ANOMALY'
                WHEN return_rate >= 0.0100 THEN '⚠️ Moderate Risk'
                ELSE '✅ Healthy Quality'
            END AS 'Quality Status'
        FROM brands
        ORDER BY return_rate DESC
        LIMIT 8;
        """
    )
]

for title, sql in queries:
    print("\n" + "-" * 75)
    print(f"📊 {title}")
    print("-" * 75)
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))

conn.close()
print("\n" + "=" * 75)
print("✅ SQL Queries executed successfully!")
print("=" * 75)
