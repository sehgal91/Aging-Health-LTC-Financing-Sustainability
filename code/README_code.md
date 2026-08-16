# Code scope

These scripts perform archive-integrity and consistency checks. They do not claim to recreate model searches whose exact settings, pruning rules, seeds, or recalibration sequence are not available in verified artifacts.

- `00_run_all.py` runs all checks.
- `01_data_cleaning_and_merging.py` verifies the 2010–2023 panel keys and dimensions.
- `02_variable_construction.py` reconstructs deterministic indicators while retaining restricted-sample missingness.
- `03_reported_output_tables.py` verifies the final headline model, conformal, and scenario summaries.

