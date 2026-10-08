USER_AGENT = "Your Name your.email@example.com"


COMPANIES = {
    "apple":     {"name": "Apple",     "ticker": "AAPL",  "cik": 320193},
    "microsoft": {"name": "Microsoft", "ticker": "MSFT",  "cik": 789019},
    "alphabet":  {"name": "Alphabet",  "ticker": "GOOGL", "cik": 1652044},
    "amazon":    {"name": "Amazon",    "ticker": "AMZN",  "cik": 1018724},
    "nvidia":    {"name": "NVIDIA",    "ticker": "NVDA",  "cik": 1045810},
}


METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss"],
}

RAW_DIR = "data/raw"
STAGING_FILE = "data/staging/financials_long.csv"
WAREHOUSE_FILE = "data/warehouse.duckdb"