# 🤖 Artificial Intelligence & Predictive Modeling Layer

Welcome to the **Machine Learning Layer** of the **Carbon Heist Mitigation Platform**. This directory houses our predictive engine, feature encoders, training pipelines, and interactive CLI simulation playground used to forecast greenhouse gas emissions and evaluate statutory penalty exposure under **NYC Local Law 97**.

---

## 📂 Folder Contents

| File Name | Description |
| :--- | :--- |
| **`train_ll97_model.py`** | Automated Python model training pipeline (`scikit-learn`, `joblib`). Loads cleaned records, applies outlier guardrails (**Site EUI < 2000**), encodes categorical features, trains a **Random Forest Regressor**, validates accuracy (**R² = 81.65%**), and exports serialized models. |
| **`ll97_playground.py`** | Interactive command-line simulation playground. Allows engineers to input custom building specifications (Year Built, GFA, Energy Star, Borough, Property Type) and inspect predicted emissions and financial penalties in real time. |
| **`ll97_model.joblib`** | Serialized trained **Random Forest Regressor** model (`n_estimators=150`, `max_depth=20`) ready for production inference. |
| **`ll97_encoders.joblib`** | Serialized categorical feature encoders ensuring consistency across training, testing, and UI inference. |

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

<div align="center">

[![Return to Main Repo](https://img.shields.io/badge/🏠%20RETURN%20TO-MAIN%20REPOSITORY%20HOME-00FF66?style=for-the-badge&logo=github&logoColor=black)](https://github.com/ahmedadelamin/carbon-heist-mitigation)&nbsp;
[![Docs Suite](https://img.shields.io/badge/📑%20VIEW-ACADEMIC%20DOCS%20SUITE-00E5FF?style=for-the-badge)](../Project%20Documentations/README.md)

</div>
