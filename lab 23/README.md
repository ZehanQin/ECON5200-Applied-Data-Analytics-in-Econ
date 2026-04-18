# FedSpeak 2.0 — NLP Pipeline for Central Bank Communications

## Objective
A diagnostic-to-production NLP pipeline that extracts monetary policy signals from FOMC meeting minutes, benchmarking classical bag-of-words features against modern transformer embeddings for Fed regime classification.

## Methodology
- **Pipeline diagnosis & repair:** Identified and corrected three systematic errors in a broken NLP pipeline — a naive whitespace tokenizer that left punctuation attached to tokens, a Harvard General Inquirer sentiment dictionary that misclassifies neutral financial terminology (e.g., "capital", "cost", "tax") as negative, and a TF-IDF configuration with no document-frequency filtering that allowed ubiquitous background terms to dominate the feature space.
- **Preprocessing:** Rebuilt the text cleaning layer using `nltk.word_tokenize` with regex-based non-alphabetic stripping, stopword removal, and WordNet lemmatization.
- **Domain-appropriate sentiment:** Replaced the Harvard GI lexicon with the Loughran-McDonald financial sentiment dictionary, which eliminates the ~73% false-positive rate that GI produces on financial text.
- **Feature engineering:** Configured TF-IDF with `min_df=5`, `max_df=0.85`, and bigrams (`ngram_range=(1,2)`) to capture multi-word financial expressions such as "interest rate" and "labor market" while filtering out noise and non-discriminating background vocabulary.
- **Transformer embeddings:** Encoded each FOMC document with `sentence-transformers/all-MiniLM-L6-v2` to produce 384-dimensional dense semantic vectors.
- **Comparative evaluation:** Benchmarked TF-IDF (reduced to 50 dimensions via TruncatedSVD) against sentence-transformer embeddings on two tasks: (i) unsupervised clustering evaluated by silhouette score and (ii) tightening-regime classification evaluated via `TimeSeriesSplit` cross-validation with logistic regression and AUC-ROC.
- **Reusable module:** Packaged the production pipeline into `src/fomc_sentiment.py`, exposing three documented functions — `preprocess_fomc()`, `compute_lm_sentiment()`, and `build_tfidf_matrix()` — with type hints and a self-test entry point.

## Key Findings
- **TF-IDF outperformed sentence-transformer embeddings** on the downstream prediction task, achieving an AUC of **0.818 ± 0.212** versus **0.721 ± 0.210** for embeddings across time-series cross-validation folds.
- **Clustering quality favored embeddings slightly** (silhouette 0.197 vs 0.168), indicating that dense semantic vectors produce cleaner unsupervised structure, but this advantage did not transfer to supervised classification.
- **Interpretation:** Fed tightening cycles are characterized by a distinctive, repeatable vocabulary — "inflation", "restrictive", "overheating", "firm" — and a high-dimensional sparse representation captures these lexical signals more directly than a 384-dimensional dense compression that prioritizes generic semantic meaning. In short, when the predictive signal lives in specific words, bag-of-words wins; when it lives in meaning, embeddings win. For Fed regime classification, the signal is lexical.
- **Sentiment dictionary choice dominates model choice:** Fixing the domain mismatch (GI → Loughran-McDonald) contributed more signal improvement than upgrading from TF-IDF to transformer embeddings, reinforcing the principle that domain-appropriate feature design beats architectural sophistication in structured financial text.

## Repository Structure
```
lab 23/
├── notebooks/
│   └── lab_ch23_diagnostic.ipynb   # Full diagnostic pipeline with all four parts
├── src/
│   └── fomc_sentiment.py           # Reusable production module
└── README.md
```

## Note on GitHub Rendering
The notebook preview may display as "Invalid Notebook" on GitHub due to a known Colab widget metadata bug (progress bars from model downloads store widget state that GitHub's renderer cannot parse). The `.ipynb` file itself is valid — please download and open in Jupyter/Colab to view all outputs.
