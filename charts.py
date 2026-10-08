from pathlib import Path

import duckdb
import matplotlib.pyplot as plt

from config import WAREHOUSE_FILE

CHART_DIR = Path("output")


def run_query(con, name):

    return con.execute(Path(f"sql/{name}.sql").read_text()).df()


def line_chart(df, column, title, ylabel, filename, scale=1):

    fig, ax = plt.subplots(figsize=(10, 5))
    for company, group in df.groupby("company"):
        ax.plot(group["mid_date"], group[column] * scale, label=company)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.savefig(CHART_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def make_charts():

    CHART_DIR.mkdir(exist_ok=True)
    con = duckdb.connect(WAREHOUSE_FILE, read_only=True)

    line_chart(run_query(con, "revenue"), "revenue_bn",
               "Quarterly revenue", "$ billions", "revenue.png")
    line_chart(run_query(con, "operating_margin"), "operating_margin",
               "Operating margin (operating income / revenue)", "%", "operating_margin.png", scale=100)
    line_chart(run_query(con, "yoy_growth").dropna(), "yoy_growth",
               "Revenue growth vs same quarter a year earlier", "%", "yoy_growth.png", scale=100)

    annual = run_query(con, "annual_summary")
    annual.to_csv(CHART_DIR / "annual_summary.csv", index=False)
    con.close()
    print("saved output to", CHART_DIR, "as annual_summary.csv")


if __name__ == "__main__":
    make_charts()