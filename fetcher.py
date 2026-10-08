import json
import time
from pathlib import Path

import requests

from config import COMPANIES, RAW_DIR, USER_AGENT


def fetch():

    raw_dir = Path(RAW_DIR)
    raw_dir.mkdir(parents=True, exist_ok=True)

    for key, company in COMPANIES.items():
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{company['cik']:010d}.json"
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        data = response.json()

        with open(raw_dir / f"{key}.json", "w") as f:
            json.dump(data, f)

        print(key, "->", data["entityName"])
        time.sleep(0.2)


if __name__ == "__main__":
    fetch()