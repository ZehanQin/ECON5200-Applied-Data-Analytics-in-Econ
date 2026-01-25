# The Cost of Living Crisis: A Data-Driven Analysis

**Why the "Average" CPI Fails Students**

---

## 📌 The Problem

The Consumer Price Index (CPI) is the headline number used to measure inflation—but whose inflation is it actually measuring?

As a student, I noticed my lived expenses were rising faster than the 3-4% annual inflation reported in the news. Tuition keeps climbing. Rent is skyrocketing. Even a Chipotle burrito costs 53% more than it did in 2016. Yet policymakers and economists point to the "official" CPI as if it represents everyone equally.

**It doesn't.**

The CPI is a weighted average based on the spending habits of a typical urban household. But students aren't typical—we spend disproportionately on tuition, rent, and food away from home, categories that have dramatically outpaced headline inflation.

---

## 🔬 Methodology

### Data Sources
- **FRED API** (Federal Reserve Economic Data) for official price indices
- Manual price tracking for student-specific items

### Technical Approach
- **Language:** Python
- **Libraries:** `pandas`, `matplotlib`, `fredapi`
- **Index Theory:** Laspeyres Price Index methodology

### The Laspeyres Approach

I constructed a custom **Student Price Index (SPI)** using fixed base-period weights that reflect actual student spending patterns:

| Category | Weight | FRED Series |
|----------|--------|-------------|
| Tuition & Fees | 45% | CUSR0000SEEB |
| Rent | 25% | CUSR0000SEHA |
| Food Away from Home | 25% | CUSR0000SEFV |
| Streaming/Cable | 5% | CUSR0000SERA02 |

All indices were normalized to a common base year (January 2016 = 100) to enable valid comparisons—a critical step that many analyses overlook.

---

## 📊 Key Findings

### The Divergence is Real

> **My analysis reveals a 40.4% cumulative increase in student costs since 2016, compared to just 37.2% for the national CPI—a 3.2 percentage point gap that compounds year over year.**

### Individual Category Inflation (2016-2024)

| Item | Inflation Rate |
|------|---------------|
| Chipotle Burrito | +53.33% |
| Rent (1-Bedroom) | +50.00% |
| Tuition | +28.89% |
| Spotify | +20.02% |

### Cumulative Growth Summary (Jan 2016 – Present)

| Index | Value | Growth |
|-------|-------|--------|
| Student SPI | 140.4 | **+40.4%** |
| National CPI | 137.2 | +37.2% |
| Boston CPI | 135.3 | +35.3% |

### Visual Evidence

The divergence between the Student SPI and Official CPI becomes strikingly clear when visualized. The shaded region in the comparison chart represents the "hidden inflation" students experience but that never makes the headlines.

---

## 🚫 A Note on Data Integrity

Comparing raw indices with different base years is what I call a **"data crime."** Each index series uses a different reference point (1982 vs 2002, for example), making direct comparisons meaningless. The solution is normalization—setting a common base year so all series start at 100 and changes can be compared apples-to-apples.

---

## 💡 Implications

1. **Policy Blind Spots:** Cost-of-living adjustments (COLAs) tied to headline CPI systematically undercompensate students and young workers.

2. **Financial Planning:** Students budgeting based on reported inflation rates will consistently underestimate their true cost increases.

3. **Regional Variation:** Even Boston's CPI (+35.3%) understates what students in the area actually experience (+40.4%).

---

## 🛠️ Repository Structure

```
├── notebooks/
│   └── cost_of_living_analysis.ipynb
├── data/
│   └── student_basket.csv
├── visualizations/
│   ├── cost_of_living_normalized.png
│   ├── student_spi_vs_cpi.png
│   └── regional_disparity.png
└── README.md
```

---

## 🚀 How to Reproduce

```bash
# Clone the repository
git clone https://github.com/[username]/cost-of-living-analysis.git

# Install dependencies
pip install pandas matplotlib fredapi

# Add your FRED API key
# Get one free at: https://fred.stlouisfed.org/docs/api/api_key.html

# Run the notebook
jupyter notebook notebooks/cost_of_living_analysis.ipynb
```

---

## 📚 References

- Bureau of Labor Statistics. *Consumer Price Index*.
- Federal Reserve Bank of St. Louis. *FRED Economic Data*.
- Laspeyres, E. (1871). Price index methodology.

---

## 👤 Author

**Zehan Qin**  
Economics 5200 | Quantitative Methods  
*January 2026*

---

*If this analysis resonated with you, consider starring ⭐ the repository.*
