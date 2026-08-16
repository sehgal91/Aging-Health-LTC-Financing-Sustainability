"""Audit the archived 2010–2023 analytical panel."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "master_panel_final.csv"
df = pd.read_csv(path)
lower = {c.lower(): c for c in df.columns}
country = next((lower[k] for k in ("country", "economy", "country_name") if k in lower), None)
year = lower.get("year")
if not country or not year:
    raise ValueError("Country/economy and year columns are required")
if df.duplicated([country, year]).any():
    raise ValueError("Duplicate country-year keys detected")
years = pd.to_numeric(df[year], errors="raise")
panel = df.loc[years.between(2010, 2023)]
if len(panel) != 518 or panel[country].nunique() != 37:
    raise ValueError("Expected 518 observations and 37 economies for 2010–2023")
print("Panel audit passed: 37 economies, 518 observations, 2010–2023.")

