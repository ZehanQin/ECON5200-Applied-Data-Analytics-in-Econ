"""
decompose.py — Time Series Decomposition & Diagnostics Module

Reusable functions for STL/MSTL decomposition, stationarity testing,
structural break detection, and block-bootstrap trend uncertainty on
economic time series.

Author: Zehan Qin
Course: ECON 5200, Lab 20
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL, MSTL
from statsmodels.tsa.stattools import adfuller, kpss
import ruptures as rpt
from typing import Optional, Sequence, Dict, Tuple


def run_stl(
    series: pd.Series,
    period: int = 12,
    log_transform: bool = True,
    robust: bool = True,
):
    """Apply STL decomposition with optional log-transform.

    For series with multiplicative seasonality, set log_transform=True
    to convert to additive structure before applying STL.

    Args:
        series: Time series with DatetimeIndex.
        period: Seasonal period (12=monthly, 4=quarterly).
        log_transform: Log-transform for multiplicative data.
        robust: Downweight outliers via bisquare weights.

    Returns:
        STL result object with .trend, .seasonal, .resid.

    Raises:
        ValueError: if series has non-positive values with log_transform=True.
    """
    if log_transform:
        if (series <= 0).any():
            raise ValueError(
                "Series contains non-positive values. "
                "Cannot log-transform. Set log_transform=False."
            )
        work_series = np.log(series)
    else:
        work_series = series.copy()
    return STL(work_series, period=period, robust=robust).fit()


def run_mstl(
    series: pd.Series,
    periods: Sequence[int],
    log_transform: bool = False,
):
    """Multi-seasonal STL decomposition.

    MSTL iteratively peels off seasonal components, shortest period first.

    Args:
        series: Time series with DatetimeIndex.
        periods: Seasonal periods, ascending (e.g. [24, 168]).
        log_transform: Log-transform for multiplicative data.

    Returns:
        MSTL result with .trend, .seasonal (DataFrame), .resid.
    """
    if len(periods) == 0:
        raise ValueError("periods must contain at least one period")
    if log_transform and (series <= 0).any():
        raise ValueError("log_transform=True requires strictly positive values")
    work = np.log(series) if log_transform else series
    return MSTL(work, periods=list(periods)).fit()


def test_stationarity(
    series: pd.Series,
    alpha: float = 0.05,
) -> dict:
    """Run ADF + KPSS and return the 2x2 decision table verdict.

    ADF null : unit root (non-stationary)
    KPSS null: stationary

    Args:
        series: Time series to test.
        alpha: Significance level.

    Returns:
        dict with 'adf_stat', 'adf_p', 'kpss_stat', 'kpss_p', 'verdict'.
        verdict ∈ {'stationary', 'non-stationary', 'contradictory',
        'inconclusive'}.
    """
    adf_stat, adf_p, _, _, _, _ = adfuller(series, autolag='AIC', regression='ct')
    kpss_stat, kpss_p, _, _ = kpss(series, regression='c', nlags='auto')

    adf_rejects = adf_p < alpha
    kpss_rejects = kpss_p < alpha

    if adf_rejects and not kpss_rejects:
        verdict = 'stationary'
    elif not adf_rejects and kpss_rejects:
        verdict = 'non-stationary'
    elif adf_rejects and kpss_rejects:
        verdict = 'contradictory'
    else:
        verdict = 'inconclusive'

    return {
        'adf_stat': adf_stat,
        'adf_p': adf_p,
        'kpss_stat': kpss_stat,
        'kpss_p': kpss_p,
        'verdict': verdict,
    }


def detect_breaks(
    series: pd.Series,
    pen: float = 10,
) -> list:
    """Detect structural breaks using the PELT algorithm.

    PELT minimizes cost + pen * #breaks. Higher pen = fewer breaks
    (bias-variance tradeoff).

    Args:
        series: Time series with DatetimeIndex.
        pen: Penalty parameter.

    Returns:
        List of break dates as pd.Timestamp.
    """
    signal = series.values
    algo = rpt.Pelt(model='rbf').fit(signal)
    breakpoints = algo.predict(pen=pen)
    return [series.index[bp - 1] for bp in breakpoints if bp < len(series)]


def block_bootstrap_trend(
    series: pd.Series,
    period: int = 4,
    n_bootstrap: int = 200,
    block_size: int = 8,
    log_transform: bool = True,
    ci: Tuple[float, float] = (5.0, 95.0),
    robust: bool = True,
    random_state: Optional[int] = 42,
) -> Dict:
    """Moving-block bootstrap confidence bands for an STL trend.

    Block bootstrap preserves short-range autocorrelation (i.i.d.
    bootstrap would destroy it and produce artificially tight bands).

    Args:
        series: Input series (levels).
        period: Seasonal period for STL.
        n_bootstrap: Number of bootstrap replications.
        block_size: Block length. 1 = i.i.d. bootstrap (not recommended).
        log_transform: Decompose in log-space.
        ci: Confidence percentiles.
        robust: Robust STL fitting.
        random_state: Seed for reproducibility.

    Returns:
        dict with 'trend', 'lower', 'upper', 'boot_trends'.
    """
    rng = np.random.default_rng(random_state)
    work = np.log(series) if log_transform else series.copy()
    n = len(work)

    stl = STL(work, period=period, robust=robust).fit()
    orig_trend, orig_seas, orig_resid = (
        stl.trend.values, stl.seasonal.values, stl.resid.values
    )

    boot = np.empty((n_bootstrap, n))
    for b in range(n_bootstrap):
        resampled = np.empty(n)
        i = 0
        while i < n:
            start = rng.integers(0, n - block_size + 1)
            block = orig_resid[start:start + block_size]
            end = min(i + block_size, n)
            resampled[i:end] = block[:end - i]
            i = end
        synth = pd.Series(orig_trend + orig_seas + resampled, index=work.index)
        try:
            synth.index.freq = work.index.freq
        except (AttributeError, ValueError):
            pass
        boot[b] = STL(synth, period=period, robust=robust).fit().trend.values

    lo, hi = np.percentile(boot, [ci[0], ci[1]], axis=0)
    return {
        'trend': pd.Series(orig_trend, index=work.index),
        'lower': pd.Series(lo, index=work.index),
        'upper': pd.Series(hi, index=work.index),
        'boot_trends': boot,
    }


# --- Self-test block ---
if __name__ == '__main__':
    print('decompose.py loaded successfully.')
    print('Functions: run_stl, run_mstl, test_stationarity, detect_breaks, block_bootstrap_trend')

    np.random.seed(42)
    dates = pd.date_range('2000-01-01', periods=200, freq='MS')
    trend = np.linspace(100, 200, 200)
    seasonal = 10 * np.sin(2 * np.pi * np.arange(200) / 12)
    noise = np.random.normal(0, 3, 200)
    test_series = pd.Series(trend + seasonal + noise, index=dates)

    result = run_stl(test_series, period=12, log_transform=False)
    print(f'\nSTL residual std: {result.resid.std():.2f} (expected ~3.0)')

    verdict = test_stationarity(test_series)
    print(f'Stationarity verdict: {verdict["verdict"]}')

    breaks = detect_breaks(test_series, pen=10)
    print(f'Detected breaks: {len(breaks)}')

    print('\nAll module tests passed.')
