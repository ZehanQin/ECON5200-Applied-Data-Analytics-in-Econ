# NY Fed Yield Curve Recession Model Replication

## Objective

Replicate the Federal Reserve Bank of New York's yield curve recession probability model by fitting a logistic regression on publicly available FRED macroeconomic data to forecast NBER-defined recessions 12 months ahead — and demonstrate, on real data, why logistic regression supplants ordinary least squares for binary outcome modeling.

## Methodology

- **Data acquisition.** Retrieved two series from the Federal Reserve Bank of St. Louis (FRED): the 10-Year minus 3-Month Treasury yield spread (T10Y3M, daily frequency) and the NBER recession indicator (USREC, monthly). Coverage spans January 1970 through the most recent available month.
- **Feature engineering.** Resampled the daily yield spread to month-end frequency and lagged it by 12 months, consistent with the NY Fed's published methodology. This transforms the modeling question from contemporaneous classification ("are we in a recession?") to forward-looking prediction ("will we be in a recession 12 months from now?").
- **Linear Probability Model baseline.** Fit OLS on the binary recession indicator to document the well-known failure mode: predicted probabilities that fall below 0 or exceed 1 — logically impossible values that appeared in 16.2% of in-sample observations.
- **Logistic regression.** Fit a logistic regression via scikit-learn, producing a sigmoid curve bounded in [0, 1] by construction. Used `predict_proba()[:, 1]` to extract the positive-class probability for each month in the sample.
- **Inference and odds ratios.** Re-estimated the model via statsmodels `Logit` to obtain coefficient standard errors and 95% confidence intervals. Exponentiated the yield spread coefficient to produce the odds ratio — the standard reporting format in applied economics and regulatory communication.
- **Two-predictor extension.** Augmented the baseline model with the unemployment rate (UNRATE), lagged 12 months, and compared odds ratios across the one- and two-predictor specifications.
- **Cross-validation.** Evaluated both model specifications using `TimeSeriesSplit` (3-fold) to respect temporal ordering and avoid training on future data. Benchmarked against the naive baseline (always predict expansion).

## Key Findings

- **LPM failure is not theoretical.** On real FRED data, the linear probability model produced negative predicted probabilities for 84 of 518 observations — confirming in practice what econometrics textbooks describe in theory.
- **Yield spread odds ratio.** A one-percentage-point increase in the 10Y–3M spread (i.e., a steeper curve) multiplied recession odds by approximately 0.45 (95% CI: 0.33–0.60), corresponding to a 55% reduction. The negative relationship is economically intuitive: a steeper curve signals healthy term premia and expected growth.
- **2022–2024 inversion.** The yield curve inverted in November 2022 and remained inverted through September 2024 — the longest sustained inversion since the 1980s. The model's predicted recession probability peaked at approximately 43%, yet no NBER-defined recession materialized. This outcome is consistent with a well-calibrated probabilistic forecast: a 43% event failing to occur is not a model failure but a reminder that probability estimates are not deterministic predictions.
- **Second predictor (unemployment rate).** Adding UNRATE attenuated the yield spread odds ratio from 0.45 to 0.56, suggesting partial confounding. However, the unemployment rate coefficient was not statistically significant at the 5% level (p = 0.15), and cross-validated accuracy did not improve — indicating that the parsimonious one-predictor specification remains competitive.
- **Cross-validation against naive baseline.** Neither model specification exceeded the naive "always predict expansion" baseline (93.1% accuracy), underscoring a known limitation of accuracy as a metric for imbalanced binary outcomes — a point addressed formally in subsequent coursework on precision, recall, and ROC/AUC.

## Data Sources

| Series | Description | Source |
|--------|-------------|--------|
| T10Y3M | 10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity | FRED |
| USREC | NBER-based Recession Indicators for the United States | FRED |
| UNRATE | Civilian Unemployment Rate | FRED |

## Tech Stack

Python · pandas · NumPy · scikit-learn · statsmodels · matplotlib · Plotly · fredapi
