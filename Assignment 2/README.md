# Audit 02: Deconstructing Statistical Lies

> **Course:** ECON 5200 — Assignment 2  
> **Author:** Zehan
> **Date:** February 2026  
> **Stack:** Python · NumPy · Pandas · Matplotlib · Seaborn

---

## Overview

This audit exposes three mechanisms through which summary statistics mislead
decision-makers: outlier-inflated dispersion, base-rate neglect in classification,
and survivorship bias in market data. Each phase pairs a from-scratch algorithm
with a real-world scenario to show *how* and *why* the lie works.

---

## Phase 1 — Latency Skew: When the "Average" Is a Lie

**Scenario:** 1,000 server latency logs — 980 normal pings (20–50 ms) and 20
extreme spikes (1,000–5,000 ms).

| Metric | Value |
|--------|-------|
| Standard Deviation | 517.70 ms |
| Median Absolute Deviation (MAD) | 8.0 ms |

**Key Finding:** SD overstates variability by roughly **65×** compared to MAD.
Because SD squares each deviation from the *mean*, a handful of outliers
(just 2% of the data) dominate the result. MAD, built on the *median* and
absolute deviations, is nearly immune to the same spikes. In any
outlier-contaminated dataset — network logs, financial returns, sensor
readings — reporting SD alone paints a misleading picture of typical behavior.

---

## Phase 2 — False Positives: Bayesian Audit Detection

**Scenario:** An AI cheating detector with 98% sensitivity and 98% specificity
is deployed across three populations with different base rates of cheating.

| Scene | Population | Base Rate | P(Cheater ∣ Flagged) |
|-------|-----------|-----------|----------------------|
| A | Bootcamp | 50% | **98.0%** |
| B | Econ Class | 5% | **72.1%** |
| C | Honors Seminar | 0.1% | **4.7%** |

**Key Finding:** The same 98%-accurate detector is *useless* in low-prevalence
settings. In the Honors Seminar, over **95% of flags are false positives**.
This is a direct consequence of Bayes' Theorem — when the prior probability of
cheating is tiny, even a highly specific test generates more noise than signal.
Any institution deploying automated detection must account for base-rate context
or risk punishing innocent students at scale.

---

## Phase 3 — Chi-Square Fairness Test: Algorithm Bias Audit

**Scenario:** A hiring algorithm produces 50,250 male and 49,750 female
selections out of 100,000 total. Is this evidence of engineering bias?

| Metric | Value |
|--------|-------|
| χ² Statistic | 2.50 |
| Critical Value (α = 0.05, df = 1) | 3.84 |
| Verdict | **Valid — no significant bias detected** |

**Key Finding:** The observed imbalance (50.25% vs 49.75%) is well within the
range expected from random variation alone. The chi-square test confirms there
is insufficient evidence to reject the null hypothesis of equal selection rates.
This phase demonstrates that not every numerical asymmetry signals
discrimination — statistical testing provides the framework to distinguish
meaningful skew from noise.

---

## Phase 4 — Survivorship Bias: The Crypto Graveyard

**Scenario:** 10,000 simulated token launches using a mixture-model DGP:
99% of tokens fail (peak market cap < $1), while 1% "moon" via a Pareto
power-law tail.

| Group | Mean Peak MCap | Median Peak MCap |
|-------|---------------|-----------------|
| All 10,000 Tokens | $1,149.75 | $0.25 |
| Top 1% Survivors | $114,950.66 | $72,607.69 |

**Survivorship Bias Multiplier: 100×**

**Sanity Checks:**
- Share of tokens below $1: 99.15%
- Share of tokens below $10: 99.15%

**Key Finding:** If you only study the winners — the tokens featured in
headlines, YouTube thumbnails, and Discord alpha channels — the average
market cap appears to be ~$115K. The true population average is ~$1,150,
and the *typical* token (median) peaked at $0.25. The 100× multiplier
quantifies the exact distortion produced by conditioning on survival.
This is the statistical engine behind "my friend made $500K on a memecoin"
anecdotes: you never hear from the 9,900 people who lost everything.

---

## Connecting the Phases

| Phase | Core Illusion | Mechanism |
|-------|--------------|-----------|
| 1 — Latency Skew | "High variability" | Outliers inflate squared-deviation metrics |
| 2 — False Positives | "The test is 98% accurate" | Base-rate neglect via Bayes' Theorem |
| 3 — Chi-Square | "The algorithm is biased" | Confusing random noise with systematic skew |
| 4 — Survivorship | "Crypto makes everyone rich" | Conditioning on winners hides the graveyard |

Each phase isolates a different way that correct math applied to incomplete
framing produces a *statistical lie*. The throughline: **always ask what the
number is hiding before you trust what it's showing.**

---

## How to Run

```bash
# Open in Google Colab or run locally
jupyter notebook Econ_5200_Assignment_2_Audit.ipynb
```

**Requirements:** `numpy`, `pandas`, `matplotlib`, `seaborn` (all included in
Colab by default).

---

## License

Academic use — ECON 5200.
