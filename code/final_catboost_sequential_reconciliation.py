"""
Final CatBoost + sequential conformal reconciliation
====================================================

Purpose
-------
Reproduce the frozen CatBoost specification selected after diagnostic reconciliation,
while preserving:
- expanding-window model selection within 2010-2021;
- an untouched static final test evaluation on 2022-2023;
- separate sequential conformal prediction, where the model is refit through 2022
  before predicting 2023;
- SHAP analysis from the static 2010-2021 final model on the untouched 2022-2023 test set.

Run from the repository root:
    python code/final_catboost_sequential_reconciliation.py

Expected input:
    data/master_panel_final.csv

Outputs are written to:
    outputs/final_reconciliation/
"""

from pathlib import Path
import json
import math

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import shap

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "master_panel_final.csv"
OUT = ROOT / "outputs" / "final_reconciliation"
OUT.mkdir(parents=True, exist_ok=True)

COUNTRIES = [
    "Australia", "Austria", "Belgium", "Canada", "Chile", "Colombia",
    "Costa Rica", "Czech Republic", "Denmark", "Estonia", "Finland",
    "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
    "Israel", "Italy", "Japan", "Korea", "Latvia", "Lithuania",
    "Luxembourg", "Mexico", "Netherlands", "New Zealand", "Norway",
    "Portugal", "Slovak Republic", "Slovenia", "Spain", "Sweden",
    "Switzerland", "Türkiye", "United Kingdom", "United States"
]

FEATURES = ["Pop65", "Dependency", "GDP_pc", "Year", "Emerging"]
TARGET = "HealthExp_GDP"
VALIDATION_YEARS = [2017, 2018, 2019, 2020, 2021]
ALPHA = 0.10

CATBOOST_PARAMS = dict(
    iterations=500,
    learning_rate=0.10,
    depth=8,
    l2_leaf_reg=5,
    loss_function="RMSE",
    random_seed=42,
    thread_count=1,
    boosting_type="Plain",
    allow_writing_files=False,
    verbose=False,
)

def smape(y_true, y_pred):
    y_true = np.asarray(y_true, float)
    y_pred = np.asarray(y_pred, float)
    denom = np.abs(y_true) + np.abs(y_pred)
    mask = denom > 0
    return 100.0 * np.mean(2.0 * np.abs(y_true[mask] - y_pred[mask]) / denom[mask])

def metrics(y_true, y_pred):
    return {
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "sMAPE_pct": float(smape(y_true, y_pred)),
        "R2": float(r2_score(y_true, y_pred)),
    }

def finite_sample_higher_quantile(scores, alpha=0.10):
    """
    Split-conformal finite-sample quantile:
        rank = ceil((n+1)*(1-alpha))
    using the corresponding order statistic ("higher" convention).
    """
    scores = np.sort(np.asarray(scores, float))
    n = len(scores)
    rank = min(n, max(1, math.ceil((n + 1) * (1 - alpha))))
    return float(scores[rank - 1]), int(rank)

def fit_model(train):
    model = CatBoostRegressor(**CATBOOST_PARAMS)
    model.fit(train[FEATURES], train[TARGET])
    return model

# ---------------------------------------------------------------------
# 1. Load and validate the exact analytical panel
# ---------------------------------------------------------------------
df = pd.read_csv(DATA)
df = df[df["Country"].isin(COUNTRIES) & df["Year"].between(2010, 2023)].copy()

if "Economy_Group" not in df.columns:
    raise ValueError("Economy_Group is required in master_panel_final.csv")

df["Emerging"] = (df["Economy_Group"].astype(str) == "Emerging economy").astype(int)
df = df.sort_values(["Year", "Country"]).reset_index(drop=True)

