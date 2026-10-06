import json
from pathlib import Path

import pandas as pd

FORMS = ["10-Q", "10-K", "10-Q/A", "10-K/A"]

# each metric -> the tag names it has been filed under
METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss"],
}

# file name for company data interested.
COMPANIES = {
    "apple": "Apple",
    "microsoft": "Microsoft",
    "alphabet": "Alphabet",
    "amazon": "Amazon",
    "nvidia": "NVIDIA",
}


def period_type(days):
    if 84 <= days <= 98:
        return "Q"
    if 175 <= days <= 190:
        return "6M"
    if 266 <= days <= 280:
        return "9M"
    if 357 <= days <= 378:
        return "FY"
    return None


def to_quarters(facts):
    #Raw list of facts for one metric -> one row per quarter
    df = pd.DataFrame(facts)

    # dates and period lengths
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df["days"] = (df["end"] - df["start"]).dt.days
    df["period"] = df["days"].apply(period_type)

    df = df[df["form"].isin(FORMS)]
    df = df.sort_values("filed").drop_duplicates(subset=["end", "period"], keep="last")

    # Q4 = full year - nine months
    fy = df[df["period"] == "FY"][["start", "end", "val"]]
    nine = df[df["period"] == "9M"][["start", "end", "val"]]
    q4 = fy.merge(nine, on="start", suffixes=("_fy", "_9m"))
    q4["val"] = q4["val_fy"] - q4["val_9m"]
    q4["start"] = q4["end_9m"] + pd.Timedelta(days=1)
    q4["end"] = q4["end_fy"]

    # reported quarters + derived Q4s, no duplication
    reported = df[df["period"] == "Q"][["start", "end", "val"]].copy()
    reported["source"] = "reported"
    derived = q4[["start", "end", "val"]].copy()
    derived["source"] = "derived"
    derived = derived[~derived["end"].isin(reported["end"])]

    quarters = pd.concat([reported, derived])
    return quarters.sort_values("end").reset_index(drop=True)


def clean_company(company):

    with open(f"data/raw/{company}.json") as f:
        data = json.load(f)
    gaap = data["facts"]["us-gaap"]

    table = None
    for name, tags in METRICS.items():
        facts = []
        for tag in tags:
            if tag in gaap:
                facts += gaap[tag]["units"]["USD"]
        q = to_quarters(facts)
        q = q[["start", "end", "val"]].rename(columns={"val": name})
        if table is None:
            table = q
        else:
            table = table.merge(q, on=["start", "end"], how="outer")

    table["company"] = COMPANIES[company]
    return table


def clean():
    #Cleanand save data/clean/financials.csv
    tables = [clean_company(c) for c in COMPANIES]
    all_companies = pd.concat(tables)
    all_companies = all_companies[all_companies["end"] >= "2015-01-01"]

    all_companies["operating_margin"] = all_companies["operating_income"] / all_companies["revenue"]
    all_companies["net_margin"] = all_companies["net_income"] / all_companies["revenue"]

    CLEAN_DIR = Path("data/clean")
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    all_companies.to_csv(CLEAN_DIR / "financials.csv", index=False)

    print(all_companies.groupby("company").size())
    print("empty cells:", all_companies.isna().sum().sum())
    print("duplicate quarters:", all_companies.duplicated(subset=["company", "end"]).sum())


if __name__ == "__main__":
    clean()