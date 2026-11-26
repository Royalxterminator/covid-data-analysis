"""Create summary tables and seven exploratory visualisations."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA = Path("outputs/dataset_cleaned.csv")
OUT = Path("outputs/figures")

def main():
    df = pd.read_csv(DATA, parse_dates=["date"])
    OUT.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Confirmed cases over time
    daily = df.groupby(["date", "country"], as_index=False)["confirmed"].max()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily, x="date", y="confirmed", hue="country")
    plt.title("Cumulative confirmed cases by country")
    plt.tight_layout(); plt.savefig(OUT/"01_cases_over_time.png", dpi=160); plt.close()

    # 2. Deaths over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="date", y="deaths", hue="country")
    plt.title("Cumulative deaths by country")
    plt.tight_layout(); plt.savefig(OUT/"02_deaths_over_time.png", dpi=160); plt.close()

    # Country-level pooled metrics (latest row per country)
    latest = df.sort_values("date").groupby("country", as_index=False).tail(1).copy()
    # 3. Cases per 100k
    plt.figure(figsize=(10, 6))
    sns.barplot(data=latest, x="cases_per_100k", y="country", color="steelblue")
    plt.title("Confirmed cases per 100,000 people")
    plt.tight_layout(); plt.savefig(OUT/"03_cases_per_100k.png", dpi=160); plt.close()

    # 4. Case fatality rate calculated from pooled/latest cumulative totals
    latest["pooled_cfr_pct"] = latest["deaths"] / latest["confirmed"].replace(0, float("nan")) * 100
    plt.figure(figsize=(10, 6))
    sns.barplot(data=latest, x="pooled_cfr_pct", y="country", color="steelblue")
    plt.title("Case fatality rate (%)")
    plt.tight_layout(); plt.savefig(OUT/"04_case_fatality_rate.png", dpi=160); plt.close()

    # 5. Vaccination relative to population (interpret cautiously; source may be inconsistent)
    latest["vaccinated_pct_population"] = latest["vaccinated"] / latest["population"] * 100
    plt.figure(figsize=(10, 6))
    sns.barplot(data=latest, x="vaccinated_pct_population", y="country", color="steelblue")
    plt.title("Reported vaccinated count as % of population (check data quality)")
    plt.tight_layout(); plt.savefig(OUT/"05_vaccination_population.png", dpi=160); plt.close()

    # 6. Anomaly count by country
    anomaly = df.groupby("country", as_index=False)["has_anomaly"].sum()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=anomaly, x="has_anomaly", y="country", color="steelblue")
    plt.title("Rows flagged for data-quality anomalies")
    plt.tight_layout(); plt.savefig(OUT/"06_anomalies_by_country.png", dpi=160); plt.close()

    # 7. Correlation heatmap
    numeric = df.select_dtypes("number").select_dtypes(exclude="bool")
    plt.figure(figsize=(11, 8))
    sns.heatmap(numeric.corr(), cmap="coolwarm", center=0)
    plt.title("Correlation heatmap of numeric variables")
    plt.tight_layout(); plt.savefig(OUT/"07_correlation_heatmap.png", dpi=160); plt.close()

    # Export summary using pooled totals, not averages of row-level rates.
    summary = df.groupby("country").agg(
        total_confirmed=("confirmed", "max"),
        total_deaths=("deaths", "max"),
        population=("population", "last"),
        anomalous_rows=("has_anomaly", "sum")
    ).reset_index()
    summary["pooled_cfr_pct"] = summary["total_deaths"] / summary["total_confirmed"].replace(0, float("nan")) * 100
    summary["cases_per_100k"] = summary["total_confirmed"] / summary["population"] * 100_000
    summary.to_csv("outputs/country_summary.csv", index=False)
    print(f"Saved seven figures to {OUT} and country_summary.csv")

if __name__ == "__main__":
    main()
