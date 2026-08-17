# Health Expenditure Burden Across 37 Economies

This repository contains the analytical data, reproducibility documentation, scripts, and supporting outputs for the study **“Health Expenditure Burden Across 37 Economies: Panel Econometrics, Explainable Machine Learning, and Scenario Sensitivity Analysis.”**

The primary outcome is total health expenditure as a percentage of GDP, interpreted as **health expenditure burden**. It is not direct long-term-care (LTC) expenditure and does not by itself establish LTC financing or fiscal sustainability.

## Final analytical design

- Panel: 37 economies, 2010–2023, 518 country-year observations.
- Economy groups: 32 high-income economies and 5 emerging economies.
- Complete core variables: health expenditure burden, population aged 65 years and above, old-age dependency ratio, and GDP per capita.
- Restricted supplementary variables: government financing share (41 observations, 3 countries) and LTC workforce capacity (58 observations, 16 countries). These variables are not imputed to create full-panel predictors.
- Predictive development period: 2010–2021 (N = 444).
- Expanding-window validation years: 2017–2021.
- Independent final test period: 2022–2023 (N = 74).

## Econometric framework

The principal analysis uses pooled, fixed-effects, and random-effects log-log panel models with year effects and country-clustered inference. Within-between decomposition distinguishes persistent cross-country differences from within-country changes over time.

## Predictive framework

CatBoost was selected using development-period expanding-window validation only. The final selected configuration was:

- iterations = 500
- learning_rate = 0.10
- depth = 8
- l2_leaf_reg = 5
- loss = RMSE
- random_seed = 42
- boosting_type = Plain

Final predictive results:

- mean expanding-window validation RMSE = 1.238
- independent 2022–2023 test RMSE = 1.692
- test MAE = 1.187
- test sMAPE = 13.022%
- test R² = 0.470

## Explainability

Global SHAP importance on the 74 independent 2022–2023 test observations:

| Predictor | Mean absolute SHAP | Share |
|---|---:|---:|
| GDP per capita | 0.843 | 36.1% |
| Population aged 65+ | 0.604 | 25.8% |
| Year | 0.482 | 20.6% |
| Old-age dependency ratio | 0.309 | 13.2% |
| Economy-group indicator | 0.098 | 4.2% |

The strongest reported pairwise SHAP interaction is population aged 65+ × GDP per capita, with mean absolute interaction ≈ 0.197. SHAP values describe predictive contributions and are not causal effects.

## Sequential conformal prediction

For nominal 90% intervals:

- 2022: calibration quantile = 1.821, empirical coverage = 86.5%, total interval width = 3.643 percentage points
- 2023: calibration quantile = 1.897, empirical coverage = 89.2%, total interval width = 3.794 percentage points
- overall 2022–2023 coverage = 87.8%
- high-income coverage = 85.9%
- emerging-economy coverage = 100.0% (N = 10)

These values are interpreted as empirical calibration because temporal and cross-country dependence weaken standard exchangeability assumptions.

## Scenario sensitivity

The scenario component is separate from the CatBoost prediction model. It examines anchored 2024–2028 sensitivity trajectories under alternative demographic and GDP-growth assumptions. Rolling-origin backtesting did not systematically outperform persistence, and some projected predictor values extend beyond historical support. The scenario outputs are therefore interpreted as sensitivity trajectories rather than validated forecasts or causal policy effects.

## Repository map

| Path | Contents |
|---|---|
| `data/` | Cleaned inputs, analytical panel, and data dictionary |
| `code/` | Data-integrity, variable-construction, analysis, and output-audit scripts |
| `outputs/tables/` | Numerical outputs aligned to the manuscript and Supplementary Materials |
| `docs/` | Supplementary and supporting documentation |
| `DATA_SOURCES.md` | Variable scope and coverage |
| `DATA_PROCESSING.md` | Panel construction and time-ordering rules |
| `REPRODUCIBILITY.md` | Reproduction instructions and evidence boundaries |

## Interpretation boundaries

Government-financing and LTC-workforce variables remain supplementary restricted-sample evidence. Public financing exposure, the Fiscal Pressure Index, workforce adequacy ratio, and affordability ratio are deterministic derived indicators and are not independent measures of fiscal sustainability. Direct LTC or fiscal-sustainability assessment would require harmonized LTC-specific expenditure, financing or revenue capacity, financing-gap information, institutional characteristics, and an explicit sustainability benchmark.
