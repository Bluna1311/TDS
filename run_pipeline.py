from fetcher import fetch
from clean import clean
from charts import make_charts

print("1. Fetching data from the SEC...")
fetch()

print("\n2. Cleaning...")
clean()

print("\n3. Drawing charts...")
make_charts()

print("\nDone.")