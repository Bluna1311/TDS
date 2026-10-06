# SEC Financials Pipeline

A small data pipeline that pulls quarterly financial records for five large US tech companies from the SEC's API, cleans and combines them into one consistent table, and charts the results.

**Companies:** Apple, Microsoft, Alphabet, Amazon, NVIDIA

**Metrics:** revenue, operating income, net income, plus operating and net margin

## About me

I'm Brian Luna. I have a background in Theoretical Physics (BSc), Financial Mathematics (PG Dip) and Financial Engineering (MSc), and I've worked in tech consultancy. Across all of these, the common thread has been working with numbers and data: building models, and making sure the data going into them is right.

## Aims of the project

The aim of the project is to compare the financial performance of multiple companies using their official SEC records. The problem is that these records can't be compared directly, quarter by quarter:

- **Q4 is missing.** Companies report the full year instead of a fourth quarter.
- **Companies use different financial years.** Apple's ends in September, Microsoft's in June.
- **The same figure is reported under different names**, and the names change over time.
- **Every figure is filed many times**, because each report repeats earlier results.

The goal was to fix these problems and produce one clean table, then use it to compare the five companies on both size (revenue) and efficiency (how much of each dollar of sales they keep as profit).

## Reasons for applying

I'm applying because the part of this project I enjoyed most was the part this role focuses on: taking raw data from a real source and turning it into something reliable that others can use. I have the technical and analytical mindset from my studies, and my consultancy background means I'm used to working with clients and turning their problems into practical solutions. I'm now looking to build on that with professional experience using the tools and practices teams rely on day to day.

## How to run

Requires Python 3.10 or later.

1. Install the packages:
    **pip install -r requirements.txt**
2. Run the pipeline: **run_pipeline.py**
    
This runs three steps in order:

| step | script | what it does | output |
|---|---|---|---|
| 1 | `fetcher.py` | downloads each company's data from the SEC API | `data/raw/*.json` |
| 2 | `clean.py` | cleans and combines it into one table | `data/clean/financials.csv` |
| 3 | `charts.py` | draws the charts | `charts/*.png` |

Each script can also be run on its own, e.g. `python clean.py` to re-clean the data without downloading it again.

**Note:** the SEC requires a contact email in every request. Before running, change the `User-Agent` line in `fetcher.py` to your own name and email.