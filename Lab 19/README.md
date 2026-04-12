# Tree-Based Models — Random Forests

## Objective

This project evaluates the predictive performance of tree-based ensemble methods against traditional linear models for housing price estimation, leveraging SHAP-based explainability to distinguish predictive importance from causal inference.

## Dataset

California Housing dataset from scikit-learn: 20,640 observations across 8 features including median income, housing age, average rooms, population, and geographic coordinates.

## Methodology

- Trained and compared four models — Decision Tree, Ridge Regression, Random Forest, and Gradient Boosting Regressor — on an 80/20 train-test split
- Diagnosed a data leakage bug where Random Forest was evaluated on training data (R² = 0.97) instead of test data (R² = 0.80), illustrating the bias-variance tradeoff
- Identified a causal overclaiming flaw in MDI-based policy recommendations: feature importance measures predictive contribution, not causal effect
- Tuned Random Forest hyperparameters via 5-fold GridSearchCV over n_estimators, max_depth, and max_features
- Computed and compared three feature importance methods: MDI, permutation importance, and SHAP values
- Generated SHAP waterfall plots for high-value, low-value, and surprising observations, plus a global beeswarm plot
- Built an interactive four-panel Plotly dashboard displaying model comparison, SHAP global importance, R² vs n_estimators, and MDI/permutation/SHAP ranking comparison

## Key Findings

- **Ridge Regression:** R² = 0.5759, RMSE = 0.7455
- **Default Random Forest:** R² = 0.8062, RMSE = 0.5039
- **Tuned Random Forest:** R² = 0.8147, RMSE = 0.4928 (best params: n_estimators=500, max_features='sqrt')
- **Gradient Boosting:** R² = 0.8288, RMSE = 0.4736
- GBR marginally outperforms tuned RF by 0.0141 in R², though the practical significance is limited
- SHAP analysis confirms MedInc as the dominant predictor; MDI and SHAP diverge on mid-range features due to MDI's known bias toward high-cardinality variables
- Beyond ~200 trees, marginal R² improvement is less than 0.001, suggesting diminishing returns on computational cost

## How to Reproduce

1. `git clone https://github.com/ZehanQin/ECON5200-Applied-Data-Analytics-in-Econ.git`
2. `cd Lab 19`
3. `pip install -r requirements.txt`
4. Open `lab-ch19-diagnostic.ipynb` and run all cells
5. Open `dashboard.html` in a browser to view the interactive Plotly dashboard

## Repository Structure

```
Lab 19/
├── README.md
├── requirements.txt
├── verification-log.md
├── lab-ch19-diagnostic.ipynb
├── dashboard.html
├── src/
│   └── shap_utils.py
└── figures/
    ├── shap_waterfall.png
    ├── shap_beeswarm.png
    ├── feature_importance.png
    └── dashboard_screenshot.png
```

## Tools & Libraries

Python 3.x, scikit-learn, SHAP, Plotly, NumPy, Pandas, Matplotlib

## Course

ECON 5200: Causal Machine Learning & Applied Analytics — Topic 19: Tree-Based Models & Random Forests
