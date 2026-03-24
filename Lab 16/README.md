# High-Dimensional GDP Growth Forecasting with Regularized Regression

## Objective

Apply Ridge and Lasso regularization to a high-dimensional cross-country panel of World Development Indicators, demonstrating that penalized regression resolves the severe overfitting exhibited by OLS when the predictor-to-observation ratio is non-trivial — and that Lasso's embedded feature selection can distill 35+ macroeconomic indicators into a parsimonious, interpretable model without meaningful loss in predictive accuracy.

## Data

World Bank World Development Indicators (WDI), accessed programmatically via the `wbgapi` Python API. The dataset covers 120+ economies over the 2013–2019 window and is averaged to a single cross-section per country. After missingness filtering (≥60% non-missing threshold) and median imputation, the final design matrix contains 238 country-level observations across 28 standardized predictors spanning nine domains: trade and openness, macroeconomic stability, education and human capital, infrastructure and technology, health and demographics, financial development, natural resources, agriculture, and governance (CPIA scores).

The outcome variable is average annual GDP per capita growth (constant USD).

## Methodology

- Downloaded 37 WDI series via `wbgapi.data.DataFrame`, applied temporal averaging, and enforced a 60% completeness threshold on both the country and indicator axes to balance coverage against sample size.
- Split the data 70/30 into training (166 countries) and holdout test (72 countries) sets using `train_test_split` with a fixed random seed for reproducibility.
- Standardized all predictors to zero mean and unit variance via `StandardScaler`, fitting on the training partition only to prevent data leakage into the test set.
- Fit an unpenalized OLS baseline (`LinearRegression`) to establish the overfitting benchmark: high in-sample R² coupled with negative out-of-sample R².
- Estimated a Ridge regression with 5-fold cross-validated lambda selection (`RidgeCV`) over a log-spaced grid of 50 candidates from 10⁻² to 10³, shrinking all coefficients toward zero without exact sparsity.
- Estimated a Lasso regression with 5-fold cross-validated lambda selection (`LassoCV`, `max_iter=10,000`), which simultaneously shrinks and performs embedded feature selection by driving redundant coefficients to exactly zero.
- Visualized the full Lasso coefficient path using `sklearn.linear_model.lasso_path` to trace how each predictor enters or exits the active set as regularization strength varies.
- Built an interactive two-panel Plotly dashboard featuring a draggable lambda slider on the Lasso path (with real-time R² annotation) and a grouped bar chart comparing OLS, Ridge, and Lasso coefficient magnitudes side by side.

## Key Findings

- **OLS overfitting is severe.** The unpenalized model achieved a training R² of 0.600 but a test R² of −0.849, confirming that with a predictor-to-observation ratio of 28/166 ≈ 0.17, OLS memorizes noise rather than learning generalizable structure. The train–test R² gap of 1.45 is a textbook illustration of high-variance estimation.
- **Ridge regularization recovers generalization.** RidgeCV selected λ\* = 47.15 and improved test R² from −0.849 to −0.051, cutting test MSE nearly in half (8.25 → 4.69). All 28 coefficients remain non-zero but are uniformly attenuated — the expected shrinkage-without-selection behavior.
- **Lasso achieves comparable performance with a sparse model.** LassoCV selected λ\* = 0.066 and retained only 17 of 28 predictors, zeroing out the remaining 11 entirely. Test R² (−0.330) is modestly below Ridge, but the model is substantially more interpretable. The dominant retained predictors — CPI inflation, population growth, natural resource rents, health expenditure, and infant mortality — align with established findings in the empirical growth literature.
- **Predictive redundancy ≠ economic irrelevance.** Lasso's elimination of a predictor (e.g., paved roads percentage) reflects conditional redundancy given the other covariates in the model, not a causal claim that the variable is unrelated to growth. The high correlation structure among WDI indicators means Lasso arbitrarily selects one member of each collinear cluster — a well-known limitation that warrants caution when drawing policy conclusions from penalized coefficient estimates.
- **All models struggle with GDP growth prediction.** Negative test R² across all three specifications underscores a fundamental signal-to-noise challenge: cross-country growth regressions are inherently noisy, and even well-regularized linear models cannot capture the complex, nonlinear, and often idiosyncratic determinants of national economic performance from aggregate indicators alone.

## Tech Stack

Python 3.12 · pandas · NumPy · scikit-learn · matplotlib · Plotly · wbgapi
