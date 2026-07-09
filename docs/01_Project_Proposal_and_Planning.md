# 1. Project Planning & Management

## 1.1 Project Proposal

### Executive Summary & Overview
**Project Name:** Carbon Heist Mitigation & NYC LL97 Decarbonization Intelligence Platform  
**Domain:** Urban Sustainability, Data Science, Machine Learning, and Financial Risk Modeling  
**Target City / Dataset:** New York City Local Law 84 (LL84 Benchmarking) & Local Law 97 (LL97 Carbon Emissions Limits)  

New York City's Local Law 97 (LL97) imposes strict carbon emission limits on buildings over 25,000 square feet starting in 2024, escalating significantly in 2030. Property owners exceeding their statutory carbon thresholds face annual penalties of **$268 per metric ton of CO₂e over the limit**. Across large commercial and residential portfolios, these statutory fines can amount to millions of dollars annually—effectively a recurring "carbon heist" on asset cash flows.

The **Carbon Heist Mitigation Platform** is an end-to-end data engineering, machine learning, and interactive financial decision-support system. It transforms raw municipal energy disclosure records into actionable engineering retrofits, strategic capital expenditure (CAPEX) modeling, and accurate emissions forecasting.

---

### Objectives
1. **Automated Municipal Data Pipeline:** Build a robust ETL pipeline capable of ingesting raw NYC LL84 annual benchmarking datasets (11,000+ properties, 240+ variables), standardizing addresses, imputing missing data, and filtering data integrity alerts.
2. **Predictive Carbon AI Engine:** Train a Random Forest Machine Learning Regression model (`R² = 81.6%`) to forecast building greenhouse gas (GHG) emissions and carbon liability intensity ($/sq. ft.) based on building physical archetypes, size, age, and ENERGY STAR metrics.
3. **Relational Database & Schema Standardization:** Design normalized relational schemas (MySQL/PostgreSQL and dedicated Microsoft SQL Server T-SQL) to store physical asset metadata, annual meter readings, emission facts, and alert diagnostics.
4. **Interactive Executive Decision Dashboard:** Provide real-time UI/UX visual modeling via Streamlit and Plotly to simulate decarbonization playbooks (Surgical Strike, Electrification Push, Retro-commissioning) and evaluate payback horizons.

---

### Project Scope
- **In-Scope:**
  - Automated cleaning and anomaly detection on NYC Open Data (LL84/LL97).
  - Machine learning regression modeling for emission baseline forecasting.
  - Interactive web dashboard (`app.py`) for property owners, sustainability officers, and financial asset managers.
  - Multi-engine SQL relational database schemas.
- **Out-of-Scope:**
  - Real-time IoT hardware sensor integration inside individual buildings.
  - Automated legal filing or municipal penalty dispute generation with NYC Department of Buildings (DOB).

---

## 1.2 Project Plan & Timeline (Gantt Chart)

```mermaid
gantt
    title Implementation Timeline & Project Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d
    section 1. Architecture
    Requirements & Scope         :a1, 2026-05-01, 10d
    Database Schema & ERD        :a2, 2026-05-12, 10d
    section 2. Data Pipeline
    ETL Script & Cleaning        :b1, 2026-05-22, 12d
    Audit Validation & Report    :b2, 2026-06-04, 7d
    section 3. AI Modeling
    Feature Engineering          :c1, 2026-06-11, 8d
    Random Forest Training       :c2, 2026-06-19, 8d
    section 4. Web Dashboard
    Streamlit UI                 :d1, 2026-06-27, 8d
    Plotly Charts                :d2, 2026-07-05, 6d
    section 5. Deployment
    QA & Documentation           :e1, 2026-07-11, 5d
```

#### Detailed Milestone Breakdown
| Phase | Key Milestone / Deliverable | Target Date | Duration |
| :--- | :--- | :---: | :---: |
| **Phase 1: Architecture** | Complete Stakeholder Requirements & Relational ERD (`carbon_heist_schema_mysql.sql`) | May 22, 2026 | 22 Days |
| **Phase 2: Data Engineering** | Execute Data Cleaning Pipeline & PDF Report (`sample_nyc_energy.xlsx`) | Jun 12, 2026 | 21 Days |
| **Phase 3: AI & Predictive Modeling** | Train Random Forest Regressor (`ll97_model.joblib`) with $R^2 = 81.6\%$ | Jul 02, 2026 | 20 Days |
| **Phase 4: Web Dashboard** | Deploy Interactive Executive Streamlit App (`app.py`) | Jul 19, 2026 | 17 Days |
| **Phase 5: Deployment & QA** | Conduct End-to-End QA Testing & Publish GitHub Documentation Suite | Jul 24, 2026 | 5 Days |

