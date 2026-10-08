-- Operating margin per company per quarter:
-- how much of each dollar of sales is left as operating profit
SELECT
    company,
    quarter,
    mid_date,
    operating_income / revenue AS operating_margin
FROM v_financials
ORDER BY company, quarter_id;