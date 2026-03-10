# Architecting the Prediction Engine

## Objective

Design and implement a multivariate OLS prediction engine to forecast residential real estate valuations using cross-sectional market data, then rigorously evaluate out-of-sample generalization performance through dollar-denominated loss minimization.

## Dataset

**Zillow ZHVI 2026 Micro Dataset** — A cross-sectional snapshot of the contemporary U.S. residential market sourced from Zillow's Home Value Index. The dataset captures granular property-level and regional characteristics suitable for hedonic decomposition and predictive modeling of home valuations.

## Technology Stack

Python 3.x · pandas · NumPy · statsmodels (Patsy Formula API)

## Methodology

- **Data Ingestion & Inspection.** Loaded the Zillow ZHVI micro dataset into a pandas DataFrame and conducted preliminary exploratory analysis to assess feature distributions, missing-value patterns, and candidate predictor relevance.
- **Feature Engineering & Formula Specification.** Identified the theoretically motivated set of hedonic attributes (structural, locational, and temporal) and expressed the model specification using the statsmodels Patsy Formula API, enabling concise, readable, and reproducible variable declaration.
- **OLS Estimation.** Fit a multivariate Ordinary Least Squares regression, estimating the marginal implicit price of each housing characteristic while producing the full suite of classical diagnostic statistics (R², F-statistic, coefficient standard errors, p-values).
- **Predictive Pivot.** Shifted the analytical lens from classical coefficient interpretation to out-of-sample prediction accuracy — reframing the model as a forecasting instrument rather than a purely explanatory device.
- **Loss Minimization & RMSE Calculation.** Computed the Root Mean Squared Error in native US Dollar units to quantify the model's expected prediction deviation on unseen observations, translating abstract statistical loss into a concrete financial error margin directly interpretable by business stakeholders.

## Key Findings

The lab achieved a successful transition from classical econometric explanation to applied predictive engineering. By expressing the RMSE in actual US Dollars rather than abstract units, the analysis produced a directly actionable metric: the model's precise average financial error margin per prediction. This reframing allows decision-makers to evaluate algorithmic business risk in the same currency as the asset being valued — bridging the gap between statistical modeling and real-world deployment readiness. The result demonstrates that even a parsimonious linear specification, when carefully constructed, can serve as a viable first-pass valuation engine with a quantifiable and auditable error budget.
