# Lab 20 — Time Series Diagnostics & Advanced Decomposition

> **ECON 5200 · Causal Machine Learning & Applied Analytics · Topic 20 of 26**

## Objective

A diagnosis-first time-series workbench that rebuilds core macro-econometric plumbing — STL / MSTL decomposition, ADF + KPSS stationarity testing, PELT structural-break detection, and block-bootstrap trend uncertainty — as a portable `decompose.py` module plus an interactive Streamlit dashboard.

## Methodology

- **Diagnosed and fixed a broken STL decomposition.** Retail sales (FRED `RSXFSN`) exhibit multiplicative seasonality, but STL is an additive model. Applied a log-transform before decomposing. Verified the seasonal-amplitude ratio landed in [0.7, 1.3] (achieved 0.91).
- **Fixed a misspecified ADF test.** GDP (`GDPC1`) has both a non-zero mean and a deterministic upward trend. Switched `regression='n'` to `regression='ct'`. Paired with KPSS for a 2×2 stationarity verdict.
- **Applied MSTL to multi-seasonal data.** Decomposed simulated hourly electricity demand into trend + 24-hour daily cycle + 168-hour weekly cycle. Residual std ≈ 12 MW recovered the true injected noise level.
- **Implemented moving-block bootstrap for trend uncertainty.** Sampled contiguous residual blocks (block size = 8 quarters) to preserve short-range autocorrelation. CI width at 2008-Q4 (0.0106) exceeds 2019-Q4 (0.0056).
- **Detected structural breaks with PELT + per-regime stationarity.** Ran PELT on quarterly GDP growth (penalty = 3), then ADF + KPSS within each regime.
- **Packaged everything in `src/decompose.py`.** Production module with `run_stl()`, `run_mstl()`, `test_stationarity()`, `detect_breaks()`, `block_bootstrap_trend()` — full type hints, docstrings, and self-tests.
- **Shipped an interactive Streamlit dashboard** (`src/app.py`) exposing FRED series lookup, method selection, parameter sliders, stationarity verdicts, break detection, and block-bootstrap CIs.

## Key Findings

- **Real GDP is I(1) with structural breaks.** ADF (`regression='ct'`) fails to reject a unit root (p ≈ 0.96); KPSS rejects trend-stationarity; the first difference is unambiguously stationary. PELT surfaces a dominant break near 1985-Q1 (end of the Volcker disinflation / Great Moderation onset).
- **Trend uncertainty is state-dependent.** 90% block-bootstrap bands are visibly wider around the 2008 GFC and 2020 COVID shocks than during expansion windows.
- **Parameter choices materially change conclusions.** The Streamlit app makes three sensitivities visible: log-transform, PELT penalty, and block size.

## Repository Layout

    lab 20/
    ├── README.md
    ├── requirements.txt
    ├── notebooks/
    │   └── lab_ch20_diagnostic.ipynb
    ├── src/
    │   ├── decompose.py
    │   └── app.py
    └── verification-log.md

## How to Reproduce

    # 1. Clone the repo
    git clone https://github.com/ZehanQin/ECON5200-Applied-Data-Analytics-in-Econ.git
    cd ECON5200-Applied-Data-Analytics-in-Econ/lab\ 20

    # 2. Install dependencies
    pip install -r requirements.txt

    # 3. Set your FRED API key
    export FRED_API_KEY="your_key_here"

    # 4. Run the notebook end-to-end
    jupyter notebook notebooks/lab_ch20_diagnostic.ipynb

    # 5. (Optional) Launch the Streamlit dashboard
    streamlit run src/app.py

## Verification Checkpoints

| Check | Expected | Result |
|---|---|---|
| STL seasonal-amplitude ratio (post log) | 0.7 – 1.3 | **0.91** ✅ |
| ADF p-value on GDP levels (`regression='ct'`) | > 0.05 | **0.96** ✅ |
| MSTL residual std | ≈ 15 MW | **12.24** ✅ |
| Bootstrap CI width 2008-Q4 > 2019-Q4 | True | **0.0106 > 0.0056** ✅ |
| `test_stationarity(gdp)` verdict | `'non-stationary'` | ✅ |
| `test_stationarity(gdp_growth)` verdict | `'stationary'` | ✅ |

## Tech Stack

Python 3.10+ · pandas · numpy · statsmodels · ruptures · fredapi · Streamlit · Plotly · Matplotlib

---

*Course:* ECON 5200, Graduate Applied Econometrics  
*Topic 20 of 26:* Time Series I — Trends & Decomposition
