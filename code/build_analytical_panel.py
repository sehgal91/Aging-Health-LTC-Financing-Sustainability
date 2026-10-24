from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "master_panel_final.csv"
OUTPUT = ROOT / "data" / "analytical_panel_37_economies.csv"

COUNTRIES = [
    "Australia", "Austria", "Belgium", "Canada", "Chile", "Colombia",
    "Costa Rica", "Czech Republic", "Denmark", "Estonia", "Finland",
    "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
    "Israel", "Italy", "Japan", "Korea", "Latvia", "Lithuania",
    "Luxembourg", "Mexico", "Netherlands", "New Zealand", "Norway",
    "Portugal", "Slovak Republic", "Slovenia", "Spain", "Sweden",
    "Switzerland", "Türkiye", "United Kingdom", "United States"
]

CORE = ["HealthExp_GDP", "Pop65", "Dependency", "GDP_pc"]
REQUIRED = ["Country", "Year", *CORE]


def main():
    df = pd.read_csv(SOURCE)
    missing_columns = [c for c in REQUIRED if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    panel = df[df["Country"].isin(COUNTRIES) & df["Year"].between(2010, 2023)].copy()
    panel = panel.sort_values(["Country", "Year"]).reset_index(drop=True)

    if panel.duplicated(["Country", "Year"]).any():
        raise ValueError("Duplicate country-year records found in analytical sample")
    if len(panel) != 518:
        raise ValueError(f"Expected 518 observations; found {len(panel)}")
    if panel["Country"].nunique() != 37:
        raise ValueError(f"Expected 37 economies; found {panel['Country'].nunique()}")
    if panel[CORE].isna().any().any():
        missing = panel[CORE].isna().sum().to_dict()
        raise ValueError(f"Core variables contain missing values: {missing}")

    panel.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT} with {len(panel)} observations from {panel['Country'].nunique()} economies")


if __name__ == "__main__":
    main()
