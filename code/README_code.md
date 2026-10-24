# Code

## `build_analytical_panel.py`
Creates the 37-economy, 2010–2023 analytical panel from the harmonized master table and validates the expected panel dimensions and complete coverage of the four core variables.

Run from the repository root:

```bash
python code/build_analytical_panel.py
```

## `catboost_sequential_conformal.py`
Runs the fixed CatBoost configuration used for nonlinear comparison, expanding-window validation, independent 2022–2023 test evaluation, SHAP analysis, and sequential conformal prediction.

Run from the repository root:

```bash
python code/catboost_sequential_conformal.py
```

Machine-readable reported results for the econometric, robustness, benchmark, conformal, and scenario analyses are provided in `outputs/tables/`.
