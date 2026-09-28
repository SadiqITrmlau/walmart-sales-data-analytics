-- ====================================================================
-- WALMART MARKET ADVANCED SQL ANALYTICS SUITE
-- Author: Sadiq Khan
-- Dialect: ANSI SQL / SQLite / PostgreSQL / MySQL Compatible
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Top 10 Product Brands Pareto Analysis (Revenue & Margin)
-- --------------------------------------------------------------------
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
    rank_by_volume,
    product_brand,
    category,
    price_tier,
    transactions,
    '$' || printf('%,d', CAST(revenue AS INT)) AS formatted_revenue,
    '$' || printf('%,d', CAST(profit AS INT)) AS formatted_profit,
    profit_margin_pct || '%' AS margin,
    pct_of_total_revenue || '%' AS share_of_revenue
FROM BrandRankings
WHERE rank_by_volume <= 10;


-- --------------------------------------------------------------------
-- QUERY 2: Month-over-Month (MoM) Revenue & Profit Window Analysis
-- --------------------------------------------------------------------
WITH MonthlyAggregates AS (
    SELECT 
        month,
        SUM(revenue) AS monthly_revenue,
        SUM(profit) AS monthly_profit,
        SUM(transactions) AS monthly_txns,
        SUM(returns) AS monthly_returns
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
    month,
    ROUND(monthly_revenue, 2) AS current_revenue,
    ROUND(monthly_profit, 2) AS current_profit,
    monthly_txns,
    ROUND(((monthly_revenue - prev_month_revenue) / prev_month_revenue) * 100, 2) AS revenue_mom_growth_pct,
    ROUND(((monthly_profit - prev_month_profit) / prev_month_profit) * 100, 2) AS profit_mom_growth_pct,
    ROUND(((CAST(monthly_txns AS FLOAT) - prev_month_txns) / prev_month_txns) * 100, 2) AS txns_mom_growth_pct
FROM MoMCalculations;


-- --------------------------------------------------------------------
-- QUERY 3: Store Performance & Regional Ranking (Partitioned by Country)
-- --------------------------------------------------------------------
SELECT 
    s.store_country,
    s.store_name,
    s.store_city,
    s.store_state,
    s.transactions,
    s.december_txns,
    r.sales_district,
    DENSE_RANK() OVER (PARTITION BY s.store_country ORDER BY s.transactions DESC) AS country_rank,
    CASE 
        WHEN s.december_txns >= 1000 THEN '🎯 1,000+ Milestone Achieved'
        WHEN s.december_txns >= 800 THEN '⭐ High Volume'
        ELSE 'Normal Volume'
    END AS december_performance_status
FROM stores s
JOIN regions r ON s.region_id = r.region_id
ORDER BY s.store_country, country_rank;


-- --------------------------------------------------------------------
-- QUERY 4: Return Rate Anomaly Detection & Quality Risk Flags
-- --------------------------------------------------------------------
SELECT 
    product_brand,
    category,
    transactions,
    returns_count,
    ROUND(return_rate * 100, 2) AS return_rate_pct,
    CASE 
        WHEN return_rate >= 0.0110 THEN '🚨 HIGH RETURN ANOMALY (Action Required)'
        WHEN return_rate >= 0.0100 THEN '⚠️ Moderate Return Rate'
        ELSE '✅ Healthy Quality (<1.00%)'
    END AS quality_risk_flag
FROM brands
ORDER BY return_rate DESC;


-- --------------------------------------------------------------------
-- QUERY 5: 4-Week Moving Average & Seasonality Spike Analysis
-- --------------------------------------------------------------------
SELECT 
    week_number,
    month,
    revenue,
    ROUND(AVG(revenue) OVER (
        ORDER BY week_number 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ), 2) AS four_week_moving_avg,
    CASE 
        WHEN revenue >= 40000 THEN '🔥 Holiday Q4 Surge Peak'
        WHEN revenue >= 30000 THEN '📈 High Summer/Fall Velocity'
        ELSE 'Normal Baseline'
    END AS sales_velocity_tier
FROM weekly_revenue
ORDER BY week_number;
