# 📑 Financial Engineering & Domain Reference Models

Welcome to the **Domain & Financial Engineering Layer** of the **Carbon Heist Mitigation Platform**. This directory contains our comprehensive **16-sheet financial, engineering, and C-Suite visualization workbook (`Co2 Project.xlsx`)**, which serves as the master domain reference for all Local Law 97 statutory penalty calculations, capital expenditure (CAPEX) unit-cost breakdowns, operating expenditure (OPEX) schedules, interactive bridge charts (`Waterfall Charts`), and the 5 Decarbonization Playbooks.

---

## 📂 Folder Contents

| File Name | Description |
| :--- | :--- |
| **`Co2 Project.xlsx`** | Master **16-sheet engineering, itemized financial breakdown, and executive visualization reference workbook** for **NYC Local Law 97 (LL97)** compliance modeling, risk profiling, and retrofit planning across `11,639` properties. |

---

## ⚙️ Financial & Engineering 16-Sheet Architecture

```mermaid
flowchart TD
    RAW["1️⃣ Data & 2️⃣ Clean Sheets\nRaw municipal LL84 benchmarking data & filtered 50k+ sq. ft. subset"]:::raw --> AN["3️⃣ Analysis & 4️⃣ Data Cards\nDescriptive statistics, EUI intensity & macro portfolio constants"]:::an
    AN --> SENS["5️⃣ Sensitivity & 6️⃣ Scenario Sheets\nCAPEX stress-testing, weather shock absorbers & multi-year paths"]:::sens
    SENS --> FIN["7️⃣ Summary Table, 8️⃣ CAPEX & Breakdown & 9️⃣ OPEX & Maintenance Breakdown\nComprehensive strategic financial matrix, granular CAPEX itemization & itemized annual OPEX"]:::fin
    FIN --> EXEC["🔟 Executive Summary & 1️⃣1️⃣ Factors Dashboard\nC-Suite portfolio portals & macro risk drivers (Age, Geography, EUI & Archetypes)"]:::cards
    EXEC --> PB1["1️⃣2️⃣ Surgical Strike\nImmediate Low-Cost BMS/VFD Interventions ($20.6M/yr Net Savings | 8-Day Payback)"]:::pb
    EXEC --> PB2["1️⃣3️⃣ Retro-commissioning\nHVAC RCx & Setpoint Tuning ($243.6M/yr Maximum Fine Savings | 3.29-Yr Payback)"]:::pb
    EXEC --> PB3["1️⃣4️⃣ WET Scenario\nPre-War 1930s Historic Masonry Wastewater Heat Recovery ($122.4M/yr Saved)"]:::pb
    EXEC --> PB4["1️⃣5️⃣ 1960s Smart Scale\nPost-War Boom Target Subset ($88.0M/yr Saved | #1 Emitting Vintage)"]:::pb
    EXEC --> PB5["1️⃣6️⃣ Electrification Push\nDeep Geothermal & Heat Pump Fossil Conversion ($182.0M/yr Saved)"]:::pb

    classDef raw fill:#161B22,stroke:#8B949E,stroke-width:2px,color:#C9D1D9
    classDef an fill:#0D1117,stroke:#30363D,stroke-width:2px,color:#E6EDF3
    classDef sens fill:#0D1117,stroke:#F7931E,stroke-width:2px,color:#F7931E
    classDef fin fill:#0D1117,stroke:#9B51E0,stroke-width:2px,color:#E6EDF3
    classDef cards fill:#0D1117,stroke:#00E5FF,stroke-width:2px,color:#00E5FF
    classDef pb fill:#0D1117,stroke:#00FF66,stroke-width:2px,color:#00FF66
```

---

## 🏛️ Statutory Fine Reference Formula

Across all financial sheets, statutory penalty exposure is evaluated using the official Local Law 97 formula:

> [!IMPORTANT]
> ### **Penalty ($) = Total Emissions (MT CO₂e) × 268**
> Where **$268** is the mandatory fine rate per metric ton of **CO₂e** exceeding statutory thresholds under NYC Local Law 97 across our analyzed portfolio of `11,639` buildings.

