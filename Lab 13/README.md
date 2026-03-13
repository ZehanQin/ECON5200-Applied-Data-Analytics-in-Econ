# The Architecture of Dimensionality: Hedonic Pricing & the Frisch-Waugh-Lovell Theorem

## Objective

This project implements a multivariate hedonic pricing model on synthetic California residential real estate data to empirically demonstrate how the Frisch-Waugh-Lovell (FWL) theorem mechanically isolates the partial effect of each regressor—exposing severe omitted variable bias when a spatially correlated covariate is excluded from the specification.

## Data

2026 California Real Estate metrics (Zillow-sourced synthetic panel) comprising `Sale_Price`, `Property_Age`, and `Distance_to_Tech_Hub`. The feature set was deliberately constrained to two continuous regressors to allow geometric intuition over the partialling-out process without sacrificing analytical rigour.

## Technology

Python 3.10+ · pandas · statsmodels.formula.api · matplotlib

## Methodology

**Stage 1 — Naïve Bivariate Specification**
Regressed `Sale_Price` on `Property_Age` alone to establish a baseline coefficient. This intentionally omitted `Distance_to_Tech_Hub`, a variable hypothesised to be correlated with both the dependent variable and the included regressor, thereby satisfying the classical conditions for omitted variable bias.

**Stage 2 — Multivariate Hedonic Model**
Estimated the full specification `Sale_Price ~ Property_Age + Distance_to_Tech_Hub` via OLS. The inclusion of the proximity covariate absorbs the shared covariance between age and location, yielding the partial (ceteris paribus) effect of each feature on sale price.

**Stage 3 — Manual FWL Decomposition**
Proved the theorem by hand in three sub-steps:

1. *Auxiliary Regression*: Regressed `Property_Age` on `Distance_to_Tech_Hub` and retained the residuals. These residuals represent the component of property age that is linearly orthogonal to tech-hub proximity—variation in age that cannot be "explained" by distance.
2. *Partialled-Out Regression*: Regressed `Sale_Price` on those auxiliary residuals alone.
3. *Coefficient Verification*: Confirmed that the slope from the partialled-out regression is numerically identical (to machine precision) to the `Property_Age` coefficient from the full multivariate model, thereby validating the FWL theorem's guarantee of algebraic equivalence.

## Key Findings

**Omitted Variable Bias (OVB)**
The naïve bivariate model materially overstated the magnitude of the `Property_Age` coefficient. Because older properties in the sample tend to be located farther from major tech employment centres, the age variable in the restricted model acted as a proxy for distance, absorbing price variation that properly belongs to the spatial covariate. The direction of the bias is consistent with the classical OVB formula: the bivariate estimate equals the multivariate estimate plus the product of the omitted variable's coefficient and the auxiliary slope of `Distance_to_Tech_Hub` on `Property_Age`.

**FWL Theorem — Algorithmic Ceteris Paribus**
The manual residual-extraction procedure yielded a coefficient on `Property_Age` that matched the multivariate OLS estimate exactly, confirming the core insight of FWL: *multiple regression does not simultaneously estimate all coefficients in some opaque matrix operation—it sequentially "partials out" every other regressor, isolating the unique explanatory content of each feature*. This is the mechanical implementation of the ceteris paribus condition that economic theory demands but observational data never naturally provides.

## Implications

The exercise illustrates a principle that extends well beyond two regressors: every coefficient in an OLS model can be understood as the slope from a simple bivariate regression on residualised data. This framing is foundational for understanding instrumental variable estimation, fixed-effects models, and any identification strategy that relies on removing confounding variation before estimating a causal parameter.

---

*Lab completed as part of an applied econometrics curriculum. All data is synthetic and intended for pedagogical use.*
