import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance


def explain_prediction(model, X: pd.DataFrame, idx: int) -> None:
    """Generate SHAP waterfall plot for a single observation.
    
    Args:
        model: Fitted tree-based model.
        X: Feature matrix (DataFrame).
        idx: Row index to explain.
    """
    explainer = shap.TreeExplainer(model)
    explanation = explainer(X.iloc[[idx]])
    shap.plots.waterfall(explanation[0])


def global_importance(model, X: pd.DataFrame) -> None:
    """Generate SHAP beeswarm plot for global feature importance.
    
    Args:
        model: Fitted tree-based model.
        X: Feature matrix (DataFrame).
    """
    explainer = shap.TreeExplainer(model)
    explanation = explainer(X[:300])
    shap.plots.beeswarm(explanation)


def compare_importance(model, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """Compare MDI vs Permutation vs SHAP importance rankings.
    
    Args:
        model: Fitted tree-based model.
        X: Feature matrix (DataFrame).
        y: Target values.
    Returns:
        DataFrame with three importance rankings side by side.
    """
    mdi = pd.Series(model.feature_importances_, index=X.columns)

    perm = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    perm_imp = pd.Series(perm.importances_mean, index=X.columns)

    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(X[:300])
    shap_imp = pd.Series(np.abs(shap_vals).mean(axis=0), index=X.columns)

    result = pd.DataFrame({
        'MDI': mdi,
        'Permutation': perm_imp,
        'SHAP': shap_imp
    }).sort_values('SHAP', ascending=False)

    print(result.round(4))
    return result


if __name__ == "__main__":
    from sklearn.datasets import fetch_california_housing
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split

    data = fetch_california_housing()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    explain_prediction(rf, X_test, 0)
    global_importance(rf, X_test)
    compare_importance(rf, X_test, y_test)