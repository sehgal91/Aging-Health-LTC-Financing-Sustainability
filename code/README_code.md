# Code scope

The repository contains archive-integrity checks, deterministic variable-construction scripts, reported-output checks, and the final CatBoost/sequential-conformal reconciliation workflow.

- `00_run_all.py` runs the archive-consistency checks.
- `01_data_cleaning_and_merging.py` verifies the 2010–2023 panel keys and dimensions.
- `02_variable_construction.py` reconstructs deterministic indicators while retaining restricted-sample missingness.
- `03_reported_output_tables.py` verifies reported headline summaries.
- `final_catboost_sequential_reconciliation.py` reproduces the frozen CatBoost specification, expanding-window validation, independent 2022–2023 test evaluation, sequential conformal updating, and final SHAP analysis.

Exact trial-by-trial hyperparameter-search histories are not claimed where corresponding logs are unavailable.
