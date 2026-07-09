# 6. User Manual, Deployment & Execution Guide

## 6.1 System Requirements & Hardware Dependencies

To execute the **Carbon Heist Mitigation Platform** locally, the system requires the following environment:
- **Operating System:** Windows 10/11, macOS 11+, or Linux (Ubuntu 20.04+)
- **Python Environment:** Python 3.10+
- **Memory (RAM):** 4 GB minimum (8 GB recommended for fast pandas workbook manipulation)
- **Disk Space:** 500 MB free space (including raw Excel datasets and serialized ML models)

---

## 6.2 Installation Steps & Configuration Guide

### 1. Clone Repository
Open your command terminal or PowerShell and clone the official project repository:
```bash
git clone https://github.com/ahmedadelamin/carbon-heist-mitigation.git
cd carbon-heist-mitigation
```

### 2. Install Python Dependencies
Install all required libraries using `pip`:
```bash
pip install pandas numpy scikit-learn openpyxl streamlit plotly joblib fpdf2
```

---

## 6.3 Execution Guide (Running Locally)

### Option A: Launch Interactive Executive Web Dashboard (Streamlit)
To start the production web interface for real-time portfolio modeling:
```bash
cd application
streamlit run app.py
```
*The dashboard will automatically open in your default browser at `http://localhost:8501`.*

### Option B: Run AI Predictive Playground in Terminal
To interactively test building archetypes in your command line:
```bash
cd models
python ll97_playground.py
```

### Option C: Execute Automated Data Cleaning Pipeline
To regenerate the clean dataset (`sample_nyc_energy.xlsx`) from raw LL84 spreadsheets:
```bash
cd data
python Clean_Data_Pipeline.py
```

---

## 6.4 Step-by-Step End User Manual

### Navigating the Executive Streamlit Dashboard (`app.py`)
1. **Sidebar Controls (Asset Profile Setup):**
   - Use the sidebar controls to choose the building **Borough** (Manhattan, Queens, Brooklyn, Bronx, Staten Island).
   - Select the **Primary Property Type** (e.g., Office, Multifamily Housing, Retail Store).
   - Set the **Year Built** and **Gross Floor Area (GFA)** slider.
2. **Review Real-Time KPI Cards:**
   - **AI Predicted Emissions:** View annual greenhouse gas footprint in Metric Tons CO₂e.
   - **Carbon Liability ($/sqft):** Inspect your financial risk exposure under NYC Local Law 97 statutory fine rates ($268/MT).
   - **Peer Benchmark Gap:** See immediately whether your asset outperforms or lags behind similar buildings across New York City.
3. **Simulate Engineering Retrofit Playbooks:**
   - Navigate to the **Decarbonization Simulation** section to model HVAC retro-commissioning, window/envelope insulation, and electrification upgrades to calculate your annual penalty savings.

---

## 6.5 Database Initialization Guide

To initialize the relational schema in your SQL server:
- **For MySQL / PostgreSQL:** Execute `database/carbon_heist_schema_mysql.sql`
- **For Microsoft SQL Server (T-SQL):** Execute `database/carbon_heist_schema_mssql.sql`
