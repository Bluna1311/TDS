from fetcher import fetch
from clean import clean
from load import load
from output import make_charts

print("1. Extract: fetching data from the SEC...")
fetch()

print("\n2. Transform: cleaning...")
clean()

print("\n3. Load: building the warehouse...")
load()

print("\n4. Charts: querying the warehouse...")
make_charts()

print("\nDone.")