"""Audit, clean and enrich the COVID-19 dataset."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

REQUIRED = {"date", "country", "confirmed", "deaths", "vaccinated"}

def load_and_clean(input_path: str, reference_path: str):
    df = pd.read_csv(input_path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["confirmed", "deaths", "recovered", "vaccinated", "population"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Preserve supplied values for auditability before applying reference values.
    if "continent" not in df.columns:
        df["continent"] = "Unknown"
    if "population" not in df.columns:
        df["population"] = np.nan
    df["continent_original"] = df["continent"]
    df["population_original"] = df["population"]

    ref = pd.read_csv(reference_path)
    ref = ref.drop_duplicates("country").set_index("country")
    df["reference_continent"] = df["country"].map(ref["reference_continent"])
    df["reference_population"] = df["country"].map(ref["reference_population"])
    df["continent"] = df["reference_continent"].fillna(df["continent"])
    df["population"] = df["reference_population"].fillna(df["population"])

    # Audit flags: anomalies are flagged, not silently removed.
    df["flag_invalid_date"] = df["date"].isna()
    df["flag_negative_values"] = (
        (df[["confirmed", "deaths", "vaccinated"]].fillna(0) < 0).any(axis=1)
    )
    df["flag_deaths_gt_confirmed"] = df["deaths"] > df["confirmed"]
    df["flag_vaccinated_gt_population"] = df["vaccinated"] > df["population"]
    df = df.sort_values(["country", "date"]).reset_index(drop=True)
    df["flag_falling_confirmed"] = df.groupby("country")["confirmed"].diff().lt(0).fillna(False)
    df["flag_falling_deaths"] = df.groupby("country")["deaths"].diff().lt(0).fillna(False)
    flag_cols = [c for c in df.columns if c.startswith("flag_")]
    df["anomaly_count"] = df[flag_cols].sum(axis=1)
    df["has_anomaly"] = df["anomaly_count"] > 0

    # Derived metrics. Rates are calculated row-wise and are not averaged to
    # produce aggregate rates; use pooled totals for country-level summaries.
    pop = df["population"].replace(0, np.nan)
    confirmed = df["confirmed"].replace(0, np.nan)
    df["cases_per_100k"] = df["confirmed"] / pop * 100_000
    df["deaths_per_100k"] = df["deaths"] / pop * 100_000
    df["case_fatality_rate_pct"] = df["deaths"] / confirmed * 100
    if "recovered" in df.columns:
        df["recovery_rate_pct"] = df["recovered"] / confirmed * 100
    else:
        df["recovery_rate_pct"] = np.nan

    return df, flag_cols

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="dataset.csv")
    parser.add_argument("--reference", default="country_reference.csv")
    parser.add_argument("--output", default="outputs/dataset_cleaned.csv")
    args = parser.parse_args()
    df, flags = load_and_clean(args.input, args.reference)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Rows processed: {len(df)}")
    print(f"Rows with at least one anomaly: {int(df['has_anomaly'].sum())}")
    print(f"Flag columns: {', '.join(flags)}")
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