---

## 1.3 Task Assignment & Roles

| Team Role | Key Responsibilities | Primary Deliverables |
| :--- | :--- | :--- |
| **Lead Data Engineer** | Design and execute ETL pipeline (`Clean_Data_Pipeline.py`); handle missing values, address standardizations, and generate audit trail reports (`LL97_Data_Cleaning_Report.pdf`). | Cleaned datasets (`sample_nyc_energy.xlsx`), ETL scripts. |
| **Database Architect** | Develop relational database architecture, normalizations, DDL scripts (`carbon_heist_schema_mysql.sql`, `carbon_heist_schema_mssql.sql`), and ERD design (`NYC_Energy_Chen_ERD.drawio`). | Normalization schemas, SQL DDL scripts, ERD diagram. |
| **Machine Learning Engineer** | Build predictive models (`train_ll97_model.py`, `ll97_playground.py`), perform train-test validation, evaluate feature weights, and export serialized pipelines (`.joblib`). | Trained Random Forest Regressor (`R² = 81.6%`), encoders. |
| **Full-Stack UI/UX Engineer** | Develop Streamlit dashboard (`app.py`), interactive KPI cards, Plotly visual charts, dark-mode design system, and user simulation sliders. | Interactive Web App, simulation dashboards. |
| **Financial & ESG Domain Specialist** | Structure engineering playbooks (`Co2 Project.xlsx`), calculate LL97 fine thresholds ($268/MT), and design CAPEX reinvestment sensitivity models. | 13-sheet domain reference workbook. |

---

## 1.4 Risk Assessment & Mitigation Plan

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy |
| :---: | :--- | :---: | :---: | :--- |
| **R-01** | **Dirty Municipal Data:** Raw NYC Open Data contains string typos ("Not Available", misspellings of Boroughs/Cities, extreme outliers). | High | High | Implemented multi-step cleaning rules in `Clean_Data_Pipeline.py` including regex-based city normalization, explicit null mappings, and statistical outlier filtering (`Site EUI < 2000`). |
| **R-02** | **Model Overfitting:** Regressor could memorize noisy energy anomalies rather than true building structural trends. | Medium | High | Employed `RandomForestRegressor` with controlled tree depth (`max_depth=20`, `n_estimators=150`) and strict train/test split validation (80/20). |
| **R-03** | **SQL Dialect Incompatibility:** Different enterprise stakeholders use different database engines (MySQL vs Microsoft SQL Server). | Medium | Medium | Created separate, dedicated SQL DDL files (`carbon_heist_schema_mysql.sql` and `carbon_heist_schema_mssql.sql`) ensuring strict engine syntax adherence. |
| **R-04** | **Large File Upload Restrictions:** Exported ML models (`ll97_model.joblib` ~70MB) exceed standard Git HTTP push buffers. | High | Medium | Configured Git buffer (`http.postBuffer 524288000`) and structured lightweight encoder serialization to ensure seamless cloud synchronization. |

---

## 1.5 Key Performance Indicators (KPIs)

1. **ETL Pipeline Data Retention & Accuracy:**
   - **Target:** Retain 100% of legally subject LL97 buildings (GFA ≥ 50,000 sq. ft. in NYC) while achieving 0% null values in critical ML features.
   - **Achieved:** Processed 11,639 fully validated building records with complete data integrity.
2. **Machine Learning Predictive Accuracy:**
   - **Target:** Coefficient of Determination ($R^2$) ≥ 0.75 and Mean Absolute Error (MAE) ≤ 250 MT CO₂e.
   - **Achieved:** **$R^2 = 81.65\%$** and **MAE = 212.99 MT CO₂e**.
3. **Dashboard Interactive Response Time:**
   - **Target:** UI recalculation and chart re-rendering under 1.5 seconds upon slider adjustment.
   - **Achieved:** Sub-second response time (~0.3s) via optimized Streamlit caching and vectorized Pandas calculations.
4. **Regulatory Calculation Precision:**
   - **Target:** Exact mathematical alignment with NYC statutory penalty formula: $\text{Penalty} = \text{Total Emissions} \times 268$.
   - **Achieved:** Verified across 13 engineering scenarios against official Excel financial models.
