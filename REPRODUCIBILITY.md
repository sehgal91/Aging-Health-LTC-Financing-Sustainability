# Reproducibility

## Environment

Install the Python dependencies listed in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

## Analytical sample

The study uses 37 economies observed annually from 2010 through 2023, yielding 518 country-year observations. The country list is embedded in `code/build_analytical_panel.py` and `code/catboost_sequential_conformal.py`.

The four complete-coverage core variables are:

- `HealthExp_GDP`
- `Pop65`
- `Dependency`
- `GDP_pc`

No interpolation or grouped imputation is applied to these four variables. `Gov_Share` and `LTC_Workers` remain missing where unavailable and are used only in restricted-sample supplementary analyses.

## Data preparation

The repository retains the harmonized source/master table in `data/master_panel_final.csv`. This file may contain observations outside the 37-economy analytical sample. Generate the study panel with:

```bash
python code/build_analytical_panel.py
```

The script filters the 37 named economies and years 2010–2023, checks the expected 518 observations and 37 unique economies, verifies complete coverage of the four core variables, and writes `data/analytical_panel_37_economies.csv`.

## Econometric results

Machine-readable econometric outputs are provided in `outputs/tables/`. These include pooled, fixed-effects, and random-effects estimates; within-between elasticities; constant-PPP GDP robustness; Mundlak testing; Pesaran cross-sectional dependence; and Driscoll-Kraay sensitivity inference.

The principal fixed-effects coefficients are 0.030 for population aged 65+, 0.197 for total age dependency, and -0.143 for GDP per capita. The corresponding Driscoll-Kraay sensitivity standard errors are 0.043, 0.110, and 0.022.

## Predictive evaluation

The development period is 2010–2021. Expanding-window validation uses 2017–2021 as sequential validation years. The independent test period is 2022–2023.

The strongest benchmarks are one-step persistence and a country-fixed-effects linear model. Mean validation RMSE is 0.412 for persistence, 0.764 for the country-fixed-effects benchmark, and 1.238 for CatBoost. On the independent test period, RMSE is 0.660, 0.726, and 1.692, respectively.

The CatBoost configuration is:

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

The CatBoost/sequential-conformal workflow can be run with:

```bash
python code/catboost_sequential_conformal.py
```

## SHAP interpretation

Global CatBoost SHAP importance on the 2022–2023 test observations is reported in `sm_table_s19_feature_importance.csv`. Mean absolute SHAP values are 0.843 for GDP per capita, 0.604 for population aged 65+, 0.482 for year, 0.309 for total age dependency ratio, and 0.098 for economy group. SHAP is interpreted as model-behavior description rather than causal evidence.

## Sequential conformal prediction

CatBoost empirical coverage is 86.5% in 2022 and 89.2% in 2023, with half-widths 1.821 and 1.897 percentage points. Persistence-based intervals yield 75.7% and 94.6% coverage with half-widths 0.924 and 0.986. The interval comparison is summarized in `sm_table_s20_sequential_conformal.csv`.

## Scenario sensitivity

The anchored scenario analysis covers 2024–2028. It is evaluated using rolling-origin backtests at one-, three-, and five-year horizons. Scenario-model RMSEs are 0.494, 0.899, and 0.968, compared with persistence RMSEs 0.479, 0.862, and 0.950. The scenario outputs are therefore interpreted as sensitivity paths, not validated forecasts.
