# src/causal_ml.py
"""Causal ML module for DML and CATE analysis."""

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import KFold
from typing import Tuple, Optional


def manual_dml(
    Y: np.ndarray,
    D: np.ndarray,
    X: np.ndarray,
    ml_l,
    ml_m,
    n_folds: int = 5,
    random_state: int = 42
) -> Tuple[float, float]:
    """
    Manual Double ML with cross-fitting.
    
    Returns: (theta, se)
    """
    n = len(Y)
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    
    Y_hat = np.zeros(n)
    D_hat = np.zeros(n)
    
    for train_idx, test_idx in kf.split(X):
        ml_l_k = clone(ml_l)
        ml_l_k.fit(X[train_idx], Y[train_idx])
        Y_hat[test_idx] = ml_l_k.predict(X[test_idx])
        
        ml_m_k = clone(ml_m)
        ml_m_k.fit(X[train_idx], D[train_idx])
        D_hat[test_idx] = ml_m_k.predict(X[test_idx])
    
    V_hat = Y - Y_hat
    W_hat = D - D_hat
    
    theta = np.sum(W_hat * V_hat) / np.sum(W_hat * W_hat)
    residuals = V_hat - theta * W_hat
    se = np.sqrt(np.sum(W_hat**2 * residuals**2) / (np.sum(W_hat**2))**2)
    
    return theta, se


def cate_by_subgroup(
    data: pd.DataFrame,
    y_col: str,
    d_col: str,
    x_cols: list,
    group_col: str,
    ml_l,
    ml_m,
    n_folds: int = 5
) -> pd.DataFrame:
    """Estimate CATE for each subgroup."""
    from doubleml import DoubleMLData, DoubleMLPLR
    
    results = []
    for group_val in sorted(data[group_col].unique()):
        subset = data[data[group_col] == group_val]
        dml_data = DoubleMLData(subset, y_col=y_col, d_cols=d_col, x_cols=x_cols)
        dml = DoubleMLPLR(dml_data, clone(ml_l), clone(ml_m), n_folds=n_folds)
        dml.fit()
        ci = dml.confint()
        results.append({
            'group': group_val,
            'n': len(subset),
            'ate': dml.coef[0],
            'se': dml.se[0],
            'ci_lower': ci.iloc[0, 0],
            'ci_upper': ci.iloc[0, 1]
        })
    
    return pd.DataFrame(results)
