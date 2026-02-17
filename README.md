# ECON5200-Applied-Data-Analytics-in-Econ
# 📊 Economic Data Science Portfolio
**Bridging Economic Theory and Modern Data Science**
---
## 👋 About This Portfolio
Welcome! I'm an undergraduate economics student building expertise at the intersection of causal inference and predictive analytics. This repository showcases my coursework from **ECON 5200: Applied Data Analytics in Economics**, where I'm learning to scale foundational statistical methods using machine learning techniques.
### The Approach
This course follows a *Concept Extension* philosophy: we start with core econometric tools—like ordinary least squares regression—and extend them into the machine learning domain with algorithms like Lasso and Ridge regression. The goal is to understand not just *how* to use these tools, but *when* and *why* each approach is appropriate for different economic questions.
I'm particularly interested in:
- Applying predictive models to economic forecasting problems
- Using causal inference methods to evaluate policy impacts
- Translating complex quantitative findings into actionable insights
---
## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Primary programming language |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Data manipulation and analysis |
| ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) | Machine learning implementation |
| ![Statsmodels](https://img.shields.io/badge/Statsmodels-4B8BBE?style=flat) | Econometric modeling and inference |
| ![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat&logo=scipy&logoColor=white) | Parametric and non-parametric hypothesis testing |
| ![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat&logo=googlecolab&logoColor=white) | Cloud-based development environment |
---
## 📁 Repository Structure
```
├── labs/           # Hands-on coding exercises
├── assignments/    # Course problem sets
├── projects/       # Extended analysis projects
└── notes/          # Concept summaries and documentation
```
---
## 🔬 Projects

### Lab — Hypothesis Testing & Causal Evidence Architecture

**Dataset:** Lalonde (1986) — National Supported Work Demonstration
**Stack:** Python · SciPy · NumPy · Pandas

#### Objective

Estimation tells you *how big* an effect might be. Falsification tells you *whether you should believe it exists at all*. This project marks the deliberate pivot from the former to the latter.

Using the Lalonde (1986) dataset — a canonical benchmark in causal inference — I operationalized the core logic of the scientific method: rather than trying to *prove* that a job-training program increased earnings, I attempted to *disprove* the Null Hypothesis that it had no effect. The surviving evidence, not a single model's point estimate, forms the basis for a causal claim. This is Proof by Statistical Contradiction — the same epistemological engine that powers every credible A/B test and clinical trial in production today.

#### Technical Approach

- **Parametric Testing (Welch's T-Test via `scipy.stats.ttest_ind`):** Computed the Signal-to-Noise ratio (t-statistic) comparing real earnings (`re78`) between treatment and control groups. Welch's variant was selected over Student's T-Test because it does not assume equal variances — a critical guard rail given the heteroscedastic nature of earnings data.

- **Non-Parametric Validation (Permutation Test, 10,000 resamples):** Because earnings distributions are heavily right-skewed and zero-inflated, relying solely on a parametric test would be methodologically fragile. A permutation test was conducted to construct an empirical null distribution from the data itself, making zero distributional assumptions. This serves as a model-free robustness check on the parametric result.

- **Type I Error Control:** Both tests were evaluated against a conventional significance threshold (α = 0.05). The dual-test design — parametric *and* non-parametric — acts as a built-in replication layer, reducing the risk that a significant finding is an artifact of violated assumptions rather than a genuine signal.

#### Key Findings

| Metric | Value |
|---|---|
| Estimated ATE (Δ Real Earnings) | ~$1,795 |
| Welch's T-Test | Statistically significant (p < 0.05) |
| Permutation Test (n = 10,000) | Statistically significant (p < 0.05) |
| Decision | **Reject H₀** — Evidence supports a causal earnings lift from job training |

Both the parametric and non-parametric pipelines converge on the same conclusion: the observed treatment effect is unlikely to have arisen from chance alone.

#### Business Insight — Why This Matters Beyond the Notebook

In a production ML environment, hypothesis testing is the **safety valve of the algorithmic economy**. Without it, every correlation in a feature store looks like a discovery, and every A/B test that clears a cherry-picked metric looks like a win.

Rigorous falsification prevents three failure modes that cost real revenue and erode stakeholder trust:

1. **Data Dredging (p-hacking):** Testing many hypotheses and reporting only the significant ones inflates false-positive rates exponentially. A disciplined test framework — with pre-specified hypotheses and controlled α — is the antidote.
2. **Spurious Correlation at Scale:** Large datasets virtually guarantee statistically significant but meaningless relationships. Effect-size reasoning (the ATE) paired with significance testing separates signal from noise.
3. **Confirmation Bias in Model Evaluation:** Teams that only estimate effects without attempting to *falsify* them are running a one-sided audit. Permutation tests and robustness checks force the uncomfortable question: *"Could this result be nothing?"*

The discipline demonstrated here — estimate, then *stress-test* — is the same workflow that separates a reliable recommendation engine from one that ships a spurious feature to millions of users.

> **A Note on Decision Thresholds:** This lab applies the academic standard of α = 0.05 rigorously, but it is worth noting that in industry, significance thresholds are business parameters — not universal scientific constants. Netflix's Return-Aware Experimentation research, for example, demonstrates that the optimal p-value threshold depends on implementation costs and the distribution of potential treatment effects: firms with low shipping costs and heavy-tailed innovation gains should relax thresholds and run more tests, while firms facing high costs from false discoveries may need stricter ones. The right α is the one that maximizes cumulative long-run returns given the cost structure of your specific experimentation program.

> *"The criterion of the scientific status of a theory is its falsifiability."* — Karl Popper

---
## 🎯 Career Interests
I'm seeking opportunities in **Data Analysis** and **Tech Economics** where I can apply quantitative methods to real-world business and policy questions. If you're interested in connecting, feel free to reach out!
---
*This portfolio is a work in progress as I continue developing my skills throughout the course.*
