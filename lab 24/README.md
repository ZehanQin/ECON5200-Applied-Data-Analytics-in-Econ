# Causal ML — DML and Causal Forests for Policy Evaluation

## Objective
Estimate the causal effect of 401(k) eligibility on net financial assets using Double Machine Learning and Causal Forests, while diagnosing and correcting common implementation failures in manual cross-fitting pipelines.

## Methodology
- Diagnosed and fixed three critical bugs in a broken manual DML implementation: in-sample prediction leakage violating cross-fitting, missing treatment residualization leaving the confounding path X→D intact, and an incorrect naïve OLS formula for θ instead of the IV-style Frisch-Waugh-Lovell estimator
- Verified the corrected pipeline recovers the true ATE (= 5.0) on a simulated DGP with known ground truth
- Estimated the ATE of 401(k) eligibility on net financial assets using the `DoubleML` package with Random Forest nuisance learners and 5-fold cross-fitting
- Conducted sensitivity analysis to assess robustness to unmeasured confounders via the robustness value (RV) framework
- Fit a `CausalForestDML` (EconML) to estimate individual-level Conditional Average Treatment Effects (CATEs) with honest splitting and DML-style debiasing
- Compared coarse subgroup DML (income quartile-level) to Causal Forest continuous CATE estimation to evaluate heterogeneity detection granularity

## Key Findings
- **ATE**: 401(k) eligibility increases net financial assets by **$8,628** (95% CI: [$5,965, $11,290], p < 0.001)
- **Robustness**: RV = 6.79%, meaning an unobserved confounder would need to explain over 6.79% of residual variance in both treatment and outcome simultaneously to nullify the result — a high bar relative to observed covariates
- **Heterogeneity**: Causal Forest reveals substantial within-quartile CATE variation (average within-quartile std = $3,508) relative to the between-quartile range ($13,338), demonstrating that income quartile-level subgroup DML misses significant individual-level heterogeneity. High-response individuals tend to be older, higher-income, more educated, and married — consistent with economic theory on retirement savings behavior

## Repository Structure
​```
econ-lab-24-causal-ml/
├── README.md
├── notebooks/
│   └── lab_24_causal_ml.ipynb
├── src/
│   └── causal_ml.py
├── figures/
│   ├── cate_histogram.png
│   └── sensitivity_plot.png
└── verification-log.md
​```

## Tech Stack
- Python, DoubleML, EconML, scikit-learn, pandas, matplotlib
- Dataset: 401(k) Pension Data (Chernozhukov & Hansen), 9,915 observations
