# Lab 21 — Time Series Forecasting: ARIMA, GARCH & Bootstrap

> **ECON 5200 · Causal Machine Learning & Applied Analytics**

## Objective

A diagnosis-first forecasting workbench that debugs a broken ARIMA pipeline on US CPI, fits a GARCH(1,1) volatility model to S&P 500 returns, and packages forecast evaluation into a reusable `forecast_evaluation.py` module, with a block-bootstrap forecast-interval extension.

## Methodology

- **Diagnosed and fixed three planted errors in an ARIMA pipeline**:
  1. Wrong differencing order (`d=0` on non-stationary CPI) — fixed by log-transforming and setting `d=1`.
  2. Plain ARIMA on monthly data (ignoring seasonality) — fixed by switching to `SARIMAX` with `seasonal_order=(1, 1, 1, 12)`.
  3. Missing residual diagnostic — fixed by running Ljung-Box on residuals before forecasting.
- **Corrected pipeline**: SARIMAX(2,1,1)(1,1,1)[12] on log CPI, with ADF verification on differences and Ljung-Box residual check.
- **Fit GARCH(1,1) on S&P 500 daily returns** from yfinance. Verified `alpha + beta < 1` (variance stationarity) and computed volatility half-life.
- **Built `src/forecast_evaluation.py`** with `compute_mase()` and `backtest_expanding_window()` functions, including type hints, docstrings, and a self-test block.
- **Implemented block-bootstrap forecast intervals** as a distribution-free alternative to parametric SARIMA CIs.

## Key Findings

- **CPI is I(1) with annual seasonality**. ADF on `diff(log CPI)` rejects the unit root (p ≈ 0.012). SARIMA(2,1,1)(1,1,1)[12] with AIC ≈ −2530 produces a 24-month forecast range of ~330–364 (CPI index).
- **S&P 500 volatility is highly persistent**. Fitted GARCH(1,1): `alpha[1] = 0.12`, `beta[1] = 0.86`, `alpha + beta = 0.98`. Half-life of volatility shocks ≈ **39.5 trading days** — a large shock (2020 COVID, 2008 Lehman) takes ~2 months to decay halfway back to the long-run mean.
- **Volatility clustering is visible across four crisis periods** (9/11, Lehman 2008, COVID 2020, 2022 bear market) — exactly the stylized fact GARCH is designed to capture.

## Repository Layout

    lab 21/
    ├── README.md
    ├── requirements.txt
    ├── notebooks/
    │   └── lab_ch21_diagnostic.ipynb
    └── src/
        └── forecast_evaluation.py

## How to Reproduce

    git clone https://github.com/ZehanQin/ECON5200-Applied-Data-Analytics-in-Econ.git
    cd ECON5200-Applied-Data-Analytics-in-Econ/lab\ 21
    pip install -r requirements.txt
    export FRED_API_KEY="your_key_here"
    jupyter notebook notebooks/lab_ch21_diagnostic.ipynb

## Verification Checkpoints

| Check | Expected | Result |
|---|---|---|
| ADF p-value on diff(log CPI) | < 0.05 | **0.0118** ✅ |
| Three errors identified and explained | Yes | ✅ |
| SARIMAX with seasonal_order used | Yes | ✅ |
| Ljung-Box test executed | Yes | ✅ |
| GARCH `alpha + beta < 1` | Yes | **0.9826** ✅ |
| Volatility half-life computed | Yes | **39.5 days** ✅ |

## Tech Stack

Python 3.10+ · pandas · numpy · statsmodels · pmdarima · arch · fredapi · yfinance · matplotlib

---

*Course:* ECON 5200 — Graduate Applied Econometrics  
*Topic 21 of 26:* Time Series II — ARIMA, GARCH & Forecast Evaluation
