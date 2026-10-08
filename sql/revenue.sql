-- Quarterly revenue per company, in $ billions
SELECT
    company,
    quarter,
    mid_date,
    revenue / 1e9 AS revenue_bn
FROM v_financials
ORDER BY company, quarter_id;