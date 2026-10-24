# Data Sources

## Core variables

### Health expenditure burden (`HealthExp_GDP`)
Current health expenditure as a percentage of GDP. World Bank World Development Indicators code `SH.XPD.CHEX.GD.ZS`, sourced from the WHO Global Health Expenditure Database. The variable measures total health-system expenditure relative to national economic output and is not direct long-term-care expenditure.

### Population aged 65 years and above (`Pop65`)
Population aged 65 years and above as a percentage of total population. World Bank WDI code `SP.POP.65UP.TO.ZS` (UN Population Division source).

### Total age dependency ratio (`Dependency`)
Dependents aged 0–14 and 65 years and above relative to the working-age population aged 15–64 years. World Bank WDI code `SP.POP.DPND`.

### GDP per capita (`GDP_pc`)
Benchmark series: GDP per capita in current US dollars, World Bank WDI code `NY.GDP.PCAP.CD`.

Robustness series: GDP per capita at purchasing-power parity in constant 2021 international dollars, World Bank WDI code `NY.GDP.PCAP.PP.KD`.

## Supplementary restricted-coverage variables

### Government financing share (`Gov_Share`)
Public/government share of health financing in the archived source data. Coverage is 41 country-year observations from 3 countries. Missing values are not imputed to create a full-panel predictor.

### Long-term-care workforce (`LTC_Workers`)
Formal LTC workforce availability as reported in the archived source data. The source-specific measure has 58 country-year observations from 16 countries. Missing values are not imputed to create a full-panel predictor.

## Derived indicators

`Public_Exposure`, `FPI`, `Worker_Ratio`, and `Affordability` are deterministic transformations of observed variables. They are used only for descriptive, restricted-sample, or sensitivity analysis and are not interpreted as independent measures of LTC financing sustainability or fiscal solvency.

## Analytical coverage

The complete core panel contains 518 observations from 37 economies during 2010–2023. The four core variables have complete coverage in this analytical sample.
