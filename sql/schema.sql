-- Star schema: one fact table (one value per company, quarter and metric)
-- with three dimension tables describing who, when and what.
-- Rebuilt from scratch on every run.

-- WHO: one row per company
CREATE OR REPLACE TABLE dim_company AS
SELECT
    ROW_NUMBER() OVER (ORDER BY name) AS company_id,
    company_key,
    name,
    ticker,
    cik
FROM companies_input;

-- WHAT: one row per metric
CREATE OR REPLACE TABLE dim_metric (
    metric_id   INTEGER PRIMARY KEY,
    metric_key  VARCHAR,
    name        VARCHAR,
    description VARCHAR
);
INSERT INTO dim_metric VALUES
    (1, 'revenue',          'Revenue',          'Total sales, before any costs'),
    (2, 'operating_income', 'Operating income', 'Profit from running the business, before interest and tax'),
    (3, 'net_income',       'Net income',       'Profit after all costs, interest and tax');

-- The staging data with each row's calendar quarter worked out.
-- Companies' financial years differ, so each period is assigned to the
-- calendar quarter containing its midpoint (e.g. Apple's Oct-Dec quarter -> 2025 Q4).
CREATE OR REPLACE TEMP TABLE staged AS
SELECT
    *,
    period_start + CAST(date_diff('day', period_start, period_end) / 2 AS INTEGER) AS midpoint
FROM read_csv('data/staging/financials_long.csv');

-- WHEN: one row per calendar quarter
CREATE OR REPLACE TABLE dim_quarter AS
SELECT DISTINCT
    year(midpoint) * 10 + quarter(midpoint)                AS quarter_id,   -- e.g. 20254
    year(midpoint)                                         AS year,
    quarter(midpoint)                                      AS quarter,
    year(midpoint) || ' Q' || quarter(midpoint)            AS label,
    make_date(year(midpoint), quarter(midpoint) * 3 - 1, 15) AS mid_date  -- middle of the quarter, for charts
FROM staged
ORDER BY quarter_id;

-- THE FACTS: one row per company, quarter and metric, with where each value came from
CREATE OR REPLACE TABLE fact_financials AS
SELECT
    c.company_id,
    year(s.midpoint) * 10 + quarter(s.midpoint) AS quarter_id,
    m.metric_id,
    s.value,
    s.is_derived,
    s.source_tag,
    s.filed_date,
    s.period_start,
    s.period_end
FROM staged s
JOIN dim_company c ON c.company_key = s.company
JOIN dim_metric  m ON m.metric_key  = s.metric;

-- A wide view for analysis: one row per company per quarter, a column per metric.
-- FILTER picks out each metric's value from the long table (a pivot).
CREATE OR REPLACE VIEW v_financials AS
SELECT
    c.name                                                  AS company,
    q.quarter_id,
    q.label                                                 AS quarter,
    q.mid_date,
    MAX(f.value) FILTER (WHERE m.metric_key = 'revenue')          AS revenue,
    MAX(f.value) FILTER (WHERE m.metric_key = 'operating_income') AS operating_income,
    MAX(f.value) FILTER (WHERE m.metric_key = 'net_income')       AS net_income
FROM fact_financials f
JOIN dim_company c ON c.company_id = f.company_id
JOIN dim_quarter q ON q.quarter_id = f.quarter_id
JOIN dim_metric  m ON m.metric_id  = f.metric_id
GROUP BY c.name, q.quarter_id, q.label, q.mid_date;