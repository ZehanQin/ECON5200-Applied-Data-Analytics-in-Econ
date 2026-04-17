# Verification Log — Lab 20 AI Expansion

> P.R.I.M.E. audit trail for the AI-assisted extension artifacts.

## P.R.I.M.E. Prompt Used

    [Prep] Act as an expert Python Data Scientist specializing in
    time series analysis, FRED API, and production ML systems.

    [Request] I just completed a diagnosis-first lab where I fixed
    a broken STL decomposition (additive on multiplicative data),
    corrected a misspecified ADF test (wrong regression parameter),
    applied MSTL to multi-seasonal electricity data, implemented
    block bootstrap for trend uncertainty, and built a reusable
    decompose.py module. Now I need TWO artifacts:

    1. An extended src/decompose.py module adding:
       - run_mstl(series, periods) for multi-seasonal decomposition
       - block_bootstrap_trend(series, n_bootstrap, block_size)
       Include type hints, docstrings, and error handling.

    2. An interactive Streamlit app that lets users: enter a FRED
       series ID, select decomposition method (Classical/STL/MSTL),
       adjust parameters with sliders, see decomposition panels +
       stationarity tests, view structural breaks, generate block
       bootstrap CIs.

    [Iterate] Use streamlit, plotly, fredapi, statsmodels, ruptures.
    Handle missing data and frequency detection automatically.

    [Mechanism Check] Add inline comments explaining:
      - Why block bootstrap preserves autocorrelation but i.i.d.
        bootstrap destroys it
      - How MSTL iteratively removes seasonal components
      - Why PELT's penalty parameter controls the bias-variance
        tradeoff of break detection

    [Evaluate] Explain what the app reveals about the sensitivity
    of decomposition results to parameter choices.

## What the AI Generated

- **Extended `decompose.py`** — added `run_mstl()` and `block_bootstrap_trend()` on top of `run_stl()`, `test_stationarity()`, `detect_breaks()`. All functions have type hints, docstrings, and input validation.
- **`app.py`** — Streamlit dashboard with 5 tabs (Raw / Decomposition / Stationarity / Breaks / Bootstrap), sidebar controls for FRED series ID, start date, decomposition method, period sliders, log-transform/robust toggles, PELT penalty, bootstrap replications and block size.
- Inline mechanism comments on i.i.d. vs block bootstrap, MSTL iteration, and PELT penalty bias-variance.

## What I Changed / Verified Manually

| Area | Issue or Check | Action Taken |
|---|---|---|
| `block_bootstrap_trend` | Initially used legacy `np.random.seed`. | Switched to `np.random.default_rng(random_state)` for modern NumPy API consistency. |
| `run_mstl` | Did not validate empty `periods` or non-positive values under log-transform. | Added explicit `ValueError` guards matching `run_stl` style. |
| Streamlit app frequency detection | Assumed quarterly data. | Added `pd.infer_freq` + `try/except` so monthly (`RSXFSN`), quarterly (`GDPC1`), and other freqs all work. |
| Streamlit MSTL fallback | Crashed when `extra_period=0`. | Fallback to single-period STL when `extra_period == 0`. |
| Bootstrap tab warning | No warning at `block_size=1`. | Added `st.warning` explaining why `block_size=1` destroys autocorrelation. |
| Part 6 stationarity test | AI initially asserted `gdp.diff()` → `'stationary'`. Actual verdict was `'contradictory'`. | Switched to `gdp.pct_change().dropna() * 100` which is genuinely stationary per the 2×2 table. Verdict verified as `'stationary'`. |
| PELT penalty | `pen=10` produced 0 breaks on my GDP vintage. | Tuned to `pen=3`, which recovers the 1985-Q1 Great Moderation break consistent with macro literature. |

## Evaluation — What the App Reveals

Running the dashboard against multiple FRED series surfaces three decomposition sensitivities:

1. **Log-transform matters more than method choice.** Toggling `log_transform` on `RSXFSN` changes the seasonal-amplitude ratio from ~3× to ~0.9×, while switching Classical ↔ STL ↔ MSTL produces only cosmetic differences. The multiplicative-vs-additive choice dominates.

2. **PELT penalty is a direct bias–variance knob.** Sliding `pen` from 1 → 50 on quarterly GDP growth, detected breaks shrink from 8+ (overfits noise) to 0 (misses Volcker / Great Moderation). A well-calibrated penalty around 3 recovers the 1985 break.

3. **Block size directly controls honest CI width.** With `block_size = 1` (i.i.d. bootstrap), the 90% band is ~40% narrower than with `block_size = 8`. The tighter band is an under-estimate — autocorrelation was destroyed.

**Core takeaway.** Decomposition is not a point-and-click operation; every parameter bakes assumptions into the conclusion. A production time-series tool should expose multiple parameter combinations so the reader can judge the robustness of findings — which is what this dashboard does.
