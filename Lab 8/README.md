# Hypothesis Testing & Causal Evidence Architecture

**Dataset:** Lalonde (1986) — National Supported Work Demonstration
**Stack:** Python · SciPy · NumPy · Pandas

---

## Objective

Estimation tells you *how big* an effect might be. Falsification tells you *whether you should believe it exists at all*. This project marks the deliberate pivot from the former to the latter.

Using the Lalonde (1986) dataset — a canonical benchmark in causal inference — I operationalized the core logic of the scientific method: rather than trying to *prove* that a job-training program increased earnings, I attempted to *disprove* the Null Hypothesis that it had no effect. The surviving evidence, not a single model's point estimate, forms the basis for a causal claim. This is Proof by Statistical Contradiction — the same epistemological engine that powers every credible A/B test and clinical trial in production today.

## Technical Approach

- **Parametric Testing (Welch's T-Test via `scipy.stats.ttest_ind`):** Computed the Signal-to-Noise ratio (t-statistic) comparing real earnings (`re78`) between treatment and control groups. Welch's variant was selected over Student's T-Test because it does not assume equal variances — a critical guard rail given the heteroscedastic nature of earnings data.

- **Non-Parametric Validation (Permutation Test, 10,000 resamples):** Because earnings distributions are heavily right-skewed and zero-inflated, relying solely on a parametric test would be methodologically fragile. A permutation test was conducted to construct an empirical null distribution from the data itself, making zero distributional assumptions. This serves as a model-free robustness check on the parametric result.

- **Type I Error Control:** Both tests were evaluated against a conventional significance threshold (α = 0.05). The dual-test design — parametric *and* non-parametric — acts as a built-in replication layer, reducing the risk that a significant finding is an artifact of violated assumptions rather than a genuine signal.

## Key Findings

| Metric | Value |
|---|---|
| Estimated ATE (Δ Real Earnings) | ~$1,795 |
| Welch's T-Test | Statistically significant (p < 0.05) |
| Permutation Test (n = 10,000) | Statistically significant (p < 0.05) |
| Decision | **Reject H₀** — Evidence supports a causal earnings lift from job training |

Both the parametric and non-parametric pipelines converge on the same conclusion: the observed treatment effect is unlikely to have arisen from chance alone.

## Business Insight — Why This Matters Beyond the Notebook

In a production ML environment, hypothesis testing is the **safety valve of the algorithmic economy**. Without it, every correlation in a feature store looks like a discovery, and every A/B test that clears a cherry-picked metric looks like a win.

Rigorous falsification prevents three failure modes that cost real revenue and erode stakeholder trust:

1. **Data Dredging (p-hacking):** Testing many hypotheses and reporting only the significant ones inflates false-positive rates exponentially. A disciplined test framework — with pre-specified hypotheses and controlled α — is the antidote.
2. **Spurious Correlation at Scale:** Large datasets virtually guarantee statistically significant but meaningless relationships. Effect-size reasoning (the ATE) paired with significance testing separates signal from noise.
3. **Confirmation Bias in Model Evaluation:** Teams that only estimate effects without attempting to *falsify* them are running a one-sided audit. Permutation tests and robustness checks force the uncomfortable question: *"Could this result be nothing?"*

The discipline demonstrated here — estimate, then *stress-test* — is the same workflow that separates a reliable recommendation engine from one that ships a spurious feature to millions of users.

---

> *"The criterion of the scientific status of a theory is its falsifiability."* — Karl Popper
