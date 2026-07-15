<a id="top"></a>
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=220&section=header&text=APPLICATION%20LAYER%20DASHBOARD&fontSize=46&fontColor=00D2FF&fontAlignY=36&desc=NYC%20Local%20Law%2097%20Decarbonization%20and%20Financial%20Mitigation%20Platform&descAlignY=62&descSize=18&descColor=8B949E" width="100%" alt="Application Layer Dashboard"/>

  <br/>

  <a href="https://carbon-heist-mitigation.streamlit.app/"><img src="https://img.shields.io/badge/🌐%20LIVE%20APP-LAUNCH%20STREAMLIT%20DASHBOARD-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Streamlit App"/></a>&nbsp;
  <a href="https://carbon-heist-mitigation.streamlit.app/"><img src="https://img.shields.io/badge/AI%20Chatbot-Google%20Gemini%202.5%20Flash%20%2B%20Local-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="AI Chatbot"/></a>&nbsp;
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Framework-Streamlit%201.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/></a>&nbsp;
  <a href="https://plotly.com"><img src="https://img.shields.io/badge/Visualizations-Plotly%20Dynamic-3B82F6?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly"/></a>&nbsp;
  <a href="https://scikit-learn.org"><img src="https://img.shields.io/badge/ML%20Inference-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn"/></a>&nbsp;
  <a href="#-dual-theme-design-system"><img src="https://img.shields.io/badge/UI%20Theme-Dual%20Light%20%2F%20Dark-A855F7?style=for-the-badge" alt="Dual Theme UI"/></a>&nbsp;
  <a href="../LICENSE"><img src="https://img.shields.io/badge/Compliance-NYC%20LL97-00F59B?style=for-the-badge" alt="NYC LL97"/></a>

  <br/><br/>

  <em>"Transforming regulatory carbon liabilities into self-funding engineering strategies."</em><br/>
  <strong>NYC Local Law 97 · Portfolio Asset Management & C-Suite Intelligence Platform</strong>

  <br/><br/>
</div>

---

## 🏢 Executive Overview

The **Application Layer (`application/`)** hosts the full-stack, highly interactive **Carbon Heist Mitigation Dashboard (`app.py`)**. Designed specifically for real estate asset owners, C-Suite executives, sustainability directors, and MEP engineers, this dashboard bridges the gap between **raw building energy benchmarking data**, **statutory fine calculations**, **machine learning compliance inference**, and **capital expenditure (CAPEX) financial engineering**.

> [!TIP]
> ### 🌐 **[Launch the Live C-Suite Interactive Dashboard Online](https://carbon-heist-mitigation.streamlit.app/)**
> Access real-time portfolio emissions analysis, slider-driven mitigation simulations, machine learning risk inference, and 5-playbook CAPEX financial engineering directly in your browser without local setup.

```mermaid
flowchart LR
    RAW["📥 NYC LL84 Raw Data\n(Open Data Portal Dump)"]:::raw --> CLEAN["🧹 Forensic Data Hygiene\nCleaning Pipeline → 11,639 Cleaned Records"]:::clean
    CLEAN --> EXCEL["📊 Excel C-Suite Dashboard\n(16-Sheet Financial Model)"]:::excel
    CLEAN --> DATA["📊 input.xlsx / results.csv\nCleaned Portfolio Database"]:::data
    DATA --> CORE["🖥️ Streamlit Core Engine\napp.py Web Dashboard"]:::core
    ML["🤖 ../models/ll97_model.joblib\nRandom Forest Predictor"]:::ml --> CORE
    CORE --> T1["📊 Tab 1: Problem Analysis"]:::tab
    CORE --> T2["🛠️ Tab 2: Mitigation Playground"]:::tab
    CORE --> T3["🤖 Tab 3: ML Predictor"]:::tab
    CORE --> T4["💼 Tab 4: Financial Playbooks"]:::tab
    CORE --> T5["💬 Tab 5: AI Executive Co-Pilot & Chatbot"]:::tab

    classDef raw fill:#0d1526,stroke:#64748b,stroke-width:2px,color:#e2e8f0
    classDef clean fill:#0d1526,stroke:#00E5FF,stroke-width:2px,color:#ffffff
    classDef excel fill:#0d1526,stroke:#FFB800,stroke-width:2px,color:#ffffff
    classDef data fill:#0d1526,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0
    classDef core fill:#0d1526,stroke:#00D2FF,stroke-width:2px,color:#ffffff
    classDef ml fill:#0d1526,stroke:#A855F7,stroke-width:2px,color:#ffffff
    classDef tab fill:#0d1526,stroke:#00F59B,stroke-width:2px,color:#e2e8f0
```

