# Lab 24 Verification Log

## Part A — Manual DML Verification on Simulated DGP
- True ATE: 5.00
- Fixed ATE: 5.15
- Bias: +0.15
- Status: PASS (within ±0.3 tolerance)

## Part B — 401(k) DML with DoubleML
- ATE: $8,628
- Standard Error: $1,358
- 95% CI: [$5,965, $11,290]
- t-statistic: 6.35
- p-value: 2.13e-10
- Status: Statistically significant (p < 0.001)

## Part B — Sensitivity Analysis
- cf_y: 0.03
- cf_d: 0.03
- Robustness Value (RV): 6.79%
- RVa: 4.97%
- Lower bound theta: $4,890
- Status: Estimate survives moderate unobserved confounding

## Part C — Causal Forest CATE
- CATE predictions shape: (9915,)
- Mean CATE: $7,703
- Std CATE: $6,606
- Min CATE: -$10,713
- Max CATE: $44,987

## Part C — High-Response Subgroup (Top 25%)
- Mean age: 43.77 (vs 36.95 low-response)
- Mean income: $66,479 (vs $21,330 low-response)
- Mean education: 14.25 years (vs 12.33 low-response)
- Married: 84% (vs 49% low-response)
- IRA participation: 46% (vs 14% low-response)

## Extension — Subgroup DML vs Causal Forest
- Between-quartile CATE range: $13,338
- Average within-quartile std: $3,508
- Conclusion: Causal Forest reveals significant heterogeneity within income quartiles that subgroup DML misses
