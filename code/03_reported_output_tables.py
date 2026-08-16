"""Check that archived headline results match the final manuscript specification."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
tables = ROOT / "outputs" / "tables"
model = pd.read_csv(tables / "table9_model_selection_and_test.csv")
expected = {"Validation RMSE": 1.238, "Test RMSE": 1.692, "Test R²": 0.470}
for metric, value in expected.items():
    actual = float(model.loc[model["Metric"] == metric, "Value"].iloc[0])
    if abs(actual - value) > 1e-12:
        raise ValueError(f"{metric} differs from final reported value")
conformal = pd.read_csv(tables / "sm_table_s20_sequential_conformal.csv")
if float(conformal.loc[0, "Nominal coverage (%)"]) != 90 or float(conformal.loc[0, "Observed final-period aggregate coverage (%)"]) != 90.5:
    raise ValueError("Conformal coverage summary differs from final report")
scenario = pd.read_csv(tables / "table10_scenario_sensitivity_summary.csv")
if set(scenario["Period"]) != {"2024–2028"}:
    raise ValueError("Scenario period must be 2024–2028")
print("Reported-output audit passed.")

