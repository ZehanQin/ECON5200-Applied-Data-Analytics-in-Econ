# Lab 22 — Unsupervised Learning: Clustering & Dimensionality Reduction

> **ECON 5200 · Causal Machine Learning & Applied Analytics**

## Objective

A diagnosis-first unsupervised learning workbench that debugs a broken K-Means pipeline on World Bank Development Indicators, extends the analysis to customer segmentation with PCA vs UMAP comparison, and packages the workflow into a reusable `clustering_utils.py` module suitable for production reuse.

## Methodology

- **Pipeline diagnosis**: Identified and fixed four planted errors — missing `StandardScaler`, incorrect parameter name (`k=4` instead of `n_clusters=4`), PCA applied before standardization, and missing `random_state` for reproducibility.
- **Corrected clustering workflow**: Standardized 9 WDI indicators across 237 countries with `StandardScaler`, fit `KMeans(n_clusters=4, random_state=42)`, projected to 2D via `PCA` for visualization.
- **Customer segmentation extension**: Applied the corrected pipeline to synthetic behavioral data (2,000 customers × 6 features, 4 latent segments generated via `make_blobs`), then compared linear (PCA) and nonlinear (UMAP) dimensionality reduction side-by-side.
- **Reusable module**: Built `src/clustering_utils.py` with three typed, documented functions — `run_kmeans_pipeline()`, `evaluate_k_range()`, `plot_pca_clusters()` — plus a `__main__` self-test using synthetic blobs.
- **Hierarchical clustering comparison**: Fit `AgglomerativeClustering(linkage='ward')`, plotted the dendrogram, and cross-tabulated against K-Means labels to validate cluster stability across algorithms.

## Key Findings

- **Standardization is dispositive for distance-based clustering.** On raw WDI data, PC1 absorbed ~90% of variance (a GDP-per-capita proxy); after z-score scaling, PC1 explained **43.8%** — confirming that multiple features now contribute meaningfully to the embedding.
- **K = 4 yields balanced, interpretable country clusters** with silhouette score **0.1916** (inside the 0.15–0.40 target band for real-world heterogeneous data). Cluster sizes: `[43, 92, 56, 46]`.
- **UMAP visibly outperforms PCA on separating latent segments** for the customer data, consistent with its advantage on non-linearly separable structure — PCA's best linear projection smears the four true segments along PC1, while UMAP pulls them into visibly distinct neighborhoods.
- **K-Means and Ward agglomerative clustering converge on similar partitions**, as expected when both optimize a WCSS-style objective. Agglomerative silhouette (**0.2244**) slightly exceeds K-Means on this dataset, and cross-tabulation shows one cluster with 53 overlapping countries across both methods.

## Repository Layout

    lab 22/
    ├── README.md
    ├── requirements.txt
    ├── notebooks/
    │   └── lab_ch22_diagnostic.ipynb
    └── src/
        └── clustering_utils.py

## How to Reproduce

    git clone https://github.com/ZehanQin/ECON5200-Applied-Data-Analytics-in-Econ.git
    cd ECON5200-Applied-Data-Analytics-in-Econ/lab\ 22
    pip install -r requirements.txt
    jupyter notebook notebooks/lab_ch22_diagnostic.ipynb

## Verification Checkpoints

| Check | Target | Result |
|---|---|---|
| Four errors identified + explained | Yes | ✅ |
| Standardized means ≈ 0, std ≈ 1 | Yes | ✅ |
| PC1 variance (standardized) | 35–50% | **43.8%** ✅ |
| Silhouette score (K = 4) | 0.15–0.40 | **0.1916** ✅ |
| Cluster sizes balanced | Yes | [43, 92, 56, 46] ✅ |
| UMAP vs PCA comparison plotted | Yes | ✅ |
| Module self-test passes | Yes | ✅ |
| Hierarchical clustering + dendrogram | Yes | ✅ |

## Note

Cell 2 was modified because the World Bank API now returns only one column when `labels=True`, and `mrv=1` produces indicator-year misalignment that causes `dropna` to drop all countries. Switched to `time=2022` and added `feature_names = [v for v in indicators.values() if v in df.columns]` to skip missing indicators (e.g. CO2). All other instructor code unchanged.

## Tech Stack

Python 3.10+ · pandas · numpy · scikit-learn · umap-learn · scipy · wbgapi · matplotlib · seaborn

---

*Course:* ECON 5200 — Graduate Applied Econometrics  
*Topic 22 of 26:* Unsupervised Learning — Clustering & Dimensionality Reduction
