# Reproducibility and Evidence Boundaries

## Environment

Install the packages in `requirements.txt`, then run `python code/00_run_all.py` from the repository root. The scripts audit the archived panel, reconstruct deterministic derived variables where their parent fields are present, and check the reported CSV outputs.

## Reproducible from this archive

- panel-key, date-range, and duplicate checks;
- deterministic derived-variable construction;
- consistency checks for the final sample and split definitions;
- validation/test metric, SHAP-summary, conformal-summary, and scenario-table audits.

## Reported rather than recomputed here

The repository does not assert exact hyperparameter-search settings, pruning rules, random-search seeds, or sequential conformal recalibration values unless they are present in verified computational artifacts. The final reported facts are CatBoost validation RMSE 1.238; untouched 2022–2023 test RMSE 1.692 and R² 0.470; mean absolute SHAP summaries in Table S19; final-period aggregate conformal coverage of 90.5% for a nominal 90% procedure; and anchored 2024–2028 scenario sensitivity trajectories.

The scenario model did not systematically outperform persistence at one-, three-, or five-year horizons. Accordingly, its trajectories are not presented as validated forecasts.

