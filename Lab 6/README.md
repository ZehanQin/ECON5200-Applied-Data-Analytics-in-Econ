# Lab 6: The Architecture of Bias

## Overview

This lab provides a hands-on investigation into how **bias enters the machine learning pipeline before a single model is trained** — at the level of the Data Generating Process (DGP) and sample construction. Rather than treating datasets as given, this lab treats data collection itself as an engineered system that can silently fail, producing models that are confidently wrong.

Three complementary experiments expose three distinct failure modes: **sampling variance**, **covariate shift**, and **infrastructure-level assignment errors**.

## Tech Stack

`Python` · `pandas` · `NumPy` · `SciPy (Chi-Square)` · `scikit-learn (StratifiedShuffleSplit)`

## Methodology

### 1. Simple Random Sampling & the Variance Problem

Using the Titanic dataset as a controlled environment, I performed repeated rounds of Simple Random Sampling (SRS) and measured the resulting class distributions against the known population parameters. This demonstrated a core statistical reality: SRS is **unbiased in expectation** but exhibits **high variance in any single draw**, meaning a practitioner working with one sample can encounter significant sampling error without any indication that their data is unrepresentative.

### 2. Stratified Sampling as Covariate Shift Elimination

To solve the variance problem exposed above, I implemented Stratified Sampling via scikit-learn's `StratifiedShuffleSplit`. By enforcing proportional representation of the target variable across train/test partitions, this technique **guarantees that the sample mirrors the population's class distribution**, eliminating the covariate shift that SRS leaves to chance. The result is a stable, reproducible foundation for any downstream model.

### 3. Sample Ratio Mismatch (SRM) Forensic Audit

Shifting from model training to experimentation infrastructure, I conducted a forensic audit of an A/B test exhibiting a suspicious 550/450 split against a planned 50/50 allocation (n = 1,000). Using `scipy.stats.chisquare`, the test returned a Chi-Square statistic of 10.0 and a p-value of 0.0016 — well below the α = 0.01 threshold. This constitutes a **Sample Ratio Mismatch**, a critical engineering signal that the randomization unit (e.g., load balancer, redirect logic, or cookie assignment) has failed. Any lift or treatment effect measured on such a compromised experiment is untrustworthy.

## Theoretical Deep Dive: Survivorship Bias & Ghost Data

### The Problem

Consider a dataset of Unicorn startups (valuation ≥ $1B) scraped from TechCrunch. Analyzing only these companies to identify "success factors" — such as founding team size, initial funding round, or market vertical — produces a textbook case of **Survivorship Bias**. The dataset is conditioned on the outcome variable (success), meaning the selection mechanism is endogenous to what we are trying to predict. Any patterns discovered describe *what survivors look like*, not *what caused survival*. A shared trait among Unicorns (e.g., "all had seed rounds > $2M") may be equally prevalent among the thousands of failed startups we never observe.

### The Ghost Data

The missing complement is the **full population of failed, acqui-hired, zombified, and quietly shuttered startups** that entered the same markets, raised similar rounds, and employed similar strategies — but did not reach Unicorn status. This is the **Ghost Data**: observations that the Data Generating Process produced but that the selection mechanism filtered out before they could enter our dataset. Without it, we are estimating P(Feature | Success) when we need P(Success | Feature) — a likelihood inversion that no amount of modeling on the observed sample can correct.

### The Heckman Correction

The **Heckman two-step correction** (Heckman, 1979) is the econometric remedy for this class of selection bias. It works as follows:

1. **Selection Equation (Probit Stage):** Model the probability that a startup *appears in the dataset at all* — i.e., the probability of survival to Unicorn status — as a function of observable covariates. This produces the **Inverse Mills Ratio (λ)**, a correction term that quantifies the selection pressure at each observation.

2. **Outcome Equation (Corrected OLS Stage):** Include λ as an additional regressor in the primary model of interest (e.g., predicting valuation or growth rate). This adjusts coefficient estimates for the truncation introduced by observing only the successful tail of the distribution.

The critical requirement is an **exclusion restriction** — at least one variable that influences whether a startup *survives into the dataset* but does not directly influence the outcome being studied. A candidate might be **geographic proximity to a major VC hub at founding**, which plausibly affects survival-to-observation (media coverage, access to follow-on funding) without directly determining long-term valuation.

Without this correction, any model trained on survivor-only data inherits a systematic upward bias — it mistakes the filter for the phenomenon.

## Key Takeaways

| Failure Mode | Root Cause | Detection / Solution |
|---|---|---|
| High Sampling Variance | Simple Random Sampling on small/imbalanced data | Stratified Sampling |
| Covariate Shift | Train/test distribution mismatch | `StratifiedShuffleSplit` enforcement |
| Sample Ratio Mismatch | Infrastructure/assignment bug in A/B test | Chi-Square goodness-of-fit test |
| Survivorship Bias | Outcome-conditioned selection in DGP | Heckman Correction with Ghost Data |
