import json
from pathlib import Path

import pandas as pd

from config import COMPANIES, METRICS, RAW_DIR, STAGING_FILE

FORMS = ["10-Q", "10-K", "10-Q/A", "10-K/A"]


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

    df = pd.DataFrame(facts)

    # dates and period lengths
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df["days"] = (df["end"] - df["start"]).dt.days
    df["period"] = df["days"].apply(period_type)

    # official reports only, then remove duplicates
    # Match on end date + period type, not start date: Microsoft filed one
    # quarter with a start date a day off.
    df = df[df["form"].isin(FORMS)]
    df = df.sort_values("filed").drop_duplicates(subset=["end", "period"], keep="last")

    keep = ["start", "end", "val", "tag", "filed"]

    # Q4 = full year - nine months
    fy = df[df["period"] == "FY"][keep]
    nine = df[df["period"] == "9M"][["start", "end", "val"]]
    q4 = fy.merge(nine, on="start", suffixes=("_fy", "_9m"))
    q4["val"] = q4["val_fy"] - q4["val_9m"]
    q4["start"] = q4["end_9m"] + pd.Timedelta(days=1)
    q4["end"] = q4["end_fy"]

    # reported quarters + derived Q4s, no duplication
    reported = df[df["period"] == "Q"][keep].copy()
    reported["is_derived"] = False
    derived = q4[keep].copy()
    derived["is_derived"] = True
    derived = derived[~derived["end"].isin(reported["end"])]

    quarters = pd.concat([reported, derived])
    return quarters.sort_values("end").reset_index(drop=True)


def clean_company(key):

    with open(Path(RAW_DIR) / f"{key}.json") as f:
        data = json.load(f)
    gaap = data["facts"]["us-gaap"]

    tables = []
    for metric, tags in METRICS.items():
        facts = []
        for tag in tags:
            if tag in gaap:
                for fact in gaap[tag]["units"]["USD"]:
                    facts.append({**fact, "tag": tag})   # remember which tag each value came from
        q = to_quarters(facts)
        q["metric"] = metric
        tables.append(q)

    table = pd.concat(tables)
    table["company"] = key
    return table


def clean():
    """Clean every company into one long table: one row per company, quarter and metric."""
    long = pd.concat([clean_company(key) for key in COMPANIES])
    long = long[long["end"] >= "2015-01-01"]
    long = long.rename(columns={"start": "period_start", "end": "period_end",
                                "val": "value", "tag": "source_tag", "filed": "filed_date"})
    long = long[["company", "metric", "period_start", "period_end", "value",
                 "is_derived", "source_tag", "filed_date"]]

    Path(STAGING_FILE).parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(STAGING_FILE, index=False)

    print(long.groupby(["company", "metric"]).size().unstack())
    print("empty cells:", long.isna().sum().sum())
    print("duplicates:", long.duplicated(subset=["company", "metric", "period_end"]).sum())


if __name__ == "__main__":
    clean()