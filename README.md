# FUTURE_DS_01: Business Sales Performance Analytics

[![Track: Data Science & Analytics](https://img.shields.io/badge/Track-Data%20Science%20%26%20Analytics-blue.svg)](https://futureinterns.com/)
[![Project: Task 01](https://img.shields.io/badge/Task-01%20Sales%20Analytics-brightgreen.svg)](https://futureinterns.com/data-science-analytics-task-1-2026/)
[![Internship: Future Interns](https://img.shields.io/badge/Organization-Future%20Interns-orange.svg)](https://futureinterns.com/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

---

## 📌 Executive Overview
In this enterprise data analytics project, a multi-year commercial dataset (6,200 orders across 2023–2025) was cleaned, analyzed, and synthesized into strategic business insights. The analytical deliverables evaluate longitudinal revenue trajectories, margin health, catalog performance, geographic variation, discount elasticity, and customer segmentation to provide C-suite stakeholders with clear growth strategies.

---

## 📊 Core Performance Metrics (Executive Scorecard)

| Key Metric | Audited Value | Business Impact |
| :--- | :--- | :--- |
| **Total Net Sales** | **\$7,195,605.56** | Exceeded baseline milestone by +5.82% |
| **Gross Operating Profit** | **\$2,166,158.76** | Strong commercial bottom line (+14.01% favorable) |
| **Consolidated Margin** | **30.10%** | Healthy 30%+ overall gross margin |
| **Fulfilled Orders** | **6,200 Orders** | Distributed across 4 continental US regions |
| **Active Client Accounts** | **850 Accounts** | Strong recurring B2B & consumer relationships |
| **Average Order Value (AOV)** | **\$1,160.58** | Driven by enterprise technology procurement |

---

## 🔍 Key Findings & Analytical Highlights

1. **Longitudinal Trajectory & Seasonality:**
   - Commercial demand peaks in **Q4 (November & December)** reaching up to \$251k/month due to holiday sales and corporate budget clearing.
   - February represents an annual lull (\$133k - \$180k), signaling an ideal window for marketing campaigns and inventory realignment.

2. **Catalog Margin Divergence (Loss Leader Identification):**
   - **Technology** generates 69.1% of gross revenue (\$4.97M) at an average margin of **32.65%**.
   - **Office Supplies** carries the company's highest profit margins (**40.24%**).
   - **Furniture** exhibits severe margin compression: `Tables` (3.66% margin) and `Bookcases` (3.79% margin) are suffering from deep discounting and shipping overhead.

3. **Geographic Regional Breakdown:**
   - South leads in margin efficiency (**31.03%** profit margin), followed by West (**30.70%**) and East (**30.07%**).
   - **Central** lags at **28.54%** margin, driven by elevated shipping duration and discount practices.

4. **Discounting Elasticity:**
   - Transactions discounted above **20%** have an 82% likelihood of delivering zero or negative net profit margin.

---

## 📁 Repository Structure

```text
FUTURE_DS_01/
├── dashboards/
│   ├── interactive_dashboard.html      # Responsive interactive executive web dashboard
│   ├── sales_analytics_workbook.xlsx   # Client-ready Excel workbook with multi-tab models
│   └── sales_metrics.json              # Structured KPI JSON payload
├── data/
│   ├── raw_sales_data.csv              # Original uncleaned transaction log
│   └── cleaned_sales_data.csv          # Feature-engineered & standardized dataset
├── notebooks/
│   └── sales_performance_analysis.ipynb# Step-by-step EDA & visualization notebook
├── reports/
│   ├── sales_performance_report.md     # Full C-level analytical report
│   └── figures/
│       ├── 01_revenue_and_profit_monthly_trend.png
│       ├── 02_top_10_products_revenue.png
│       ├── 03_category_subcat_profit_margins.png
│       ├── 04_regional_performance_breakdown.png
│       ├── 05_discount_vs_profitability_scatter.png
│       └── 06_customer_segment_analysis.png
├── src/
│   ├── data_preprocessing.py           # Ingestion, validation & feature pipeline
│   ├── sales_analytics.py              # KPI calculation engine
│   └── generate_visualizations.py      # Matplotlib/Seaborn chart generation
├── requirements.txt                    # Python runtime dependencies
└── README.md                           # Documentation & execution guide
```

---

## 🚀 Setup & Reproduction Guide

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/<your-username>/FUTURE_DS_01.git
cd FUTURE_DS_01
pip install -r requirements.txt
```

### 2. Run Data Cleaning & Analytics Pipeline
```bash
python src/data_preprocessing.py
python src/sales_analytics.py
python src/generate_visualizations.py
```

### 3. View the Interactive Dashboard
Open `dashboards/interactive_dashboard.html` in any web browser to view the real-time interactive charts, KPI cards, and strategic executive summary.

---

## 🎯 Strategic Recommendations
- **Discount Ceiling:** Enforce a hard cap of 15% discount on `Furniture`, especially `Tables` and `Bookcases`.
- **Cross-Sell Bundling:** Package high-demand Technology hardware with high-margin (40%+) Office Supplies.
- **Regional Optimization:** Audit Central region logistics to recover ~250 bps in profit margin.

---
**Future Interns Data Science & Analytics Internship (2026)**  
Official Submission for Task 1: Business Sales Performance Analytics
