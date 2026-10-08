from pathlib import Path

import duckdb
import pandas as pd

from config import COMPANIES, WAREHOUSE_FILE


def load():
    """Build the DuckDB warehouse (star schema) from the staging CSV."""
    Path(WAREHOUSE_FILE).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(WAREHOUSE_FILE)

    # company details come from config.py; DuckDB can query a pandas table by its variable name
    companies_input = pd.DataFrame(
        [{"company_key": key, **details} for key, details in COMPANIES.items()]
    )
    con.register("companies_input", companies_input)

    con.execute(Path("sql/schema.sql").read_text())

    # checks
    for table in ["dim_company", "dim_quarter", "dim_metric", "fact_financials"]:
        print(f"{table:16} {con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]:>4} rows")

    dupes = con.execute("""
        SELECT COUNT(*) FROM (
            SELECT company_id, quarter_id, metric_id
            FROM fact_financials
            GROUP BY ALL
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    print("duplicate facts:", dupes)

    con.close()


if __name__ == "__main__":
    load()