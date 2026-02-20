# Recovering Experimental Truths via Propensity Score Matching

## Objective

Demonstrate that principled causal-inference techniques—specifically propensity score matching—can recover a credible experimental benchmark from heavily confounded observational data, correcting a naïve estimate that is both economically large and directionally wrong.

## Methodology

- **Diagnosed selection bias** in the observational subset of the Lalonde (1986) dataset, where unadjusted comparisons of treated and control units produced a severely misleading estimate of the job-training program's effect on post-intervention earnings.
- **Estimated propensity scores** via logistic regression, modeling each unit's probability of treatment assignment as a function of observed pre-treatment covariates (age, education, prior earnings, marital status, race, etc.) using Scikit-Learn.
- **Applied Nearest-Neighbor Matching** to pair each treated individual with the control observation whose propensity score was most similar, constructing a pseudo-experimental comparison group that approximates covariate balance across treatment arms.
- **Validated results** by comparing the bias-corrected Average Treatment Effect on the Treated (ATT) against the known experimental benchmark.

## Key Findings

| Metric | Estimate |
|---|---|
| Naïve observational difference | **−$15,204** |
| PSM-adjusted ATT | **≈ +$1,800** |
| Experimental benchmark (Lalonde RCT) | ≈ +$1,794 |

The unadjusted comparison dramatically understated—and reversed the sign of—the true program effect, reflecting profound selection bias: individuals who enrolled in the job-training program differed systematically from the observational control group on nearly every baseline characteristic. After propensity score matching, the corrected estimate closely recovers the experimental ground truth, illustrating both the danger of naïve causal claims from observational data and the power of well-executed matching estimators to mitigate confounding.

## Tech Stack

Python · Pandas · Scikit-Learn · Logistic Regression · Nearest-Neighbor Matching
