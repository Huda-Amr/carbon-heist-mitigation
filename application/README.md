# 🖥️ Application Layer — Interactive Decision Support Dashboard

Welcome to the **Application Layer** of the **Carbon Heist Mitigation Platform**. This folder contains the interactive front-end web dashboard built to help real estate asset managers, sustainability officers, and MEP engineers simulate decarbonization strategies and calculate regulatory penalties under **NYC Local Law 97 (LL97)**.

---

## 📂 Folder Contents

| File Name | Description |
| :--- | :--- |
| **`app.py`** | Full-Stack interactive web dashboard developed with **Streamlit** and **Plotly**. Features dark-mode UI aesthetics, dynamic KPI cards, peer benchmarking charts, and real-time CAPEX simulation sliders. |
| **`input.xlsx`** | Cleaned and validated building benchmarking records utilized by the dashboard for interactive filtering and peer comparison. |
| **`results.csv`** | Exported data table containing calculated carbon liabilities, projected emissions, and financial penalties across different building archetypes. |

---

## ⚙️ Interactive UI & Simulation Flow

```mermaid
flowchart LR
    DATA["📊 input.xlsx\nValidated Building Records"]:::in --> UI["🖥️ Streamlit Front-End\napp.py Dashboard UI"]:::ui
    SLIDERS["🎛️ User Interactive Sliders\n• ENERGY STAR Score Shift\n• Electrification % Transition"]:::in --> UI
    UI --> CALC["🧮 Real-Time LL97 Fine Engine\nPenalty = Emissions × $268"]:::calc
    CALC --> VIZ["📈 Plotly Peer Benchmarking\nInteractive Bar & Scatter Plots"]:::viz
    CALC --> EXP["📥 Executive CSV Export\nresults.csv Compliance Log"]:::viz

    classDef in fill:#161B22,stroke:#8B949E,stroke-width:2px,color:#C9D1D9
    classDef ui fill:#0D1117,stroke:#FF4B4B,stroke-width:2px,color:#FF4B4B
    classDef calc fill:#0D1117,stroke:#F7931E,stroke-width:2px,color:#F7931E
    classDef viz fill:#0D1117,stroke:#00FF66,stroke-width:2px,color:#00FF66
```

---

## 🏛️ Statutory Fine Reference Formula

The interactive dashboard evaluates building carbon liability instantly using the official statutory fine formula:

> [!IMPORTANT]
> ### **Penalty ($) = Total Emissions (MT CO₂e) × 268**
> Where **$268** is the mandatory statutory fine per metric ton of **CO₂e** under NYC Local Law 97.

---

## 🎯 Key Features of the Dashboard

1. **Real-Time Statutory Penalty Calculation:**
   - Evaluates baseline fine liabilities and simulates financial savings immediately upon adjusting parameter inputs.
2. **Interactive Decarbonization Simulation (Sliders):**
   - **Energy Star Efficiency Slider:** Simulate insulation and HVAC optimization improvements.
   - **Electrification Shift Slider:** Model transitioning heating fuel systems from fossil gas to electric heat pumps.
3. **Peer Comparison & Benchmarking:**
   - Visualizes your building's Carbon Intensity (**kg CO₂e / sq. ft.**) against the NYC borough and property type averages.

---

## 🚀 How to Run the Dashboard Locally

Ensure your Python environment has all dependencies installed (`streamlit`, `plotly`, `pandas`, `openpyxl`, `joblib`), then run:

```bash
cd application
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.