required = ["Country", "Year", TARGET, "Pop65", "Dependency", "GDP_pc", "Economy_Group"]
missing_cols = [c for c in required if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

if len(df) != 518:
    raise ValueError(f"Expected 518 rows; found {len(df)}")
if df["Country"].nunique() != 37:
    raise ValueError(f"Expected 37 economies; found {df['Country'].nunique()}")
if df[[TARGET, "Pop65", "Dependency", "GDP_pc"]].isna().any().any():
    raise ValueError("Core variables contain missing values; reconciliation stopped.")

# ---------------------------------------------------------------------
# 2. Expanding-window validation, 2017-2021
# ---------------------------------------------------------------------
fold_rows = []
validation_predictions = []

for val_year in VALIDATION_YEARS:
    train = df[(df["Year"] >= 2010) & (df["Year"] < val_year)].copy()
    val = df[df["Year"] == val_year].copy()

    model = fit_model(train)
    pred = model.predict(val[FEATURES])
    m = metrics(val[TARGET], pred)

    fold_rows.append({
        "Validation_Year": val_year,
        "Train_N": len(train),
        "Validation_N": len(val),
        **m
    })

    tmp = val[["Country", "Year", "Economy_Group", TARGET]].copy()
    tmp["Prediction"] = pred
    tmp["Absolute_Error"] = np.abs(tmp[TARGET] - tmp["Prediction"])
    validation_predictions.append(tmp)

fold_df = pd.DataFrame(fold_rows)
val_pred_df = pd.concat(validation_predictions, ignore_index=True)
mean_validation_rmse = float(fold_df["RMSE"].mean())
rmse_sd = float(fold_df["RMSE"].std(ddof=1))

# ---------------------------------------------------------------------
# 3. Static untouched final-test evaluation, 2022-2023
#    This is the performance estimate used for the final predictive model.
# ---------------------------------------------------------------------
development = df[df["Year"].between(2010, 2021)].copy()
test_static = df[df["Year"].between(2022, 2023)].copy()

static_model = fit_model(development)
static_pred = static_model.predict(test_static[FEATURES])
static_metrics = metrics(test_static[TARGET], static_pred)

static_test_df = test_static[["Country", "Year", "Economy_Group", TARGET]].copy()
static_test_df["Prediction"] = static_pred
static_test_df["Absolute_Error"] = np.abs(static_test_df[TARGET] - static_test_df["Prediction"])

# ---------------------------------------------------------------------
# 4. Sequential conformal prediction
#    2022: use 2017-2021 expanding-window residuals.
#    2023: refit model through 2022 and update calibration with 2022 errors.
# ---------------------------------------------------------------------
calibration_scores = val_pred_df["Absolute_Error"].to_numpy()
q_2022, rank_2022 = finite_sample_higher_quantile(calibration_scores, ALPHA)

test_2022 = df[df["Year"] == 2022].copy()
pred_2022 = static_model.predict(test_2022[FEATURES])
err_2022 = np.abs(test_2022[TARGET].to_numpy() - pred_2022)
lo_2022 = pred_2022 - q_2022
hi_2022 = pred_2022 + q_2022
covered_2022 = (test_2022[TARGET].to_numpy() >= lo_2022) & (test_2022[TARGET].to_numpy() <= hi_2022)

# Refit through 2022 before predicting 2023
development_2022 = df[df["Year"].between(2010, 2022)].copy()
model_2023 = fit_model(development_2022)

# Sequentially update the calibration score pool with realized 2022 errors
calibration_scores_2023 = np.concatenate([calibration_scores, err_2022])
q_2023, rank_2023 = finite_sample_higher_quantile(calibration_scores_2023, ALPHA)

test_2023 = df[df["Year"] == 2023].copy()
pred_2023 = model_2023.predict(test_2023[FEATURES])
err_2023 = np.abs(test_2023[TARGET].to_numpy() - pred_2023)
lo_2023 = pred_2023 - q_2023
hi_2023 = pred_2023 + q_2023
covered_2023 = (test_2023[TARGET].to_numpy() >= lo_2023) & (test_2023[TARGET].to_numpy() <= hi_2023)

conformal_2022 = test_2022[["Country", "Year", "Economy_Group", TARGET]].copy()
conformal_2022["Prediction"] = pred_2022
conformal_2022["Lower_90"] = lo_2022
conformal_2022["Upper_90"] = hi_2022
conformal_2022["Covered"] = covered_2022
conformal_2022["Calibration_q"] = q_2022
conformal_2022["Calibration_N"] = len(calibration_scores)

conformal_2023 = test_2023[["Country", "Year", "Economy_Group", TARGET]].copy()
conformal_2023["Prediction"] = pred_2023
conformal_2023["Lower_90"] = lo_2023
conformal_2023["Upper_90"] = hi_2023
conformal_2023["Covered"] = covered_2023
conformal_2023["Calibration_q"] = q_2023
conformal_2023["Calibration_N"] = len(calibration_scores_2023)

conformal_df = pd.concat([conformal_2022, conformal_2023], ignore_index=True)

coverage_2022 = float(covered_2022.mean())
coverage_2023 = float(covered_2023.mean())
coverage_overall = float(conformal_df["Covered"].mean())

group_coverage = (
    conformal_df.groupby("Economy_Group")["Covered"]
    .mean()
    .rename("Coverage")
    .reset_index()
)

# ---------------------------------------------------------------------
# 5. SHAP from the static final model on the untouched 2022-2023 test set
# ---------------------------------------------------------------------
explainer = shap.TreeExplainer(static_model)
shap_values = explainer.shap_values(test_static[FEATURES])
shap_values = np.asarray(shap_values)

mean_abs_shap = np.abs(shap_values).mean(axis=0)
shap_global = pd.DataFrame({
    "Feature": FEATURES,
    "Mean_Absolute_SHAP": mean_abs_shap,
})
shap_global["Share_of_Total"] = (
    shap_global["Mean_Absolute_SHAP"] / shap_global["Mean_Absolute_SHAP"].sum()
)
shap_global = shap_global.sort_values("Mean_Absolute_SHAP", ascending=False).reset_index(drop=True)

# Exact SHAP reconciliation check
expected_value = np.asarray(explainer.expected_value).reshape(-1)[0]
reconstructed = expected_value + shap_values.sum(axis=1)
reconciliation_error = float(np.max(np.abs(reconstructed - static_pred)))

# ---------------------------------------------------------------------
# 6. Save outputs
# ---------------------------------------------------------------------
fold_df.to_csv(OUT / "catboost_fold_metrics.csv", index=False)
val_pred_df.to_csv(OUT / "catboost_validation_predictions.csv", index=False)
static_test_df.to_csv(OUT / "catboost_static_test_predictions.csv", index=False)
conformal_df.to_csv(OUT / "sequential_conformal_intervals.csv", index=False)
group_coverage.to_csv(OUT / "sequential_conformal_group_coverage.csv", index=False)
shap_global.to_csv(OUT / "shap_global_static_test.csv", index=False)

summary = {
    "frozen_specification": "F_Plain_documented_only",
    "catboost_parameters": CATBOOST_PARAMS,
    "development_period": "2010-2021",
    "validation_years": VALIDATION_YEARS,
    "mean_validation_RMSE": mean_validation_rmse,
    "validation_RMSE_SD": rmse_sd,
    "static_test_period": "2022-2023",
    "static_test_metrics": static_metrics,
    "conformal": {
        "nominal_coverage": 0.90,
        "q_2022": q_2022,
        "q_2022_rank": rank_2022,
        "coverage_2022": coverage_2022,
        "q_2023": q_2023,
        "q_2023_rank": rank_2023,
        "coverage_2023": coverage_2023,
        "overall_coverage": coverage_overall,
        "group_coverage": group_coverage.to_dict(orient="records"),
    },
    "shap_global": shap_global.to_dict(orient="records"),
    "shap_max_reconciliation_error": reconciliation_error,
}
with open(OUT / "final_reconciliation_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(json.dumps(summary, indent=2, ensure_ascii=False))
print(f"\nSaved outputs to: {OUT}")
