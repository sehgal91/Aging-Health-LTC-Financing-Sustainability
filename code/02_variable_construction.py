"""Reconstruct deterministic indicators when their parent columns are available."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data" / "master_panel_final.csv"
out = ROOT / "data" / "processed" / "master_panel_with_indicators.csv"
df = pd.read_csv(src)
definitions = {
    "Public_Exposure": ("HealthExp_GDP", "Gov_Share", "mul"),
    "FPI": ("HealthExp_GDP", "Dependency", "mul"),
    "Worker_Ratio": ("LTC_Workers", "Pop65", "div"),
    "Affordability": ("GDP_pc", "HealthExp_GDP", "div"),
}
for name, (a, b, operation) in definitions.items():
    if a in df and b in df:
        df[name] = df[a] * df[b] if operation == "mul" else df[a] / df[b].replace(0, pd.NA)
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(f"Wrote {out.relative_to(ROOT)}; restricted-coverage indicators retain missing values.")

