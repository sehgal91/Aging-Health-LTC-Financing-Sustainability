# Data Sources and Variable Scope

The repository contains harmonized country-year indicators for health expenditure as a percentage of GDP, population aged 65+, old-age dependency, GDP per capita, government/public financing share, and LTC workforce capacity.

The primary outcome is **health expenditure burden**, not direct LTC expenditure.

Core analytical coverage:
- 37 economies
- 2010–2023
- 518 country-year observations
- complete `HealthExp_GDP`, `Pop65`, `Dependency`, and `GDP_pc`

Restricted supplementary coverage:
- `Gov_Share`: 41 observations from 3 countries
- `LTC_Workers`: 58 observations from 16 countries

Missing government-financing and LTC-workforce observations are retained as missing and are not imputed to create full-panel predictors.

Derived indicators such as `Public_Exposure`, `FPI`, `Worker_Ratio`, and `Affordability` are deterministic transformations used for descriptive, restricted-sample, or sensitivity purposes and are not independent measures of fiscal sustainability.
