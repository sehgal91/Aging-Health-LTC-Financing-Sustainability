# Data Processing and Analytical Splits

The final analytical frame is a 37-economy panel covering 2010–2023 (518 country-year observations).

Processing includes country-name and year harmonization, exclusion of aggregate records, numeric plausibility checks, duplicate country-year screening, country-year merging, and final panel-key verification.

The complete-coverage core analysis uses `HealthExp_GDP`, `Pop65`, `Dependency`, and `GDP_pc`. Government-financing and LTC-workforce measures remain missing where unavailable and are not imputed into the core panel.

Derived variables include:

- `Public_Exposure`: health expenditure burden combined with observed government financing share;
- `FPI = HealthExp_GDP × Dependency`;
- `Worker_Ratio = LTC_Workers / Pop65`;
- `Affordability = GDP_pc / HealthExp_GDP`.

Predictive evaluation is strictly time ordered:
- development period: 2010–2021;
- expanding-window validation years: 2017–2021;
- independent final test period: 2022–2023.

The final CatBoost model is selected using development-period validation only. The final test period is excluded from model-family and hyperparameter selection.

Sequential conformal prediction uses 2017–2021 validation residuals for the 2022 interval. After 2022 outcomes become available, the model is refitted through 2022 and the calibration pool is updated before predicting 2023.

The 2024–2028 scenario component is modeled separately from CatBoost using an anchored log-linear within-country specification. Scenario outputs are sensitivity trajectories rather than validated forecasts.
