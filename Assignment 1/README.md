# 📊 The Cost of Living Crisis: A Data-Driven Analysis

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FRED API](https://img.shields.io/badge/Data-FRED%20API-green.svg)](https://fred.stlouisfed.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A macroeconomic analysis revealing how official inflation metrics systematically understate the true cost burden on college students.**

**Author:** Zehan Qin | **Course:** ECON 5200 | **Date:** January 2026

---

## 🎯 The Problem

The Consumer Price Index (CPI) is the gold standard for measuring inflation—but **whose inflation?**

The BLS constructs the CPI using a market basket weighted toward typical American household consumption. For college students, this basket is fundamentally misaligned:

| What CPI Measures | What Students Actually Pay |
|-------------------|---------------------------|
| Mortgages | Rent in college towns |
| New vehicles | Tuition & fees |
| General groceries | Dining out / meal plans |
| Cable TV | Streaming subscriptions |

When policymakers cite "3% inflation," they're describing an economic reality that **doesn't exist** for 20 million American students.

---

## 🔬 Methodology

### Data Sources (FRED API)

```python
from fredapi import Fred
fred = Fred(api_key='*')

# Data pulled from Federal Reserve Economic Data
official_cpi = fred.get_series('CPIAUCSL')        # National CPI
tuition = fred.get_series('CUSR0000SEEB')         # College Tuition & Fees
rent = fred.get_series('CUSR0000SEHA')            # Rent of Primary Residence
food_away = fred.get_series('CUSR0000SEFV')       # Food Away from Home
streaming = fred.get_series('CUSR0000SERA02')     # Cable/Streaming Services
boston_cpi = fred.get_series('CUURA103SA0')       # Boston Metro CPI
```

### Student Price Index (SPI) Construction

I built a **Laspeyres fixed-weight index** using student-specific expenditure weights:

```
SPI = (0.45 × Tuition) + (0.25 × Rent) + (0.25 × Food Away) + (0.05 × Streaming)
```

| Component | FRED Code | Weight | Rationale |
|-----------|-----------|--------|-----------|
| Tuition & Fees | CUSR0000SEEB | 45% | Dominant student expense |
| Rent | CUSR0000SEHA | 25% | Housing in college markets |
| Food Away from Home | CUSR0000SEFV | 25% | Dining out / meal plans |
| Streaming Services | CUSR0000SERA02 | 5% | Digital entertainment |

### Critical Step: Base Year Normalization

All series re-indexed to **January 2016 = 100** for valid comparison:

```python
base = df.loc['2016-01-01':].iloc[0]
df_index = (df / base) * 100
```

> ⚠️ **Why this matters:** Raw BLS indices use different base periods (1982-84, 2002, etc.). Comparing them directly is a "data crime" that produces misleading conclusions.

---

## 📈 Key Findings

### Finding 1: The Student-National Inflation Gap

```
┌─────────────────────────────────────────────────────────┐
│  MY ANALYSIS REVEALS A ~20 PERCENTAGE POINT DIVERGENCE  │
│  BETWEEN STUDENT COSTS AND NATIONAL INFLATION           │
└─────────────────────────────────────────────────────────┘
```

| Index | Latest Value | Cumulative Growth (2016-2024) |
|-------|--------------|-------------------------------|
| National CPI | ~123 | +23% |
| Boston CPI | ~126 | +26% |
| **Student SPI** | **~143** | **+43%** |

**Students experience nearly 2x the inflation rate** compared to headline CPI.

### Finding 2: Component Breakdown

```
Chipotle Burrito:  ████████████████████████████ 53.33%
Rent (1 Bed):      █████████████████████████    50.00%
Tuition:           ██████████████               28.89%
Spotify:           ██████████                   20.02%
```

### Finding 3: Regional Amplification (Boston)

The Boston-Cambridge-Newton metro CPI consistently exceeds national averages, creating a **compounding penalty** for students in high-cost educational hubs.

---

## 📊 Visualizations

### 1. Normalized Cost of Living Series
![Cost of Living](images/cost_of_living_normalized.png)
*Five components normalized to Jan 2016 = 100*

### 2. Student SPI vs Official CPI
![SPI vs CPI](images/spi_vs_cpi_comparison.png)
*Shaded region shows the growing divergence*

### 3. Regional Disparity Analysis
![Regional Analysis](images/regional_disparity_analysis.png)
*National CPI (grey) vs Boston CPI (blue) vs Student SPI (red)*

---

## 🛠️ Technical Stack

```
python >= 3.12
├── fredapi          # Federal Reserve data access
├── pandas           # Data manipulation & time series
├── matplotlib       # Visualization
└── numpy            # Numerical operations
```

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/student-inflation-analysis.git
cd student-inflation-analysis

# Install dependencies
pip install -r requirements.txt

# Add FRED API key
export FRED_API_KEY='*'

# Run analysis
python main.py
```

---

## 💡 Policy Implications

| Issue | Current Practice | Recommended Change |
|-------|------------------|-------------------|
| Financial Aid | Indexed to headline CPI | Index to education-specific inflation |
| Student Loan Rates | Pegged to general inflation | Account for true student cost burden |
| Tuition Communications | "Below-inflation increases" | Benchmark against student-relevant costs |

---

## 📁 Repository Structure

```
student-inflation-analysis/
│
├── data/
│   └── raw/                    # Downloaded FRED data
│
├── notebooks/
│   └── analysis.ipynb          # Full Jupyter notebook
│
├── src/
│   ├── data_acquisition.py     # FRED API calls
│   ├── index_construction.py   # SPI calculation
│   └── visualization.py        # Plot generation
│
├── images/                     # Generated figures
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🎓 Skills Demonstrated

- **API Integration** — FRED API authentication & time-series extraction
- **Data Wrangling** — Pandas operations, resampling, forward-fill imputation
- **Index Number Theory** — Laspeyres weighting, base-year normalization
- **Data Visualization** — Multi-series plots, annotations, professional styling
- **Economic Analysis** — CPI methodology critique, demographic segmentation

---

## 📬 Contact

**Zehan Qin**

[![Email](https://img.shields.io/badge/Email-Contact-red.svg)](mailto:your.email@example.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com/in/yourprofile)

---

<p align="center">
  <i>If this analysis helped you, consider giving it a ⭐</i>
</p>
