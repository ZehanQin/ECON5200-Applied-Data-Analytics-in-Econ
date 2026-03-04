# Assignment 3: The Causal Architecture

**ECON 5200 | Statistical & Machine Learning for Economics | Module 3**

## Overview

This project tackles three core challenges at **SwiftCart Logistics**, a multinational on-demand delivery platform, using non-parametric statistical methods and causal inference techniques to cut through misleading data narratives:

1. **Driver compensation equity** — auditing zero-inflated tip distributions
2. **A/B test validity** — stress-testing a new routing algorithm's claims
3. **Subscription ROI** — isolating the true causal effect of the SwiftPass loyalty program

## Phase 1: Bootstrapping Non-Parametric Uncertainty

Simulated a zero-inflated tip distribution (100 zero-tips + 150 exponentially distributed tips) and built a **manual bootstrap engine** with 10,000 resamples to construct a 95% confidence interval for the median.

- **Median:** $0.76
- **95% CI:** ($0.27, $1.47)
- **Key Insight:** The confidence interval is asymmetric due to the heavy right skew — a few large tips stretch the upper bound, demonstrating why parametric assumptions (symmetric CIs) fail for this type of data.

## Phase 2: Permutation Testing for A/B Evaluation

Generated synthetic A/B test data comparing a Control group (Normal distribution, mean=35min) against a Treatment group (Log-Normal distribution, mean=3.4, sigma=0.4) to evaluate a batch-routing algorithm.

- **Observed Difference in Means:** 2.26 minutes
- **Permutation Test P-value:** 0.0004 (5,000 permutations)
- **Key Insight:** Under the null hypothesis of no difference, only 0.04% of permutations produced a difference as extreme as the observed value, providing strong evidence against the null — the algorithm does affect delivery times.

## Phase 3: Causal Inference via Propensity Score Matching

Addressed **selection bias** in evaluating the SwiftPass premium subscription's impact on spending.

### Naive vs. Causal Estimate

| Metric | Value |
|--------|-------|
| Naive SDO (Simple Difference) | $17.57 |
| ATT (After PSM) | $9.91 |

### Methodology

1. Estimated propensity scores using **Logistic Regression** on pre-treatment covariates (`pre_spend`, `account_age`, `support_tickets`)
2. Matched each subscriber to the nearest non-subscriber via **Nearest Neighbor Matching** on propensity scores
3. Computed the **Average Treatment Effect on the Treated (ATT)**

### Key Insight

The naive SDO of $17.57 nearly doubles the causal ATT of $9.91, confirming that high-spending users self-select into the subscription program. Propensity Score Matching removes this selection bias by comparing subscribers only to observationally similar non-subscribers.

## Phase 4: Love Plot — Covariate Balance Diagnostic

Generated a Love Plot to visualize **Standardized Mean Differences (SMD)** before and after matching.

| Covariate | Before Matching | After Matching |
|-----------|:-:|:-:|
| `pre_spend` | 0.6740 | 0.0137 |
| `account_age` | 0.3241 | 0.0159 |
| `support_tickets` | 0.1661 | 0.0171 |

All post-matching SMDs fall well below the 0.10 threshold, confirming that observed covariates are well balanced and supporting the credibility of the ATT estimate.

## Tools & Libraries

- **Python** (Google Colab)
- `numpy`, `pandas`, `matplotlib`, `seaborn`
- `scikit-learn` (LogisticRegression, NearestNeighbors)

## File Structure

```
Assignment 3/
├── Econ_3916_Assignment_3.ipynb   # Full Colab notebook
└── README.md                      # This file
```
