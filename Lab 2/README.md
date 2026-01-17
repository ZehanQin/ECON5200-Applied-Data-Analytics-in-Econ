# Lab 2: The Illusion of Growth & The Composition Effect

## Objective

This project builds a Python data pipeline to ingest live economic data from the Federal Reserve Economic Data (FRED) API, enabling real-time analysis of U.S. wage trends spanning over 50 years. The primary goals were to investigate the phenomenon of wage stagnation, visualize the "Money Illusion" (the gap between nominal and inflation-adjusted wages), and identify and correct for statistical biases that distort labor market metrics.

## Tech Stack

- **Python** — Core programming language
- **fredapi** — FRED API wrapper for fetching economic time series
- **pandas** — Data manipulation and time series alignment
- **matplotlib** — Visualization of wage trends and anomalies

## Methodology

### 1. Data Ingestion & Real Wage Calculation
Connected to the FRED API to fetch two primary series:
- **AHETPI** — Average Hourly Earnings of Production and Nonsupervisory Employees (Nominal Wages)
- **CPIAUCSL** — Consumer Price Index for All Urban Consumers (Inflation Measure)

Calculated real wages by deflating nominal earnings against CPI, rebasing to a common year to enable meaningful historical comparison.

### 2. Anomaly Detection: The 2020 Spike
Time series visualization revealed an unexpected sharp increase in average wages during Q2 2020—seemingly contradicting the economic devastation of the pandemic. This anomaly warranted further investigation.

### 3. Composition Effect Correction
To diagnose whether the spike reflected genuine wage growth or statistical artifact, I fetched an additional series:
- **ECIWAG** — Employment Cost Index (Wages and Salaries)

The ECI uses *fixed employment weights*, meaning it tracks wage changes for the same jobs over time rather than recalculating based on who is currently employed. By comparing standard average wages against the ECI, I isolated the **Composition Effect**—the distortion caused by changes in workforce composition rather than actual wage increases.

## Key Findings

### The Money Illusion
Despite nominal wages rising steadily since 1964, real purchasing power has remained essentially flat for production workers. The visual divergence between nominal and real wage curves starkly illustrates why "getting a raise" often fails to translate into improved living standards.

### The Pandemic Paradox
The apparent 2020 wage boom was not a boom at all. When millions of low-wage workers in hospitality, retail, and service industries lost their jobs, the *average* wage mechanically increased—not because remaining workers earned more, but because lower earners disappeared from the calculation.

The ECI, immune to this compositional shift, showed steady, unremarkable growth through the same period. This confirmed the spike was a **statistical artifact** of workforce composition changes, not evidence of increased labor demand or employer generosity.

This analysis demonstrates a critical lesson in economic data literacy: aggregate statistics can mislead when the underlying population changes, and proper controls (like the ECI) are essential for accurate interpretation.
