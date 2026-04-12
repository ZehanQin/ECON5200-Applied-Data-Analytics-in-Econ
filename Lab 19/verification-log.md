# Verification Log — Lab 19: Random Forests

## P.R.I.M.E. Prompt Used

```
[Prep] Act as an expert Python Data Scientist specializing
in SHAP explanations, interactive visualizations, and
scikit-learn production workflows.

[Request] I just completed a diagnosis-first lab where I
compared Decision Trees, Ridge, Random Forests, and Gradient
Boosting on California Housing data. I fixed evaluation bugs,
diagnosed causal overclaiming from MDI, tuned hyperparameters
with GridSearchCV, and generated SHAP waterfall + beeswarm
plots. Now I need TWO artifacts:

1. A reusable src/shap_utils.py module with three functions:
   - explain_prediction(model, X, idx) -> SHAP waterfall
   - global_importance(model, X) -> SHAP beeswarm
   - compare_importance(model, X, y) -> MDI vs SHAP side-by-side
   Include type hints, docstrings, and error handling.

2. An interactive Plotly dashboard with four panels:
   (a) model comparison bar chart (RF vs Ridge vs GBR),
   (b) SHAP beeswarm that updates with max_features,
   (c) Train vs Test R² as n_estimators increases,
   (d) toggle between MDI / permutation / SHAP rankings.

[Iterate] Use plotly.graph_objects, shap, numpy, sklearn.
Use the same variable names: X_train, X_test, y_train, y_test.

[Mechanism Check] Add inline comments explaining:
  - How TreeExplainer differs from KernelExplainer
  - Why SHAP values are additive (Shapley property)

[Evaluate] Explain what the dashboard reveals about:
  - The relationship between n_estimators, max_features, and test performance
  - Where MDI and SHAP rankings diverge and why
  - The marginal value of additional trees beyond ~200
```

## What AI Generated

### Artifact 1: Plotly Dashboard
- Four-panel dashboard using `plotly.graph_objects` and `make_subplots`
- Panel (a): Model comparison bar chart for Ridge, RF (default), RF (tuned), GBR
- Panel (b): SHAP global importance bar chart using mean absolute SHAP values
- Panel (c): Train vs Test R² curve across n_estimators = [10, 50, 100, 150, 200, 300, 400, 500]
- Panel (d): Side-by-side MDI, permutation, and SHAP importance rankings
- Dashboard saved as `dashboard.html`

### Artifact 2: README.md
- Professional project description with Objective, Methodology, Key Findings, How to Reproduce, and Repository Structure

### Artifact 3: src/shap_utils.py
- Reusable module with three functions: `explain_prediction()`, `global_importance()`, `compare_importance()`
- Includes docstrings, type hints, and `if __name__ == "__main__"` block

## What I Changed

- Verified variable names match my notebook (`the_best_rf`, `rf_correct`, `the_fit_GBRegressor`)
- Confirmed R² values in dashboard match Part 3 results: Ridge 0.5759, Default RF 0.8062, Tuned RF 0.8147, GBR 0.8288
- Adjusted SHAP explainer to use `X_test[:300]` consistent with the Extension section
- Added `random_state=RANDOM_STATE` to all model fits for reproducibility
- Updated repo structure in README to reflect actual file layout

## What I Verified

- Dashboard opens correctly in browser and all four panels display data
- SHAP values in dashboard are consistent with notebook SHAP output
- R² vs n_estimators curve shows diminishing returns beyond ~200 trees (marginal gain < 0.001)
- MDI ranks AveOccup higher than Latitude; SHAP and permutation rank Latitude higher — consistent with MDI's known bias toward high-cardinality features
- `shap_utils.py` runs without errors via `python src/shap_utils.py`
- All three PNG figures saved correctly to `figures/`

## Key Takeaway

AI accelerated the dashboard and module creation, but manual verification was essential to ensure variable consistency and numerical accuracy. The P.R.I.M.E. framework helped structure the prompt so that AI output aligned closely with existing notebook code.
