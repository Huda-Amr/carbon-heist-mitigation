<div align="center">

[![Prev Document](https://img.shields.io/badge/Prev-Doc_03:_Architecture-181717?style=for-the-badge)](./03_System_Analysis_and_Design.md)&nbsp;
[![Back to Suite](https://img.shields.io/badge/Back_to-Docs_Suite-00FF66?style=for-the-badge&logo=github)](./README.md)&nbsp;
[![Next Document](https://img.shields.io/badge/Next-Doc_05:_Testing_QA-00E5FF?style=for-the-badge)](./05_Testing_and_Quality_Assurance.md)

# 📑 DOC 04 — IMPLEMENTATION & CODING STANDARDS
### *Carbon Heist Mitigation & NYC Local Law 97 Intelligence Platform*

</div>

---

### 🏆 Executive Implementation & Governance Grid

<table>
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
    ROOT["📁 carbon-heist-mitigation/ (Workspace Root)"]:::root --> APP["📁 application/\n• app.py (Streamlit UI)\n• input.xlsx & results.csv"]:::pkg
    ROOT --> DATA["📁 data/\n• Clean_Data_Pipeline.py\n• sample_nyc_energy.xlsx"]:::pkg
    ROOT --> DB["📁 database/\n• carbon_heist_schema_mysql.sql\n• carbon_heist_schema_mssql.sql"]:::pkg
    ROOT --> ML["📁 models/\n• train_ll97_model.py\n• ll97_playground.py & .joblib"]:::pkg
    ROOT --> EXCEL["📁 Excel Project/\n• Co2 Project.xlsx (13 Sheets)"]:::pkg

    classDef root fill:#161B22,stroke:#00FF66,stroke-width:2px,color:#00FF66
    classDef pkg fill:#0D1117,stroke:#30363D,stroke-width:2px,color:#E6EDF3
```

---

## 4.3 Security & Error Handling Architecture

> [!TIP]
> ### **Runtime Exception Shielding**
> All external CLI and UI user inputs pass through explicit numeric type coercion and guardrail checks (`pd.to_numeric(errors='coerce')`) to eliminate unhandled runtime exceptions.

- **Data Validation:** All external user inputs in `app.py` and `ll97_playground.py` are wrapped in type coercion blocks (`float()`, `pd.to_numeric(errors='coerce')`) to prevent unexpected runtime crashes or unhandled exceptions.
- **Outlier Guardrails:** Predictive models enforce physical domain guardrails (`Site EUI < 2000`, `GFA > 0`) to prevent out-of-distribution hallucinations.
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
```

---

<div align="center">

[![Prev Document](https://img.shields.io/badge/Prev-Doc_03:_Architecture-181717?style=for-the-badge)](./03_System_Analysis_and_Design.md)&nbsp;
[![Back to Suite](https://img.shields.io/badge/Back_to-Docs_Suite-00FF66?style=for-the-badge&logo=github)](./README.md)&nbsp;
[![Next Document](https://img.shields.io/badge/Next-Doc_05:_Testing_QA-00E5FF?style=for-the-badge)](./05_Testing_and_Quality_Assurance.md)

</div>
