<div align="center">

# 🤖 Artificial Intelligence & Predictive Modeling Layer

[![Live Streamlit App](https://img.shields.io/badge/🌐%20LIVE_APP-LAUNCH_STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://carbon-heist-mitigation.streamlit.app/)&nbsp;
[![AI Chatbot](https://img.shields.io/badge/AI%20Chatbot-Google%20Gemini%202.5%20%2B%20Local-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://carbon-heist-mitigation.streamlit.app/)

</div>

---

The **Predictive Artificial Intelligence & Machine Learning Layer (`models/`)** serves as the core quantitative engine of the **Carbon Heist Mitigation Platform**. By leveraging advanced ensemble regression (`Random Forest Regressor` achieving **R² = 81.65%**), this suite empowers real estate asset owners, sustainability directors, and C-Suite executives to forecast building greenhouse gas (GHG) emissions with mathematical precision, quantify statutory fine liabilities under **NYC Local Law 97**, and simulate proactive capital mitigation scenarios well before regulatory enforcement deadlines.

---

## 📂 Folder Contents

| File Name | Description |
| :--- | :--- |
| **`train_ll97_model.py`** | Automated Python model training pipeline (`scikit-learn`, `joblib`). Loads cleaned records, applies outlier guardrails (**Site EUI < 2000**), encodes categorical features, trains a **Random Forest Regressor**, validates accuracy (**R² = 81.65%**), and exports serialized models. |
| **`ll97_playground.py`** | Interactive command-line simulation playground. Allows engineers to input custom building specifications (Year Built, GFA, Energy Star, Borough, Property Type) and inspect predicted emissions and financial penalties in real time. |
| **`ll97_model.joblib`** | Serialized trained **Random Forest Regressor** model (`n_estimators=150`, `max_depth=20`) ready for production inference inside **Tab 3 (`ML Predictor`)** of our **5-Tab Streamlit Dashboard (`application/app.py`)**. |
| **`ll97_encoders.joblib`** | Serialized categorical feature encoders ensuring 100% data alignment across training, testing, CLI simulation (`ll97_playground.py`), and real-time dashboard UI inference. |

---

## 📈 Model Architecture & Flow

```mermaid
flowchart LR
    IN["📊 Clean NYC Data\n11,622 Buildings"]:::input --> FE["🛠️ Feature Engineering & Guardrails\nSite EUI < 2000 & Categorical Encoders"]:::proc
    FE --> RF["🤖 Random Forest Regressor\n150 Decision Trees, Max Depth 20"]:::ml
    RF --> EVAL["✅ Validation Accuracy\nR² = 81.65% | MAE = 212.99 MT CO₂e"]:::eval
    EVAL --> OUT1["💾 ll97_model.joblib"]:::art
    EVAL --> OUT2["🖥️ Interactive CLI Audit\nll97_playground.py"]:::art

    classDef input fill:#161B22,stroke:#8B949E,stroke-width:2px,color:#C9D1D9
    classDef proc fill:#0D1117,stroke:#30363D,stroke-width:2px,color:#E6EDF3
    classDef ml fill:#0D1117,stroke:#F7931E,stroke-width:2px,color:#F7931E
    classDef eval fill:#0D1117,stroke:#00FF66,stroke-width:2px,color:#00FF66
    classDef art fill:#0D1117,stroke:#00E5FF,stroke-width:2px,color:#00E5FF
```

### Model Performance Highlights:
- **Algorithm:** `RandomForestRegressor` (`n_estimators=150`, `max_depth=20`)
- **Predictors (Features):** `Year Built`, `Gross Floor Area (GFA)`, `ENERGY STAR Score`, `Borough`, `Primary Property Type`
- **Target Variable:** `Total GHG Emissions (Metric Tons CO2e)`
- **Validated Accuracy (R²):** **81.65%**
- **Mean Absolute Error (MAE):** **212.99 MT CO₂e**

---

## 🚀 How to Execute & Retrain

### 1. Retrain Model & Regenerate `.joblib` Artifacts:
```bash
cd models
python train_ll97_model.py
```

### 2. Run Interactive CLI Playground:
```bash
cd models
python ll97_playground.py
```


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

<div align="center">

[![Return to Main Repo](https://img.shields.io/badge/🏠%20RETURN%20TO-MAIN%20REPOSITORY%20HOME-00FF66?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ahmedadelamin/carbon-heist-mitigation)&nbsp;
[![Docs Suite](https://img.shields.io/badge/📑%20VIEW-ACADEMIC%20DOCS%20SUITE-00E5FF?style=for-the-badge)](../Project%20Documentations/README.md)

</div>
