# Forecasting Architecture and the Bias-Variance Tradeoff

## Objective

Diagnose and quantify the operational risk embedded in high-variance polynomial forecasting models applied to real corporate revenue data, demonstrating that near-zero training error is a misleading proxy for predictive accuracy and that K-Fold Cross-Validation is the minimum viable standard for honest model evaluation.

## Data

NVIDIA Corporation (NVDA) quarterly total revenue filings, Q1 2024 – Q1 2026. Source data reflects the secular demand expansion driven by accelerated datacenter and AI infrastructure procurement across the period.

## Methodology

- Ingested and indexed NVIDIA quarterly revenue as a univariate time series, encoding each observation's ordinal quarter position as the sole predictor.
- Constructed a 7th-degree polynomial expansion of the feature space using scikit-learn's `PolynomialFeatures`, enabling the regression surface to capture arbitrarily nonlinear temporal dynamics.
- Fitted an unregularized Ordinary Least Squares model (`LinearRegression`) to the expanded feature matrix and evaluated in-sample training MSE, confirming a near-zero residual — the hallmark of a model that has memorized noise rather than learned signal.
- Extrapolated the fitted polynomial one quarter beyond the training window to expose catastrophic out-of-sample divergence: the model produced a hallucinated revenue forecast disconnected from any plausible financial trajectory.
- Implemented 4-Fold Cross-Validation (`cross_val_score`, `cv=4`) to partition the limited quarterly observations into rotating train/test splits, computing a robust estimate of true generalization error that is immune to the optimistic bias of in-sample evaluation.
- Visualized the overfitted regression curve against the raw observations and the extrapolated prediction to make the variance pathology immediately legible.

## Key Findings

The unregularized 7th-degree polynomial achieved a training MSE approaching zero, yet this metric proved entirely fictitious as a measure of forecasting utility. When subjected to K-Fold Cross-Validation, the model's true generalization MSE was orders of magnitude larger than the training figure, confirming that the polynomial had allocated its degrees of freedom to fitting sample-specific noise rather than the underlying revenue trend. The single-quarter extrapolation further dramatized the failure: the predicted value diverged explosively from any economically rational bound, illustrating how unconstrained coefficient magnitudes in high-degree terms amplify small input perturbations into unbounded output swings. These results establish a concrete empirical case for the Bias-Variance Tradeoff — training-set accuracy was purchased entirely with variance, and the model carries zero credible predictive authority without the application of algorithmic regularization (e.g., Ridge or Lasso penalization) to constrain weight magnitudes.

## Tech Stack

Python · pandas · NumPy · scikit-learn · Matplotlib