---

## 📊 Detailed Structure of Workbook Sheets (16 Sheets)

Our master workbook (`Co2 Project.xlsx`) is logically structured into three distinct functional layers: **Core Data & Baseline Analytics**, **Comprehensive Financial Breakdowns & Executive Summaries**, and **Decarbonization Playbook Scenarios**:

### 📈 I. Core Data & Baseline Analytics (Sheets 1–6)
| # | Sheet Name | Description & Analytical Purpose |
| :---: | :--- | :--- |
| **1** | **`Data`** | Raw municipal building energy disclosure records imported from official NYC Local Law 84 benchmarking files across `21,000+` property records. |
| **2** | **`Clean`** | Filtered and validated data subset retaining compliant properties (**Gross Floor Area ≥ 50,000 sq. ft.**) totaling `11,639` analyzed portfolio assets. |
| **3** | **`Analysis`** | Core analytical sheet computing descriptive statistics, energy intensity (`Site EUI`) distributions, top offender rankings, and baseline unmitigated penalty liabilities (`$2.83 Billion`). |
| **4** | **`Data Cards`** | Executive summary cards defining core portfolio constants, total square footage (`2.01 Billion sq. ft.`), `$268/MT` penalty rate, and weather shock absorber ranges (`+5% to +15%`). |
| **5** | **`Sensitivity`** | Sensitivity stress-testing matrix evaluating how different CAPEX reinvestment rates and weather shock absorbers impact Net Operating Income (`NOI`) and fine avoidance ($/sq. ft.). |
| **6** | **`Scenario`** | Multi-year scenario model comparing baseline business-as-usual unmitigated trajectories against phased decarbonization paths across construction decades (`1930s`, `1950s`, `1970s`). |

---

### 👑 II. Comprehensive Financial Breakdowns & Executive Portals (Sheets 7–11)
| # | Sheet Name | Description & Financial Architecture | Key Visualizations & Features |
| :---: | :--- | :--- | :--- |
| **7** | **`Summary Table`** | **Master Strategic Executive Matrix:** Consolidated portfolio summary detailing unmitigated fine exposure (`$2,830.68M`), total 5-Playbook capital investment (`$4,976.80M`), recurring annual savings (`$656.63M/yr`), and blended capital payback (`6.97 Years`). | Master C-Suite 5-Phase Playbook matrix and macroeconomic cascade table. |
| **8** | **`CAPEX & Breakdown`** | **Granular Itemization of Capital Expenditure:** Detailed engineering and unit-cost breakdown (`$/ft²`, `$/building`) across equipment, labor, mechanical sub-systems, and 50% government PPP/grant subsidies for all 5 playbooks. | Itemized cost allocation rates (`Level 2 Audits: $15K/bldg`, `BMS Optimization: $12.5K/bldg`, `Steam Traps: $12.5K/bldg`). |
| **9** | **`OPEX & Maintenance Breakdown`** | **Granular Operating Expenditure & Maintenance Schedules:** Comprehensive breakdown of recurring annual maintenance costs, operational labor overhead, sensor replacements, and ongoing measurement & verification (`M&V`) expenses. | Itemized OPEX offsets and annual net cash flow calculations verifying long-term asset profitability. |
| **10** | **`Executive Summary`** | **C-Suite Presentation Portal:** High-level narrative overview and executive briefing dashboard designed for asset managers, real estate investment committees, and regulatory authorities. | High-level portfolio overview cards (`THE CARBON HEIST` - 11,639 Properties across NYC). |
| **11** | **`Factors`** | **Forensic Carbon Drivers Dashboard:** Consolidated visual portal analyzing macro-level risk drivers across Age (`Decade`), Geography (`Borough`), Efficiency (`ENERGY STAR`), and Property Archetypes. | 1. **`Building Vintage Analysis: Total GHG Emissions vs. Penalty Intensity ($/ft²)`**<br/>2. **`NYC Borough Carbon Emissions Distribution (MT CO₂e / Year)`**<br/>3. **`Carbon Concentration by ENERGY STAR Bracket (1–100)`**<br/>4. **`Carbon Emissions by Property Archetype (MT CO₂e / Year)`** |

