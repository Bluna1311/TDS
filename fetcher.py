import json
import time
from pathlib import Path

import requests

# The SEC requires a name and contact email (see its "Fair access" policy)
HEADERS = {"User-Agent": "Brian Luna brian1311@hotmail.co.uk"}

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# company name -> SEC ID number (CIK), looked up with EDGAR company search
COMPANIES = {
    "apple": 320193,
    "microsoft": 789019,
    "alphabet": 1652044,
    "amazon": 1018724,
    "nvidia": 1045810,
}
def fetch():
    """Download each company's data from the SEC into data/raw/."""
    for name, cik in COMPANIES.items():
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        with open(RAW_DIR / f"{name}.json", "w") as f:
            json.dump(data, f)

        print(name, "->", data["entityName"])
        time.sleep(0.2)


if __name__ == "__main__":
    fetch()