-- Calendar-year totals per company (complete years only),
-- with the margin worked out from the yearly totals.
SELECT
    f.company,
    q.year,
    SUM(f.revenue) / 1e9                       AS revenue_bn,
    SUM(f.operating_income) / 1e9              AS operating_income_bn,
    SUM(f.net_income) / 1e9                    AS net_income_bn,
    SUM(f.operating_income) / SUM(f.revenue)   AS operating_margin
FROM v_financials f
JOIN dim_quarter q ON q.quarter_id = f.quarter_id
GROUP BY f.company, q.year
HAVING COUNT(*) = 4
ORDER BY f.company, q.year;