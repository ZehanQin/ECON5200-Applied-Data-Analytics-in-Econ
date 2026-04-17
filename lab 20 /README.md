# Lab 20 — Time Series Diagnostics & Advanced Decomposition

> **ECON 5200 · Causal Machine Learning & Applied Analytics · Topic 20 of 26**

## Objective

A diagnosis-first time-series workbench that rebuilds core macro-econometric
plumbing — STL / MSTL decomposition, ADF + KPSS stationarity testing, PELT
structural-break detection, and block-bootstrap trend uncertainty — as a
portable `decompose.py` module plus an interactive Streamlit dashboard.

## Methodology

- **Diagnosed and fixed a broken STL decomposition.** Retail sales (FRED
  `RSXFSN`) exhibit multiplicative seasonality, but STL is an additive model.
  Applied a log-transform to convert $Y_t = T_t \times S_t \times R_t$ into
  $\log Y_t = \log T_t + \log S_t + \log R_t$ before decomposing. Verified the
  seasonal-amplitude ratio landed in [0.7, 1.3] (achieved 0.91).
- **Fixed a misspecified ADF test.** GDP (`GDPC1`) has both a non-zero mean
  and a deterministic upward trend. Switched `regression='n'` → `regression='ct'`
  so the auxiliary regression includes the constant and linear trend actually
  present in the data. Paired with KPSS for a 2×2 stationarity verdict.
- **Applied MSTL to multi-seasonal data.** Decomposed simulated hourly
  electricity demand into trend + 24-hour daily cycle + 168-hour weekly cycle.
  Residual std ≈ 12 MW recovered the true injected noise level, confirming
  clean separation of the two overlapping seasonalities.
- **Implemented moving-block bootstrap for trend uncertainty.** Sampled
  contiguous residual blocks (block size = 8 quarters ≈ one business-cycle
  horizon) to preserve short-range autocorrelation, re-ran STL on each
  bootstrap sample, and computed pointwise 5th/95th percentile confidence
  bands around the log-GDP trend. CI width at 2008-Q4 (0.0106) exceeds
  2019-Q4 (0.0056), quantifying wider trend uncertainty during recessions.
- **Detected structural breaks with PELT + per-regime stationarity.** Used
  the PELT changepoint algorithm on quarterly GDP growth (penalty = 3),
  then ran ADF + KPSS within each regime to test whether stationarity
  conclusions are stable across structural shifts.
- **Packaged everything in `src/decompose.py`.** Production module with
  `run_stl()`, `run_mstl()`, `test_stationarity()`, `detect_breaks()`, and
  `block_bootstrap_trend()` — full type hints, docstrings, input validation,
  and a `__main__` self-test block.
- **Shipped an interactive Streamlit dashboard** (`src/app.py`) exposing
  FRED series lookup, method selection (Classical / STL / MSTL), parameter
  sliders, stationarity verdicts, break detection, and block-bootstrap CIs.

## Key Findings

- **Real GDP is I(1) with structural breaks.** ADF (`regression='ct'`) fails
  to reject a unit root (p ≈ 0.96); KPSS rejects trend-stationarity; the
  first difference (quarterly growth) is unambiguously stationary. PELT on
  quarterly growth surfaces a dominant break near **1985-Q1** (end of the
  Volcker disinflation / onset of the Great Moderation), splitting the
  series into two stationary regimes.
- **Trend uncertainty is state-dependent.** 90% block-bootstrap bands are
  visibly wider around the 2008 GFC and 2020 COVID shocks than during
  expansion windows — a stylized fact that point-estimate trends obscure.
- **Parameter choices materially change conclusions.** The Streamlit app
  makes three sensitivities visible at a glance: (i) the log-transform
  toggles whether STL cleanly separates seasonality; (ii) PELT penalty is a
  direct bias–variance knob; (iii) block size ≪ autocorrelation length
  yields artificially tight bands.

## Repository Layout
