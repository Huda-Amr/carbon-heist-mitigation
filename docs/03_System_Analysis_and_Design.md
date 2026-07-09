<div align="center">

[![Prev Document](https://img.shields.io/badge/Prev-Doc_02:_Requirements-181717?style=for-the-badge)](./02_Requirements_and_Stakeholders.md)&nbsp;
[![Back to Suite](https://img.shields.io/badge/Back_to-Docs_Suite-00FF66?style=for-the-badge&logo=github)](./README.md)&nbsp;
[![Next Document](https://img.shields.io/badge/Next-Doc_04:_Implementation-00E5FF?style=for-the-badge)](./04_Implementation_and_Coding_Standards.md)

# 📑 DOC 03 — SYSTEM ANALYSIS & DESIGN ARCHITECTURE
### *Carbon Heist Mitigation & NYC Local Law 97 Intelligence Platform*

</div>

---

<div align="center">

### 🏆 Executive System Architecture Grid

<table width="100%" align="center">
  <tr>
    <td align="center" width="33%">
      <br/>
      🏗️ <strong>System Blueprint</strong><br/>
      <h2 style="color: #00FF66;">5-Layer Stack</h2>
      <em>ETL, DB, ML, Domain, UI</em>
      <br/><br/>
    </td>
    <td align="center" width="33%">
      <br/>
      🗄️ <strong>Relational Schema</strong><br/>
      <h2 style="color: #00E5FF;">3NF Normalized</h2>
      <em>MySQL + MSSQL Schemas</em>
      <br/><br/>
    </td>
    <td align="center" width="33%">
      <br/>
      🤖 <strong>AI Model Pipeline</strong><br/>
      <h2 style="color: #FF4B4B;">R² = 81.65%</h2>
      <em>RandomForestRegressor</em>
      <br/><br/>
    </td>
  </tr>
</table>

</div>

---

## 3.1 Problem Statement & Software Architecture

### Problem Statement
Municipal carbon disclosure regulations (Local Law 97) present a complex data and financial challenge: raw annual building disclosure data is often incomplete or noisy, and predicting future carbon penalties under varying building operational parameters is difficult. Without a predictive analytical platform, property managers risk paying excessive carbon fines or overspending on unoptimized capital projects.

---

### Software Architecture (Five-Pillar Layered Architecture)

The system is designed as a modular **Layered Decision-Support Architecture** separating ETL processing, relational persistence, predictive AI modeling, and interactive visualization.

```mermaid
graph TD
    subgraph L1 [Layer 1: Data Ingestion & Engineering]
        RAW[Raw NYC LL84 Excel Dataset] --> ETL[Clean_Data_Pipeline.py]
        ETL --> CLEAN[sample_nyc_energy.xlsx]
        ETL --> REPORT[PDF Audit Report]
    end

    subgraph L2 [Layer 2: Relational Database Architecture]
        CLEAN --> SQL_MY[carbon_heist_schema_mysql.sql]
        CLEAN --> SQL_MS[carbon_heist_schema_mssql.sql]
        SQL_MY --> DB[(Normalized Relational Store)]
    end

    subgraph L3 [Layer 3: Machine Learning Engine]
        CLEAN --> TRAIN[train_ll97_model.py]
        TRAIN --> MODEL[ll97_model.joblib]
        TRAIN --> ENC[ll97_encoders.joblib]
        MODEL --> INFER[Inference Engine / Playground]
    end

    subgraph L4 [Layer 4: Interactive Presentation UI]
        MODEL --> APP[Streamlit Dashboard app.py]
        ENC --> APP
        APP --> DASH[Plotly Executive Charts & Sliders]
    end
```

---

## 3.2 Database Design & Data Modeling (ER Diagram)

> [!IMPORTANT]
> ### **3rd Normal Form (3NF) Normalization Standard**
> The relational schema enforces strict 3NF decomposition to eliminate anomaly duplication across geographical lookups (`BOROUGHS`), property classes (`PROPERTY_TYPES`), and annual metering facts (`ENERGY_METRICS`, `LL97_PENALTIES`).

### Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    CITIES ||--o{ BOROUGHS : contains
    CITIES ||--o{ PROPERTIES : located_in
    BOROUGHS ||--o{ PROPERTIES : located_in
    PROPERTY_TYPES ||--o{ PROPERTIES : categorized_by
    CONSTRUCTION_STATUSES ||--o{ PROPERTIES : has_status
    PARENT_PROPERTIES ||--o{ PROPERTIES : parent_of

    PROPERTIES ||--|| ENERGY_METRICS : records
    PROPERTIES ||--|| EMISSION_METRICS : produces
    PROPERTIES ||--|| LL97_PENALTIES : incurs
    PROPERTIES ||--o{ PROPERTY_FUEL_USAGE : consumes
    PROPERTIES ||--o{ PROPERTY_ALERTS : triggers

    PROPERTIES {
        varchar(50) property_id PK
        varchar(255) property_name
        int year_built
        decimal gfa_buildings_parking_ft2
        int borough_id FK
        int property_type_id FK
    }

    ENERGY_METRICS {
        int energy_metric_id PK
        varchar(50) property_id FK
        decimal energy_star_score
        decimal site_eui_kbtu_ft2
        decimal site_energy_use_kbtu
    }

    EMISSION_METRICS {
        int emission_metric_id PK
        varchar(50) property_id FK
        decimal total_ghg_emissions_metric_tons_co2e
        decimal total_ghg_emissions_intensity_kgco2e_ft2
    }

    LL97_PENALTIES {
        int penalty_id PK
        varchar(50) property_id FK
        decimal base_ll97_penalty
        decimal base_penalty_per_ft2
    }
```

---

## 3.3 Data Flow & System Behavior

### Context-Level Data Flow Diagram (DFD Level 0)

```mermaid
flowchart LR
    USER[Real Estate Asset Manager / ESG Officer]
    NYC[NYC Open Data Portal / LL84 Portal]
    SYSTEM((Carbon Heist Mitigation Platform))

    NYC -- Raw Annual Energy Benchmarking Records --> SYSTEM
    USER -- Asset Parameters & CAPEX Sliders --> SYSTEM
    SYSTEM -- Projected Emissions & LL97 Fines --> USER
    SYSTEM -- Decarbonization Playbook & ROI Audit --> USER
```

---

### Sequence Diagram: Real-Time Asset Analysis Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Asset Manager
    participant UI as Streamlit UI (app.py)
    participant ML as ML Engine (ll97_model)
    participant Engine as Financial Calculation Engine

    User->>UI: Select Property Archetype & Input Specs (GFA, Year, Energy Star)
    UI->>ML: Pass Feature Vector [Year, GFA, Score, Borough_Enc, Type_Enc]
    ML-->>UI: Return Predicted Emissions (MT CO₂e)
    UI->>Engine: Calculate Statutory Exposure (Emissions * $268) / GFA
    Engine-->>UI: Return Penalty Liability ($/sq. ft.) & Peer Gap %
    UI->>User: Render Visual KPI Cards & Strategic Playbook Recommendations
```

---

### Activity Diagram: Automated ETL Data Cleaning Workflow

```mermaid
stateDiagram-v2
    [*] --> LoadRawData: Read LL84 Excel Spreadsheet
    LoadRawData --> ReplaceNulls: Standardize "Not Available" to NaN
    ReplaceNulls --> FilterStatus: Remove Test Properties
    FilterStatus --> FilterGFA: Retain Buildings >= 50,000 sq. ft.
    FilterGFA --> NormalizeCity: Correct City Typos & Enforce NYC Boroughs
    NormalizeCity --> FilterAlerts: Drop Records with Meter Gaps / Missing 12-Month Data
    FilterAlerts --> FilterOutliers: Drop Extreme Penalty Outliers ($/ft² > $1,700)
    FilterOutliers --> RemoveDuplicates: Deduplicate by Property ID
    RemoveDuplicates --> SaveCleanData: Export sample_nyc_energy.xlsx
    SaveCleanData --> GeneratePDF: Write LL97_Data_Cleaning_Report.pdf
    GeneratePDF --> [*]
```

---

<div align="center">

[![Prev Document](https://img.shields.io/badge/Prev-Doc_02:_Requirements-181717?style=for-the-badge)](./02_Requirements_and_Stakeholders.md)&nbsp;
[![Back to Suite](https://img.shields.io/badge/Back_to-Docs_Suite-00FF66?style=for-the-badge&logo=github)](./README.md)&nbsp;
[![Next Document](https://img.shields.io/badge/Next-Doc_04:_Implementation-00E5FF?style=for-the-badge)](./04_Implementation_and_Coding_Standards.md)

</div>
