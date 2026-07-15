<div align="center">

# 📑 DOC 04 — IMPLEMENTATION & CODING STANDARDS
### *Carbon Heist Mitigation & NYC Local Law 97 Intelligence Platform*

[![Prev Document](https://img.shields.io/badge/Prev-Doc_03:_Architecture-181717?style=for-the-badge)](./03_System_Analysis_and_Design.md)&nbsp;
[![Back to Suite](https://img.shields.io/badge/Back_to-Docs_Suite-00FF66?style=for-the-badge&logo=github)](./README.md)&nbsp;
[![Next Document](https://img.shields.io/badge/Next-Doc_05:_Testing_QA-00E5FF?style=for-the-badge)](./05_Testing_and_Quality_Assurance.md)
<br/>
[![Live Streamlit App](https://img.shields.io/badge/🌐%20LIVE_APP-LAUNCH_STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://carbon-heist-mitigation.streamlit.app/)&nbsp;
[![AI Chatbot](https://img.shields.io/badge/AI%20Chatbot-Google%20Gemini%202.5%20%2B%20Local-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://carbon-heist-mitigation.streamlit.app/)

</div>

---

<div align="center">

### 🏆 Executive Implementation & Governance Grid

<table width="100%" align="center">
  <tr>
    <td align="center" width="33%">
      <br/>
      🐍 <strong>Python Standard</strong><br/>
      <h2 style="color: #00FF66;">PEP 8 Strict</h2>
      <em>Modular & Clean Codebase</em>
      <br/><br/>
    </td>
    <td align="center" width="33%">
      <br/>
      🛡️ <strong>Data Guardrails</strong><br/>
      <h2 style="color: #00E5FF;">EUI &lt; 2000</h2>
      <em>Outlier & Null Protection</em>
      <br/><br/>
    </td>
    <td align="center" width="33%">
      <br/>
      🗃️ <strong>SQL Dialects</strong><br/>
      <h2 style="color: #FF4B4B;">Dual Engine</h2>
      <em>MySQL / PG & MSSQL T-SQL</em>
      <br/><br/>
    </td>
  </tr>
</table>

</div>

---

## 4.1 Coding Standards & Naming Conventions

The codebase rigorously adheres to standard software engineering guidelines across all programming languages:

> [!IMPORTANT]
> ### **PEP 8 Compliance & Type Safety**
> All core analytical and data processing modules enforce strict adherence to PEP 8 formatting guidelines, clear function signatures, and comprehensive Google/NumPy docstrings.

### Python Coding Standards (PEP 8)
- **Variable & Function Names:** `snake_case` is used for variables, function names, and module names (`train_strategic_model()`, `file_name`, `sample_nyc_energy.xlsx`).
- **Class Names:** `PascalCase` is used for class definitions (`class PDF(FPDF):`).
- **Constants:** `UPPER_CASE_WITH_UNDERSCORES` is used for design tokens and application thresholds (`COLOR_GREEN = "#10B981"`, `CURRENT_LIMITS`).
- **Docstrings & Comments:** All core analytical functions include explicit Google/NumPy style docstrings defining input parameters, return values, and mathematical formulas.

### SQL Standards
- **Keywords:** Standard DDL/DML keywords are written in uppercase (`CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `ON DELETE NO ACTION`).
- **Table Names:** Plural uppercase nouns representing distinct relational entities (`PROPERTIES`, `EMISSION_METRICS`, `LL97_PENALTIES`).
- **Column Names:** Lowercase `snake_case` with explicit unit suffixes (`site_eui_kbtu_ft2`, `total_ghg_emissions_metric_tons_co2e`).

---

## 4.2 Modular Code Architecture & Package Partitioning

```mermaid
flowchart TD
    ROOT["📁 carbon-heist-mitigation/ (Workspace Root)"]:::root --> APP["📁 application/\n• app.py (Streamlit 5-Tab UI + AI Chatbot)\n• input.xlsx & results.csv"]:::pkg
    ROOT --> DATA["📁 data/\n• Clean_Data_Pipeline.py\n• sample_nyc_energy.xlsx"]:::pkg
    ROOT --> DB["📁 database/\n• carbon_heist_schema_mysql.sql\n• carbon_heist_schema_mssql.sql"]:::pkg
    ROOT --> ML["📁 models/\n• train_ll97_model.py\n• ll97_playground.py & .joblib"]:::pkg
    ROOT --> EXCEL["📁 Excel Project/\n• Co2 Project.xlsx (16 Sheets)"]:::pkg

    classDef root fill:#161B22,stroke:#00FF66,stroke-width:2px,color:#00FF66
    classDef pkg fill:#0D1117,stroke:#30363D,stroke-width:2px,color:#E6EDF3
```

---

## 4.3 Security & Error Handling Architecture

> [!TIP]
> ### **Runtime Exception Shielding & Fallback Intercept**
> All external CLI, UI user inputs, and cloud AI API calls (`Google Gemini`) pass through explicit type coercion (`pd.to_numeric`) and exception-catching guardrails (`try-except`) to eliminate unhandled runtime exceptions.

- **Data Validation:** All external user inputs in `app.py` and `ll97_playground.py` are wrapped in type coercion blocks (`float()`, `pd.to_numeric(errors='coerce')`) to prevent unexpected runtime crashes or unhandled exceptions.
- **Outlier Guardrails:** Predictive models enforce physical domain guardrails (`Site EUI < 2000`, `GFA > 0`) to prevent out-of-distribution hallucinations.
- **Dual-Engine AI Rate-Limit Shielding:** External Google Gemini API calls (`gemini-2.5-flash` / `gemini-2.0-flash`) inside `Tab 5` are wrapped in resilient `try-except` blocks handling API quota limits (`HTTP 429`) and missing keys. Upon encountering cloud exceptions, the system automatically routes the prompt to an internal local quantitative charting engine that queries `sample_nyc_energy.xlsx` and synthesizes exact Plotly visualizations without dropping the user session.
- **SQL Injection Prevention:** Database queries and schema definitions utilize strict parameterized schemas rather than string concatenation.

---

## 4.4 Version Control & Collaboration Workflow

### Version Control Repository
- **Platform:** GitHub  
- **Repository Visibility:** Public Enterprise Repository  
- **URL:** [carbon-heist-mitigation Repository](https://github.com/ahmedadelamin/carbon-heist-mitigation)

### Branching & Release Workflow

```mermaid
gitGraph
    commit id: "Initial Project Setup"
    branch feature/etl-pipeline
    checkout feature/etl-pipeline
    commit id: "Add 8-Step Data Pipeline"
    commit id: "Generate PDF Report"
    checkout main
    merge feature/etl-pipeline id: "Merge ETL Module"
    branch feature/ml-engine
    checkout feature/ml-engine
    commit id: "Train Random Forest Regressor"
    commit id: "Achieve R2 = 81.65%"
    checkout main
    merge feature/ml-engine id: "Merge ML Models"
    branch feature/streamlit-ui
    checkout feature/streamlit-ui
    commit id: "Build Interactive App UI"
    checkout main
    merge feature/streamlit-ui id: "Production Release"
    branch feature/ai-chatbot-tab5
    checkout feature/ai-chatbot-tab5
    commit id: "Integrate Gemini 2.5 Flash SDK"
    commit id: "Build Local Fallback Chart Engine"
    checkout main
    merge feature/ai-chatbot-tab5 id: "Final Suite Release"
```

---

## 4.5 Tableau BI & Visual Analytics Standards
- **Workbook Packaging:** All visual analytics deliverables must be published as Packaged Workbooks (.twbx) embedding the audited sample_nyc_energy.csv dataset to prevent external database path dependencies.
- **Design Aesthetics:** Dashboards strictly adhere to the C-Suite high-contrast palette (#0D1321 Navy background, #FFD700 Gold highlights) with standardized font scaling (Segoe UI / Tableau Semibold).
- **Calculated Field Governance:** Custom formulas across visual sheets must use explicit conditional logic verified against statutory fine boundaries (/MT).

---

<div align="center">

[![Return to Main Repo](https://img.shields.io/badge/🏠%20RETURN%20TO-MAIN%20REPOSITORY-00FF66?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ahmedadelamin/carbon-heist-mitigation)&nbsp;
[![Prev Document](https://img.shields.io/badge/PREV-DOC%2003:%20ARCHITECTURE-181717?style=for-the-badge)](./03_System_Analysis_and_Design.md)&nbsp;
[![Docs Suite](https://img.shields.io/badge/📑%20BACK%20TO-DOCS%20SUITE-181717?style=for-the-badge)](./README.md)&nbsp;
[![Next Document](https://img.shields.io/badge/NEXT-DOC%2005:%20TESTING%20QA-00E5FF?style=for-the-badge)](./05_Testing_and_Quality_Assurance.md)

</div>
