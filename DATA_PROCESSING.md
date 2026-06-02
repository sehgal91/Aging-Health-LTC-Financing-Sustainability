# Data Sources and Variable Interpretation

This repository uses publicly available international country-year datasets. The cleaned files in `data/raw_cleaned/` were prepared from the following original data sources.

## Original data sources

| Dataset/domain | Source organization | Original source link | Variables used in this study |
|---|---|---|---|
| Health expenditure burden | World Health Organization Global Health Expenditure Database / World Bank health expenditure indicators | https://apps.who.int/nha/database and https://data.worldbank.org/indicator/SH.XPD.CHEX.GD.ZS | Health expenditure as a percentage of GDP |
| GDP per capita | World Bank World Development Indicators | https://data.worldbank.org/indicator/NY.GDP.PCAP.CD | GDP per capita |
| Population aged 65+ | World Bank World Development Indicators / UN World Population Prospects | https://data.worldbank.org/indicator/SP.POP.65UP.TO.ZS and https://population.un.org/wpp/ | Population aged 65 years and above |
| Old-age dependency ratio | World Bank World Development Indicators | https://data.worldbank.org/indicator/SP.POP.DPND.OL | Old-age dependency ratio |
| Government/public financing share | OECD Health Statistics / OECD Health at a Glance | https://www.oecd.org/health/health-data.htm and https://www.oecd.org/health/health-at-a-glance/ | Government/public financing share |
| Long-term care workforce | OECD Health Statistics / OECD long-term care indicators | https://www.oecd.org/health/health-data.htm | Long-term care workforce capacity |

## Variable interpretation

The primary expenditure variable is **health expenditure burden**, measured as health expenditure as a percentage of gross domestic product. It is interpreted as a broad system-level indicator of aging-related health and care-financing pressure, not as a direct measure of formal long-term care expenditure alone.

Long-term care-specific public financing and workforce indicators are treated as supplementary variables because they have limited and uneven country-year coverage.

## Processed repository files

The cleaned input files are stored in:

```text
data/raw_cleaned/