---

### 🚀 III. Decarbonization Playbook Scenarios (Sheets 12–16)
Each dedicated scenario tab models one of the 5 engineering playbooks and features custom KPI cards (`Penalty Risk Per Year`, `Total Project CAPEX`, `Fine Savings Per Year`), architectural/mechanical illustrations, and **Financial Bridge / Waterfall Charts** (`Before vs. After Statutory Penalty Exposure`):

| # | Sheet Name | Target Subset & Playbook Strategy | Financial Impact & Payback | Bridge Chart Title (`Before vs. After`) |
| :---: | :--- | :--- | :--- | :--- |
| **12** | **`Surgical Strike`** | **Playbook 01 (`Immediate O&M Interventions`):** Low-cost BMS sensors, Variable Frequency Drives (VFDs), and Level 2 audit setpoint tuning for top 10 worst offenders. | **`$20.6M/yr Net Savings`**<br/>`$500K CAPEX`<br/>**8-Day Payback (`0.02 Yr`)** | **`Surgical Strike Penalty Reduction Waterfall ($20.6M/yr Saved)`**<br/>`$51.5M Exposure → $30.9M Residual Penalty` |
| **13** | **`Retro-commissioning`** | **Playbook 02 (`HVAC & BMS Automation`):** Whole-building HVAC retro-commissioning, automated Fault Detection & Diagnostics (FDD), and VAV box balancing at `$1.50/ft²`. | **`$243.6M/yr Maximum Savings`**<br/>`$802.2M CAPEX`<br/>**3.29-Year Payback** | **`Retro-commissioning Penalty Reduction Bridge ($243.6M/yr Saved)`**<br/>`$974.5M Exposure → $730.8M Residual Penalty` |
| **14** | **`WET Scenario`** | **Playbook 04 (`Pre-War 1930s Historic Masonry`):** Waste-heat Energy Transfer (`WET`) wastewater heat recovery systems extracting thermal energy from hot graywater without disrupting architectural facades. | **`$122.4M/yr Net Savings`**<br/>`$1.50B Net CAPEX`<br/>**12.25-Year Payback** | **`WET Systems Penalty Reduction Bridge ($122.4M/yr Saved)`**<br/>`$306.0M Exposure → $183.6M Residual Penalty` |
| **15** | **`1960s Smart Scale`** | **Playbook 03 (`Post-War Boom Archetypes`):** Targeted smart automation, district loop scaling, and envelope weatherization for NYC's #1 single largest emitting construction decade (`1960s`). | **`$88.0M/yr Net Savings`**<br/>`$785.2M CAPEX`<br/>**8.92-Year Payback** | **`1960s Smart Scale Penalty Bridge ($88.0M/yr Saved)`**<br/>`$440.2M Exposure → $352.1M Residual Penalty` |
| **16** | **`Electrification Push`** | **Playbook 05 (`Deep Geothermal & Heat Pumps`):** Replacement of fossil fuel heating boilers with high-efficiency air-source and water-source electric heat pump networks. | **`$182.0M/yr Net Savings`**<br/>`$2.30B CAPEX`<br/>**12.63-Year Payback** | **`Electrification Push Penalty Reduction Bridge ($182.0M/yr Saved)`** |

---

<div align="center">

[![Return to Main Repo](https://img.shields.io/badge/🏠%20RETURN%20TO-MAIN%20REPOSITORY%20HOME-00FF66?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ahmedadelamin/carbon-heist-mitigation)&nbsp;
[![Docs Suite](https://img.shields.io/badge/📑%20VIEW-ACADEMIC%20DOCS%20SUITE-00E5FF?style=for-the-badge)](../docs/README.md)

</div>
