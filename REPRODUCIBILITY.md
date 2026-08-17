# Reproducibility and Evidence Boundaries

## Environment

Install the packages in `requirements.txt`.

## Analytical panel

The final analytical sample contains 518 observations from 37 economies over 2010–2023. Core variables `HealthExp_GDP`, `Pop65`, `Dependency`, and `GDP_pc` are complete across the analytical panel. `Gov_Share` and `LTC_Workers` are supplementary restricted-coverage variables and are not imputed to create full-panel predictors.

## Predictive workflow

Model development uses 2010–2021 data. Expanding-window validation uses 2017–2021 as sequential validation years, with each model trained only on earlier observations. The 2022–2023 period is reserved for independent final evaluation.

Final CatBoost configuration:

```text
iterations = 500
learning_rate = 0.10
depth = 8
l2_leaf_reg = 5
loss_function = RMSE
random_seed = 42
thread_count = 1
boosting_type = Plain
```

Expected rounded results:

```text
mean validation RMSE = 1.238
test RMSE = 1.692
test MAE = 1.187
test sMAPE = 13.022%
test R² = 0.470
```

## Explainability

Final independent-test global SHAP values:

```text
GDP per capita        0.843 (36.1%)
Population aged 65+   0.604 (25.8%)
Year                   0.482 (20.6%)
Dependency ratio       0.309 (13.2%)
Economy group          0.098 (4.2%)
```

The strongest reported pairwise SHAP interaction is population aged 65+ × GDP per capita (mean absolute interaction ≈ 0.197).

## Sequential conformal prediction

Absolute residuals from expanding-window validation for 2017–2021 (N = 185) form the initial conformity-score pool.

```text
2022 q = 1.821
2022 empirical coverage = 86.5%
2022 total interval width = 3.643

After refitting through 2022 and appending the 37 realized 2022 absolute errors:
calibration pool N = 222

2023 q = 1.897
2023 empirical coverage = 89.2%
2023 total interval width = 3.794

overall 2022–2023 coverage = 87.8%
high-income coverage = 85.9%
emerging-economy coverage = 100.0% (N = 10)
```

Coverage is interpreted empirically because temporal and cross-country dependence weaken standard exchangeability assumptions.

## Hyperparameter documentation

Supplementary Tables S14–S18 document search spaces and development-period tuning frameworks. Exact trial-by-trial Optuna counts, random-search seeds, pruning parameters, or tuning-convergence histories are not asserted where corresponding logs are unavailable.

## Scenario sensitivity

The 2024–2028 scenario analysis is separate from CatBoost. It uses an anchored log-linear within-country specification, rolling-origin backtesting, and predictor-support checks. It should not be interpreted as a validated long-term forecast or causal policy-effect model.

## Interpretation boundary

The primary outcome is total health expenditure as a percentage of GDP, not direct LTC expenditure. Direct LTC fiscal-sustainability analysis would require harmonized LTC-specific expenditure, financing capacity, financing-gap information, institutional data, and an explicit sustainability benchmark.
