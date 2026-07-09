# 4. Implementation, Coding Standards & Version Control

## 4.1 Coding Standards & Naming Conventions

The codebase rigorously adheres to standard software engineering guidelines across all programming languages:

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

## 4.2 Modular Code & Reusability

To ensure separation of concerns and long-term maintainability, the codebase is partitioned into reusable packages:

```
carbon-heist-mitigation/
├── application/             # Presentation Layer
│   ├── app.py               # Interactive Streamlit Web App
│   ├── input.xlsx           # Production test case harness
│   └── results.csv          # Output verification matrix
├── data/                    # Data Engineering & ETL Pipeline
│   ├── Clean_Data_Pipeline.py # Modular 8-step data cleaning engine
│   └── sample_nyc_energy.xlsx # Cleaned reference artifact
├── database/                # Persistence & Data Definition Layer
│   ├── carbon_heist_schema_mysql.sql # MySQL / PostgreSQL DDL
│   ├── carbon_heist_schema_mssql.sql # Microsoft SQL Server T-SQL DDL
│   └── NYC_Energy_Chen_ERD.drawio    # ERD Architectural Diagram
├── models/                  # Artificial Intelligence & Prediction Layer
│   ├── train_ll97_model.py  # Model training script
│   ├── ll97_playground.py   # Terminal diagnostic playground
│   ├── ll97_model.joblib    # Serialized Random Forest weights
│   └── ll97_encoders.joblib # Serialized categorical encoders
└── Excel Project/           # Financial Domain Engine
    └── Co2 Project.xlsx     # 13-sheet domain & scenario reference
```

---

## 4.3 Security & Error Handling

- **Data Validation:** All external user inputs in `app.py` and `ll97_playground.py` are wrapped in type coercion blocks (`float()`, `pd.to_numeric(errors='coerce')`) to prevent unexpected runtime crashes or unhandled exceptions.
- **Outlier Guardrails:** Predictive models enforce physical domain guardrails (`Site EUI < 2000`, `GFA > 0`) to prevent out-of-distribution hallucinations.
- **SQL Injection Prevention:** Database queries and schema definitions utilize strict parameterized schemas rather than string concatenation.

---

## 4.4 Version Control & Collaboration Strategy

### Version Control Repository
- **Platform:** GitHub  
- **Repository Visibility:** Public / Shared Enterprise  
- **URL:** [carbon-heist-mitigation Repository](https://github.com/ahmedadelamin/carbon-heist-mitigation)

### Branching Strategy
- **`main` Branch:** Production-ready codebase containing verified ML weights, complete SQL DDL scripts, and live Streamlit app code.
- **Commit History:** Meaningful atomic commit messages clearly stating technical changes (e.g., `"Sync playground filters with main model"`, `"Rename SQL schema for MySQL and add dedicated schema for Microsoft SQL Server"`).
