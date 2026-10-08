-- Revenue growth compared with the same quarter a year earlier.
-- LAG(revenue, 4) looks 4 rows back within each company, i.e. one year ago.
-- Comparing with the same quarter last year removes seasonal swings (e.g. holiday sales).
SELECT
    company,
    quarter,
    mid_date,
    revenue,
    LAG(revenue, 4) OVER (PARTITION BY company ORDER BY quarter_id) AS revenue_year_ago,
    revenue / LAG(revenue, 4) OVER (PARTITION BY company ORDER BY quarter_id) - 1 AS yoy_growth
FROM v_financials
ORDER BY company, quarter_id;