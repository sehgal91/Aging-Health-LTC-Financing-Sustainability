# Data Processing

## Harmonization

Source tables are harmonized to a common country-year structure. Processing includes standardizing country names and years, removing aggregate/non-country records, checking units and numeric plausibility, screening duplicate country-year entries, and merging indicators on country and year.

## Analytical sample

The study sample contains 37 economies observed from 2010 through 2023. `code/build_analytical_panel.py` applies the country/year filter to the harmonized master table and verifies:

- 518 country-year observations;
- 37 unique economies;
- complete `HealthExp_GDP`, `Pop65`, `Dependency`, and `GDP_pc` values; and
- no duplicate country-year records.

## Missing data

The four core variables require no interpolation or grouped imputation in the analytical sample. Government-financing and LTC-workforce variables remain missing where unavailable. Analyses involving these variables are restricted to observed country-years.

## Derived variables

The repository distinguishes observed variables from deterministic derived indicators:

- `Public_Exposure`: health expenditure burden combined with government financing share;
- `FPI`: health expenditure burden combined with total age dependency;
- `Worker_Ratio`: LTC workforce relative to the older population;
- `Affordability`: GDP per capita relative to health expenditure burden.

These derived variables are not used as independent core predictors when they are mathematically constructed from the same underlying variables.

## Temporal evaluation

Predictive development uses 2010–2021. Validation is strictly chronological over 2017–2021. The 2022–2023 period is reserved for independent evaluation. Sequential conformal prediction calibrates 2022 from prior validation errors and updates the conformity-score pool only after 2022 outcomes become available before constructing 2023 intervals.

## Scenario analysis

Scenario trajectories are anchored to observed 2023 health expenditure burden and extend through 2028. They manipulate demographic and GDP trends only and are evaluated against persistence using rolling-origin backtests. The outputs are interpreted as sensitivity paths rather than unconditional forecasts.