## 💬 Live AI Executive Chatbot & Dual-Engine Interactive Visualization

The application header features an integrated **Executive C-Suite AI Co-Pilot & Chatbot** trained on our complete 11,639-property forensic dataset:

- **🧠 Live Generative AI Mode (Google Gemini 2.5 Flash):** Connect any Google Gemini API key directly in the UI header to enable live C-Suite strategic reasoning. The AI parses any natural-language prompt, computes executive metrics, and dynamically generates custom interactive Plotly visualizations on the fly. Built-in **Multi-Model Auto-Fallback (`Gemini 2.5 -> 2.0 -> 1.5 Flash`)** and exponential backoff retry guarantee high resilience.
- **⚡ Local Quantitative & Charting Engine (Offline/Rate-Limit Safe):** Even without an API key or during API rate limits (`HTTP 429`), our embedded local dataset engine parses natural-language queries (`"top 10 buildings"`, `"multifamily housing"`, `"boroughs"`, `"capex breakdown"`, `"payback horizon"`) and instantly renders both quantitative C-Suite text analysis and interactive Plotly charts directly from our audited `sample_nyc_energy.xlsx` database.

## 📑 Deep-Dive: Analytical Modules (Tabs)

### 1️⃣ Tab 1 — 📊 Problem Analysis & Executive C-Suite Briefing
Provides immediate portfolio-wide situational awareness across filtered NYC properties:
- **Executive KPI Grid**: Displays real-time aggregates for **Total Properties**, **Total GHG Emissions (MT CO₂e)**, **Total Statutory Fine Liability ($B)**, **Avg ENERGY STAR Score**, and **Avoided Emissions**.
- **NYC Borough Analysis (Dual-Axis Chart)**: Visualizes statutory fine exposure ($ bars, left axis) against average carbon intensity (`kgCO₂/ft²` line, right axis) across **Manhattan, Brooklyn, Queens, Bronx, and Staten Island**.
- **Building Age vs. Emission Intensity Scatter**: Incorporates an Ordinary Least Squares (OLS) regression trendline to analyze how infrastructure age correlates with carbon efficiency.
- **Top 10 Carbon Emitters Ledger**: A clean, interactive table highlighting properties with the highest compliance risk, complete with instant search and alert flags.

### 2️⃣ Tab 2 — 🛠️ Mitigation Scenarios & Strategy Playground
Empowers engineers and managers to test decarbonization strategies interactively:
- **Interactive Multi-Slider Simulation**:
  - `S1: Energy Efficiency Shift (0–50%)`: Models envelope insulation, LED retrofits, and EMS controls.
  - `S2: Clean Electrification / PPA Shift (0–80%)`: Models replacing fossil fuels with electric heat pumps or green power purchase agreements.
  - `S3: Deep Envelope Retrofit (0–40%)`: Models complete mechanical and facade overhauls.
- **Interactive Gauge Indicator**: Displays the real-time percentage of total portfolio emissions reduced.
- **Radar Chart Comparison**: Compares holistic physical vs. financial yield across strategies.
- **Return vs. Impact Grouped Bar Chart**: Directly contrasts tons of CO₂e abated versus annual fine savings in dollars.
- **Decarbonization Roadmap**: Interactive timeline illustrating Phase 1 (Audits), Phase 2 (PPAs), and Phase 3 (Deep Retrofits).

