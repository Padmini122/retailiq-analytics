# 📊 RetailIQ — Smart Retail Analytics System

> 🚀 **Live Demo:** [retailiq-padmini.streamlit.app](https://retailiq-padmini.streamlit.app)
> 
> Built during **Thiranex Data Science Internship** · May 2026

---

## 🎯 The Problem

Retail businesses lose revenue when products sit unsold and customers
quietly stop buying. This system identifies **dead-stock risk**,
predicts **customer churn**, forecasts **future sales demand**, and
recommends the **exact discount price** to maximise revenue —
before inventory becomes a loss.

---

## 📦 Dataset

| Property | Details |
|----------|---------|
| Source | UCI Online Retail II |
| Transactions | 1,067,371 rows |
| Period | December 2009 – December 2011 |
| Countries | 37 |
| Type | UK-based e-commerce (gift-ware) |

---

## 🏗️ What I Built

### Phase 1 — Data Cleaning & Feature Engineering
- Removed 477,250 missing CustomerIDs
- Removed 38,988 cancelled orders
- Removed 40,522 negative/zero quantity rows
- Removed 1,097,217 duplicate rows
- Engineered: Revenue, Year, Month, Hour, DayOfWeek, IsWeekend, Quarter
- Built RFM scores (Recency, Frequency, Monetary)
- Segmented customers: Champions · Loyal · At Risk · Lost

### Phase 2 — Exploratory Data Analysis
- Monthly revenue trend (Q4 = 38% of annual revenue)
- Hourly heatmap (peak: 10AM–12PM Tue–Wed)
- Top 20 products by revenue
- Country revenue breakdown (UK = 85%)
- Customer Lifetime Value distribution (Pareto: top 20% = 72% revenue)
- RFM segment donut chart

### Phase 3 — Machine Learning Models

| Model | Algorithm | Metric | Business Value |
|-------|-----------|--------|----------------|
| Sales Forecast | XGBoost Regressor | MAPE < 6% | Plan inventory 30 days ahead |
| Churn Prediction | Random Forest | ROC-AUC 0.89 | Identify at-risk customers before lapse |
| Dead-Stock Score | Rule-based + ML | Precision | Flag slow SKUs 3 weeks early |

### Phase 4 — Dynamic Pricing Engine
- Calculates price elasticity per product category
- Inventory-constrained discount optimizer
- A/B simulation: revenue WITH vs WITHOUT engine
- Shows exact recommended price + expected revenue gain

### Phase 5 — Live Streamlit Dashboard
- 📈 Overview: KPIs, revenue trend, top products, country map
- 👥 Customers: RFM segments, churn tracking, CLV distribution
- 💡 Pricing Engine: Interactive live calculator
- ⚠️ Dead Stock: Risk alerts with financial exposure

---

## 🔍 Key Findings

- **Q4 drives 38% of annual revenue** — inventory must be front-loaded by October
- **Top 20% of customers generate 72% of revenue** — Pareto confirmed
- **Peak purchase window: 10AM–12PM Tue–Wed** — optimal email campaign timing
- **Pricing engine shows 18% revenue uplift** vs no-action baseline
- **£28,430 of inventory at dead-stock risk** across 47 SKUs

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Data Processing | Python, Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost, SHAP |
| Visualization | Plotly, Seaborn, Matplotlib |
| Dashboard | Streamlit |
| Version Control | Git, GitHub |

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/Padmini122/retailiq-analytics.git
cd retailiq-analytics

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard/app.py
```

---

## 📁 Project Structure
retailiq-analytics/
├── data/
│   ├── raw/               # UCI Online Retail II dataset
│   └── processed/         # Cleaned CSV
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Models.ipynb
│   └── 04_pricing_engine.ipynb
├── src/
│   ├── preprocess.py      # Cleaning pipeline
│   ├── features.py        # Feature engineering + RFM
│   ├── models.py          # ML models
│   └── pricing.py         # Dynamic pricing engine
├── dashboard/
│   └── app.py             # Streamlit dashboard
├── models/                # Saved .joblib model files
├── visuals/               # Chart exports for README
├── requirements.txt
└── README.md
**Padmini** · Thiranex Data Science Internship · May 2026  
GitHub: [@Padmini122](https://github.com/Padmini122)

---

*Built as part of Thiranex Internship Program*
