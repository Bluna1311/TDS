import json
import pandas as pd
import json
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


with open("data/raw/apple.json") as f:
    data = json.load(f)

net_income = data["facts"]["us-gaap"]["NetIncomeLoss"]["units"]["USD"]
df = pd.DataFrame(net_income)

print(len(df))
print(df.tail(10))

df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])
df["days"] = (df["end"] - df["start"]).dt.days

print(df["days"].value_counts().head(10))

def period_type(days):
    if 84 <= days <= 98:
        return "Q"      # quarter
    if 175 <= days <= 190:
        return "6M"     # six months
    if 266 <= days <= 280:
        return "9M"     # nine months
    if 357 <= days <= 378:
        return "FY"     # full year
    return None

df["period"] = df["days"].apply(period_type)
print(df["period"].value_counts(dropna=False))
df = df[df["form"].isin(["10-Q", "10-K", "10-Q/A", "10-K/A"])]
print("after form filter:", len(df))

df = df.sort_values("filed")
df = df.drop_duplicates(subset=["start", "end"], keep="last")
df = df.sort_values("end").reset_index(drop=True)
print("after removing duplicates:", len(df))

print(df["period"].value_counts())

fy_start = pd.Timestamp("2024-09-29")
year = df[df["start"] == fy_start]
print(year[["start", "end", "val", "period"]])


fy = df[df["period"] == "FY"][["start", "end", "val"]]
nine = df[df["period"] == "9M"][["start", "end", "val"]]

q4 = fy.merge(nine, on="start", suffixes=("_fy", "_9m"))

q4["val"] = q4["val_fy"] - q4["val_9m"]
q4["q4_start"] = q4["end_9m"] + pd.Timedelta(days=1)
q4["q4_end"] = q4["end_fy"]

print(q4[["q4_start", "q4_end", "val_fy", "val_9m", "val"]].tail())

reported = df[df["period"] == "Q"][["start", "end", "val"]].copy()
reported["source"] = "reported"

derived = q4[["q4_start", "q4_end", "val"]].rename(columns={"q4_start": "start", "q4_end": "end"})
derived["source"] = "derived"

derived = derived[~derived["end"].isin(reported["end"])]


quarters = pd.concat([reported, derived])
quarters = quarters.sort_values("end").reset_index(drop=True)

print(len(quarters))
print(quarters["source"].value_counts())
print("duplicate quarters:", quarters["end"].duplicated().sum())
print(quarters.tail(8))

import json

with open("data/raw/apple.json") as f:
    data = json.load(f)

gaap = data["facts"]["us-gaap"]

for tag in gaap:
    if "Revenue" in tag:
        facts = gaap[tag]["units"].get("USD", [])
        if facts:
            ends = [f["end"] for f in facts]
            print(f"{tag:60} {min(ends)} → {max(ends)}  ({len(facts)} rows)")