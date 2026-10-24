# Health Expenditure Burden Across 37 Economies

This repository accompanies the study **“Health Expenditure Burden Across 37 Economies: Panel Econometrics, Explainable Machine Learning, and Scenario Sensitivity Analysis.”**

## Study scope

The analysis covers 37 economies over 2010–2023 (518 country-year observations). The primary outcome is **health expenditure burden**, measured as current health expenditure as a percentage of GDP. The complete-coverage core predictors are population aged 65 years and above, total age dependency ratio, and GDP per capita. Government-financing and long-term-care workforce variables are used only as supplementary restricted-sample indicators because their country-year coverage is substantially smaller.

The main analytical components are:

- log-log pooled, fixed-effects, random-effects, and within-between panel analysis with country-clustered inference;
- constant-PPP GDP robustness analysis;
- cluster-robust Mundlak, Pesaran cross-sectional-dependence, and Driscoll-Kraay robustness checks;
- expanding-window predictive validation during 2017–2021;
- independent evaluation on 2022–2023;
- comparison with one-step persistence and country-fixed-effects predictive benchmarks;
- CatBoost-based SHAP interpretation as a secondary nonlinear diagnostic;
- sequential conformal prediction compared with a persistence-based interval benchmark; and
- anchored 2024–2028 scenario sensitivity analysis with rolling-origin backtesting.

## Core variables

| Variable | Definition | Source / indicator |
|---|---|---|
| `HealthExp_GDP` | Current health expenditure as % of GDP | World Bank WDI `SH.XPD.CHEX.GD.ZS`, sourced from the WHO Global Health Expenditure Database |
| `Pop65` | Population aged 65 years and above (% of total population) | World Bank WDI `SP.POP.65UP.TO.ZS` |
| `Dependency` | Total age dependency ratio (% of working-age population) | World Bank WDI `SP.POP.DPND` |
| `GDP_pc` | GDP per capita, current US$ | World Bank WDI `NY.GDP.PCAP.CD` |
| PPP robustness | GDP per capita, PPP, constant 2021 international $ | World Bank WDI `NY.GDP.PCAP.PP.KD` |

The total age dependency ratio includes dependents aged 0–14 and 65 years and above relative to the working-age population aged 15–64 years.

## Main numerical results

The fixed-effects aging elasticity is 0.030 and statistically imprecise. The within-country income elasticity of per-capita health expenditure is 0.857, compared with 1.141 between countries; the corresponding confidence intervals include unity. A cluster-robust Mundlak test rejects equality of within- and between-country relationships (Wald chi-square = 19.820, df = 3, p < 0.001), and the Pesaran CD test indicates residual cross-sectional dependence (CD = -2.240, p = 0.025).

For prediction, one-step persistence achieved mean expanding-window validation RMSE 0.412 and 2022–2023 test RMSE 0.660. The country-fixed-effects linear benchmark achieved validation RMSE 0.764 and test RMSE 0.726. CatBoost achieved validation RMSE 1.238 and test RMSE 1.692. CatBoost is therefore used as a nonlinear comparator rather than as the preferred predictive model.

CatBoost sequential conformal intervals achieved overall empirical coverage of 87.8% across 2022–2023. Persistence-based intervals achieved 85.1% overall coverage and were substantially narrower.

The 2024–2028 scenario analysis is interpreted as sensitivity analysis rather than validated forecasting. The modeled 2028 mean burden ranges from 9.437% to 9.510% of GDP across the specified pathways, while the five-year rolling-origin backtest RMSE is 0.968 percentage points.

## Repository structure

```text
README.md
REPRODUCIBILITY.md
DATA_SOURCES.md
DATA_PROCESSING.md
requirements.txt
code/
    README_code.md
    build_analytical_panel.py
    catboost_sequential_conformal.py
data/
    master_panel_final.csv
    master_panel_final.xlsx
    data_dictionary.xlsx
    *_standardized.csv
    raw_cleaned/
        README_raw_cleaned.md
outputs/
    tables/
        README_tables.md
        sm_table_s2_missing_data_summary.csv
        sm_table_s3_robustness_strategy.csv
        table5_descriptive_statistics.csv
        table6_groupwise_comparison.csv
        table7_econometric_results.csv
        table8_predictive_validation.csv
        table9_model_selection_and_test.csv
        table10_scenario_sensitivity_summary.csv
        sm_table_s7a_within_between.csv
        sm_table_s7b_ppp_robustness.csv
        sm_table_s8a_mundlak.csv
        sm_table_s8b_pesaran_cd.csv
        sm_table_s8c_driscoll_kraay.csv
        sm_table_s13_foldwise_validation.csv
        sm_table_s19_feature_importance.csv
        sm_table_s20_sequential_conformal.csv
        sm_table_s21a_scenario_backtest.csv
        sm_table_s21b_predictor_support.csv
        sm_table_s22_robustness_results.csv
        sm_table_s23_independent_test.csv
docs/
    Supplementary_Materials.pdf
```

## Interpretation boundaries

`HealthExp_GDP` is a measure of total health-system expenditure relative to national economic output. It is **not** direct long-term-care expenditure and is **not** a direct measure of fiscal solvency. Government-financing and LTC-workforce indicators have restricted coverage and are not generalized to the complete 37-economy panel. Derived indicators are deterministic transformations used for descriptive or sensitivity purposes and are not treated as independent measures of fiscal sustainability.
