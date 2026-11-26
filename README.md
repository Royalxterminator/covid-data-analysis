# COVID-19 Data Analysis and Visualisation

A beginner-friendly Python data analytics project that audits a multi-country COVID-19 dataset, cleans country reference fields, engineers comparable metrics, flags suspicious records, and produces charts plus a standalone interactive HTML dashboard.

## Important data note
The included `dataset.csv` is **synthetic demonstration data** (500 rows: 50 dates × 10 countries). It is included so the repository runs immediately. Replace it with your approved project dataset before submitting results. Do not present demo outputs as real-world COVID-19 findings. The included `country_reference.csv` is an editable example reference table; verify population/continent values and cite the source/date you use.

## Project structure
```text
covid19_data_analysis_project/
├── dataset.csv                 # synthetic demo input; replace with your dataset
├── country_reference.csv       # country-to-continent/population lookup
├── requirements.txt
├── README.md
├── src/
│   ├── clean_data.py           # validation, cleaning, anomaly flags, derived metrics
│   ├── analysis.py             # seven exploratory charts and country summary
│   └── dashboard.py            # standalone interactive HTML dashboard
└── outputs/                    # generated outputs
```

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\\Scripts\\activate

pip install -r requirements.txt
```

## Run the complete pipeline
Run these commands from the project root:

```bash
python -m src.clean_data
python -m src.analysis
python -m src.dashboard
```

Then open `outputs/dashboard.html` in a browser. The dashboard loads Plotly.js from a CDN, so an internet connection is needed to render charts.

## Expected input columns
Required: `date`, `country`, `confirmed`, `deaths`, `vaccinated`.

Optional: `continent`, `population`, `recovered`.

If your source uses different column names, rename them in the CSV or update `REQUIRED` and the field references in `src/clean_data.py`. `country_reference.csv` should contain:
- `country`
- `reference_continent`
- `reference_population`

## Data-quality approach
The pipeline preserves original continent/population values in separate columns, uses the reference table for standardised values, and creates flags for invalid dates, negative values, deaths exceeding confirmed cases, vaccination counts exceeding population, and falling cumulative counts. It flags suspicious records rather than silently deleting them.

Rates are calculated per row for exploration. Country-level case fatality rate should be calculated from pooled totals (`total deaths / total confirmed × 100`), not by averaging row-level percentages.

## Outputs
- `outputs/dataset_cleaned.csv`
- `outputs/country_summary.csv`
- `outputs/figures/01_cases_over_time.png` through `07_correlation_heatmap.png`
- `outputs/dashboard.html`

## Suggested GitHub description
COVID-19 Data Analysis and Visualisation using Python, Pandas, NumPy, Matplotlib, Seaborn and Plotly. Includes data cleaning, anomaly detection, feature engineering, exploratory visualisations and an interactive HTML dashboard.

## References
- Our World in Data COVID-19 dataset: https://github.com/owid/covid-19-data
- WHO COVID-19 Dashboard: https://covid19.who.int
- Pandas documentation: https://pandas.pydata.org/docs/
- Plotly Python documentation: https://plotly.com/python/
