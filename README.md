# Health Expenditure Burden under Population Aging

This repository archives the data, documentation, and reported outputs for a 37-economy country-year study of **health expenditure as a percentage of GDP**. The outcome is a broad health-system expenditure-burden measure; it is not direct long-term-care (LTC) expenditure and does not establish LTC financing or fiscal sustainability.

## Final analytical design

- Panel: 37 economies, 2010–2023 (518 country-year observations).
- Core variables: health expenditure burden, population aged 65+, old-age dependency ratio, GDP per capita, year, and economy group.
- Supplementary variables: government financing share and LTC workforce capacity, used only where observed because coverage is restricted.
- Time split: model development through 2021; 2022–2023 retained as an untouched test period.
- Model selection: CatBoost selected on validation RMSE (1.238), before test evaluation.
- Untouched-test performance: RMSE 1.692 and R² 0.470.
- Explainability: mean absolute SHAP values are archived in `outputs/tables/sm_table_s19_feature_importance.csv`.
- Uncertainty: sequential conformal prediction targets 90% coverage; the observed final-period aggregate coverage reported in the manuscript is 90.5%. Unverified recalibration half-widths are not asserted here.
- Scenarios: anchored 2024–2028 sensitivity trajectories, not validated forecasts.

## Repository map

| Path | Contents |
|---|---|
| `data/` | Cleaned inputs, analytical panel, and data dictionary |
| `code/` | Data-integrity, derived-variable, and reported-output audit scripts |
| `outputs/tables/` | CSV tables aligned to the final manuscript framing |
| `docs/` | Supplementary-material documentation |
| `DATA_SOURCES.md` | Variable scope and coverage |
| `DATA_PROCESSING.md` | Panel-construction and leakage-control rules |
| `REPRODUCIBILITY.md` | What can and cannot be reproduced from the archive |

## Interpretation boundary

Government-financing and LTC-workforce variables are supplementary restricted-sample evidence. The Fiscal Pressure Index and affordability measure are deterministic transformations used descriptively and in sensitivity analysis; they are not independent evidence of fiscal sustainability. Direct sustainability assessment would require expenditure obligations, financing or revenue capacity, a financing gap, and an explicit benchmark.

