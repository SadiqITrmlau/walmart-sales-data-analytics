-- ====================================================================
-- WALMART MARKET BUSINESS INTELLIGENCE DATABASE SCHEMA
-- Author: Sadiq Khan
-- Dialect: SQLite / PostgreSQL / MySQL Compatible
-- Architecture: Star Schema (Dimensions & Facts)
-- ====================================================================

-- 1. DIMENSION: REGIONS
DROP TABLE IF EXISTS regions;
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    sales_district VARCHAR(100) NOT NULL,
    sales_region VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- 2. DIMENSION: STORES
DROP TABLE IF EXISTS stores;
CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR(150) NOT NULL,
    store_city VARCHAR(100) NOT NULL,
    store_state VARCHAR(50) NOT NULL,
    store_country VARCHAR(50) NOT NULL,
    region_id INTEGER,
    grocery_sqft INTEGER,
    first_opened DATE,
    transactions INTEGER,
    december_txns INTEGER,
    FOREIGN KEY(region_id) REFERENCES regions(region_id)
);

-- 3. DIMENSION: PRODUCTS & BRANDS
DROP TABLE IF EXISTS brands;
CREATE TABLE brands (
    brand_id INTEGER PRIMARY KEY,
    product_brand VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price_tier VARCHAR(20) NOT NULL,
    transactions INTEGER,
    profit DECIMAL(12, 2),
    revenue DECIMAL(12, 2),
    profit_margin DECIMAL(5, 4),
    return_rate DECIMAL(5, 4),
    returns_count INTEGER
);

-- 4. FACT: 52-WEEK REVENUE TIME SERIES (1998)
DROP TABLE IF EXISTS weekly_revenue;
CREATE TABLE weekly_revenue (
    week_number INTEGER PRIMARY KEY,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    revenue DECIMAL(12, 2),
    profit DECIMAL(12, 2),
    transactions INTEGER,
    returns INTEGER
);

-- 5. CREATE OPTIMIZED INDEXES FOR HIGH-PERFORMANCE ANALYTICS
CREATE INDEX IF NOT EXISTS idx_stores_country ON stores(store_country);
CREATE INDEX IF NOT EXISTS idx_stores_city ON stores(store_city);
CREATE INDEX IF NOT EXISTS idx_brands_margin ON brands(profit_margin);
CREATE INDEX IF NOT EXISTS idx_weekly_month ON weekly_revenue(month);

-- 6. ANALYTIC VIEW: Topline Executive KPI Summary
CREATE VIEW IF NOT EXISTS v_topline_kpis AS
SELECT
    COUNT(DISTINCT s.store_id) AS total_stores,
    SUM(b.transactions) AS total_annual_transactions,
    ROUND(SUM(b.revenue), 2) AS total_annual_revenue,
    ROUND(SUM(b.profit), 2) AS total_annual_profit,
    ROUND(SUM(b.profit) / SUM(b.revenue) * 100, 2) AS avg_profit_margin_pct,
    ROUND(CAST(SUM(b.returns_count) AS FLOAT) / SUM(b.transactions) * 100, 2) AS overall_return_rate_pct
FROM brands b, stores s;
