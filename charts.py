from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def make_charts():
    df = pd.read_csv("data/clean/financials.csv", parse_dates=["start", "end"])


    # incase charts folder doesnt exist.
    CHART_DIR = Path("charts")
    CHART_DIR.mkdir(exist_ok=True)

    # 1. Quarterly revenue, one line per company
    fig, ax = plt.subplots(figsize=(10, 5))
    for company, group in df.groupby("company"):
        ax.plot(group["end"], group["revenue"] / 1e9, label=company)
    ax.set_title("Quarterly revenue")
    ax.set_ylabel("$ billions")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.savefig(CHART_DIR / "revenue.png", dpi=150, bbox_inches="tight")

    # 2. Operating margin, one line per company
    fig, ax = plt.subplots(figsize=(10, 5))
    for company, group in df.groupby("company"):
        ax.plot(group["end"], group["operating_margin"] * 100, label=company)
    ax.set_title("Operating margin (operating income ÷ revenue)")
    ax.set_ylabel("%")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.savefig(CHART_DIR / "operating_margin.png", dpi=150, bbox_inches="tight")

    print("saved charts to", CHART_DIR)


if __name__ == "__main__":
    make_charts()