### 3️⃣ Tab 3 — 🤖 ML-Powered Property Compliance Predictor
Integrates our trained machine learning models (`models/ll97_model.joblib`) for real-time asset prediction:
- **Custom Property Inference**: Input any building's **Year Built (1800–2026)**, **Gross Floor Area (GFA)**, **ENERGY STAR Score (0–100)**, and **Property Type**.
- **Automated Peer Benchmarking**: Calculates the exact percentage gap between your asset and NYC borough / property archetype averages.
- **Instant Statutory Fine & Compliance Status**: Predicts annual greenhouse gas emissions, statutory penalties ($/year), liability intensity (`$/ft²`), and flags whether the property is **✅ Compliant** or **🚫 Non-Compliant** against NYC Local Law 97 statutory limits.

### 4️⃣ Tab 4 — 💼 Financial Modeling & C-Suite Playbooks

> [!IMPORTANT]
> ### **All Savings Figures Represent Recurring Annual Savings ($ / Year)**
> Every savings value calculated across the dashboard (such as `Annual Fine Savings`, `Annual LL97 Fine Avoided`, and `Annual Penalty Eliminated`) represents **recurring annual fine avoidance and operational cost savings ($ / yr)** generated every single year.

Delivers rigorous capital allocation and financial sensitivity analysis:
- **Grid Shock & Carbon Tax Sensitivity Matrix (Heatmap)**: Models liability intensity (`$/ft²`) under varying statutory rate hikes (**$268, $300, and $350 / MT**) and electrical grid carbon shocks (**+0% to +15%**).
- **5 Strategic Playbooks Payback & CAPEX Comparison**:
  1. *Surgical Strike (Level 2 Audits & Low-Cost Repairs)* — **0.02 yr payback (8 days)**
  2. *Retro-commissioning (RCx & BMS Optimization)* — **3.29 yr payback**
  3. *1960s Smart Scale (LED, VFD Motors & Controls)* — **8.92 yr payback**
  4. *1930s WET Systems (Wastewater Heat Recovery)* — **12.25 yr payback**
  5. *Electrification Push (Fuel Oil #4 to Heat Pumps)* — **10.38 yr payback**
- **Self-Funding Financial Engineering Model**: Demonstrates how ultra-fast payback Phase 1 projects generate immediate operational savings to de-risk and fund deeper capital investments.

### 5️⃣ Tab 5 — 💬 AI Executive Co-Pilot & Chatbot
Delivers a dedicated full-page conversational intelligence center and real-time visualization portal:
- **Dual-Engine Strategic Chat Interface**: Interactive full-width chat terminal where asset owners and sustainability directors can query the entire 11,639-property portfolio in natural English or Arabic (`"What are the top 5 emitting property types across Manhattan?"`, `"Compare CAPEX requirements vs fine savings for 1930s buildings"`).
- **Dynamic On-the-Fly Plotly Chart Generation**: Automatically synthesizes complex quantitative answers into custom, interactive Plotly visualizations (Bar, Pie, Line, and Scatter charts) embedded directly inside the conversation flow.
- **Offline / Rate-Limit Safe Fallback Engine**: If no API key is provided or during rate limits (`HTTP 429`), the local dataset engine seamlessly intercepts queries to compute accurate financial totals, averages, and generate instant charts from `sample_nyc_energy.xlsx` without external connectivity.

---

## 🏛️ Statutory Fine Reference Formula

All calculations inside the dashboard strictly enforce the official NYC statutory penalty structure:

```math
\text{Annual LL97 Penalty} = \text{Total Emissions} \times 268
```

> [!IMPORTANT]
> ### **Statutory Fine = Total Emissions (MT CO₂e) × $268**
> Where **$268 per Metric Ton of CO₂e** is the mandatory fine rate established under NYC Local Law 97.

---

## 📂 Folder Directory & File Descriptions

```text
application/
├── app.py             # Main Streamlit + Plotly full-stack interactive dashboard application
├── input.xlsx         # Cleaned NYC building benchmarking dataset used for filtering & peer analysis
├── results.csv        # Comprehensive compliance ledger containing calculated penalties & intensities
└── README.md          # Technical documentation & dashboard architectural overview
```

| File Name | Role | Description |
| :--- | :--- | :--- |
| **`app.py`** | Application Entry Point | Contains the full UI design tokens, data loaders, sidebar filter logic, ML inference bridges, and Plotly interactive chart generators. |
| **`input.xlsx`** | Benchmarking Database | Processed portfolio dataset with standardized columns (`Property Name`, `Total GHG Emissions`, `Base LL97 Penalty`, `Borough`, `Property Type`, etc.). |
| **`results.csv`** | Compliance Ledger | Pre-computed summary table providing portfolio-wide penalty analytics across building archetypes. |

---

## 🚀 Quickstart & Deployment Guide

### 1️⃣ Prerequisites
Ensure you have Python 3.9+ installed along with the required dependencies:

```bash
pip install streamlit plotly pandas numpy openpyxl joblib scikit-learn
```

### 2️⃣ Running the Dashboard Locally
Navigate to the `application/` directory and launch the Streamlit engine:

```bash
cd application
streamlit run app.py
```

### 3️⃣ Accessing the Interface
- The dashboard will automatically launch in your default browser at **`http://localhost:8501`**.
- **Sidebar & Filters**: The sidebar contains advanced multi-select filters (`City`, `Borough`, `Property Type`, `Building Age`, `ENERGY STAR Score`, and `GHG Emissions`). If collapsed, open it anytime using the toggle arrow (`[ > ]`) at the top left.
- **Theme Switching**: Toggle between **🌙 Dark Mode** and **☀️ Light Mode** directly from the top of the sidebar.

---

<div align="center">

[![Return to Main Repo](https://img.shields.io/badge/🏠%20RETURN%20TO-MAIN%20REPOSITORY%20HOME-00FF66?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ahmedadelamin/carbon-heist-mitigation)&nbsp;
[![Model Docs](https://img.shields.io/badge/🤖%20VIEW-AI%20%26%20ML%20MODELS-A855F7?style=for-the-badge)](../models/README.md)&nbsp;
[![Academic Docs](https://img.shields.io/badge/📑%20VIEW-ACADEMIC%20DOCS%20SUITE-00E5FF?style=for-the-badge)](../Project%20Documentations/README.md)

<br/>

**Carbon Heist Mitigation Platform** · Engineered for NYC Local Law 97 Compliance & Strategic Decarbonization

</div>


---

## 🔗 Explore Other Core Layers of the Project Suite

| Layer | Directory / Deliverable | Strategic Role & Highlights | Documentation Link |
| :---: | :--- | :--- | :---: |
| 📊 **Visual BI Portal** | **`Tableau/Interactive Dashboard.twbx`** | 3-Page Executive C-Suite BI Portal with macro choropleth maps, fine liability breakdowns (`$2.43B`), and mobile C-Suite QR bridging. | [📖 Tableau Docs](../Tableau/README.md) |
| 🌐 **Live Web Application** | **`application/app.py`** | 5-Tab Streamlit & Plotly interactive dashboard powered by dual-engine AI (`Google Gemini 2.5 + Local Engine`). | [📖 Streamlit Docs](../application/README.md) |
| 📑 **Financial Engineering** | **`Excel Project/Co2 Project.xlsx`** | 16-sheet domain reference workbook featuring comprehensive CAPEX payback modeling and WET system thermodynamics. | [📖 Excel Docs](../Excel%20Project/README.md) |
| 🤖 **Predictive AI Engine** | **`models/ll97_model.joblib`** | Random Forest Regressor (`R² = 81.65%`) predicting statutory fine liabilities across 11,639 properties. | [📖 ML Docs](../models/README.md) |
| 🗄️ **Relational Database** | **`database/`** | Normalized 3NF SQL schemas (`MySQL & MSSQL`) and Chen ER diagram enforcing data integrity. | [📖 Database Docs](../database/README.md) |
| 📚 **Academic Suite** | **`Project Documentations/`** | Official 6-part academic deliverables (`Doc 01 - Doc 06`) and comprehensive Word report (`.docx`). | [📖 Academic Suite](../Project%20Documentations/README.md) |

---

> [!NOTE]
> **Multi-Tier Visual Presentation Strategy:** This live Streamlit web dashboard works in tandem with our packaged **Tableau Executive BI Portal (`../Tableau/README.md`)** and **16-Sheet Excel Financial Model (`../Excel Project/README.md`)** to provide comprehensive decision-support across executive boardroom presentations, technical MEP audits, and live online C-Suite portals.
