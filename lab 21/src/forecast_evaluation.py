"""
forecast_evaluation.py — Forecast Evaluation & Backtesting Module

Reusable functions for computing MASE and running expanding-window
backtests on time series forecasting models.

Author: Zehan Qin
Course: ECON 5200, Lab 21
"""

import numpy as np
import pandas as pd
from typing import Callable


def compute_mase(
    actual: np.ndarray,
    forecast: np.ndarray,
    insample: np.ndarray,
    m: int = 1
) -> float:
    """Compute Mean Absolute Scaled Error.

    MASE < 1: model beats naive seasonal benchmark.
    MASE > 1: naive benchmark is better.

    Args:
        actual: True out-of-sample values
        forecast: Model predictions (same length as actual)
        insample: In-sample (training) data for naive baseline
        m: Seasonal period (1=random walk, 12=monthly seasonal)

    Returns:
        MASE score (float)
    """
    mae_forecast = np.mean(np.abs(actual - forecast))
    naive_errors = insample[m:] - insample[:-m]
    mae_naive = np.mean(np.abs(naive_errors))
    return mae_forecast / mae_naive


def backtest_expanding_window(
    series: pd.Series,
    model_fn: Callable,
    min_train: int = 120,
    horizon: int = 12,
    step: int = 12
) -> pd.DataFrame:
    """Expanding-window time series backtest.

    Args:
        series: Full series with DatetimeIndex
        model_fn: Callable(train) -> np.ndarray of length horizon
        min_train: Minimum training observations
        horizon: Forecast horizon per iteration
        step: Observations added per iteration

    Returns:
        DataFrame with backtest results
    """
    results = []
    for origin in range(min_train, len(series) - horizon, step):
        train = series.iloc[:origin]
        actual = series.iloc[origin:origin + horizon].values
        forecast = model_fn(train)
        errors = actual - forecast
        mase = compute_mase(actual, forecast, train.values, m=12)
        for h in range(len(actual)):
            results.append({
                'origin': series.index[origin],
                'horizon': h + 1,
                'actual': actual[h],
                'forecast': forecast[h],
                'error': errors[h],
                'abs_error': np.abs(errors[h]),
                'mase': mase
            })
    return pd.DataFrame(results)


# --- Quick self-test ---
if __name__ == '__main__':
    print('forecast_evaluation.py loaded successfully.')
    train = np.sin(np.linspace(0, 8 * np.pi, 120))
    actual = np.sin(np.linspace(8 * np.pi, 9 * np.pi, 12))
    predicted = actual + np.random.normal(0, 0.1, 12)
    mase = compute_mase(actual, predicted, train, m=12)
    print(f"Test MASE: {mase:.3f}")
