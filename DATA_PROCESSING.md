# Data Processing and Analytical Splits

The final analytical frame is a 37-economy panel covering 2010–2023 (518 country-year observations).

Processing checks comprise country-name and year harmonization, exclusion of aggregate records, numeric plausibility checks, duplicate country-year detection, country-year merges, and verification of the final panel keys and period.

The complete-coverage core analysis uses health expenditure burden, population aged 65+, old-age dependency ratio, GDP per capita, year, and economy group. Government-financing and LTC-workforce measures remain missing where unavailable and are not imputed into the 518-observation core panel.

Derived variables are:

- `Public_Exposure = HealthExp_GDP × Gov_Share` (restricted-sample public financing exposure);
- `FPI = HealthExp_GDP × Dependency` (descriptive Fiscal Pressure Index);
- `Worker_Ratio = LTC_Workers / Pop65` (restricted-sample workforce ratio);
- `Affordability = GDP_pc / HealthExp_GDP` (descriptive affordability transformation).

Predictive evaluation is time ordered. Data through 2021 are used for model development and validation; 2022–2023 form an untouched test set. The test set is not used for model selection or tuning.

The 2024–2028 scenario component uses an anchored log-linear specification separately from CatBoost. Its outputs are sensitivity trajectories rather than forecasts.

