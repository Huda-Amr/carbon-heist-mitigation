# 5. Testing & Quality Assurance

## 5.1 Test Plan & Test Scenarios

The **Carbon Heist Mitigation Platform** employs a comprehensive verification strategy spanning data engineering integrity, predictive machine learning regression accuracy, and interactive UI verification.

### Test Matrix & Verification Outcomes

| Test ID | Test Category | Scenario Description | Input / Condition | Expected Outcome | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | **Data Engineering** | Ingest Raw LL84 Spreadsheet | 11,000+ Raw NYC municipal disclosure records | Cleanly replace `"Not Available"` with `NaN` without data corruption | Successfully parsed all records | **PASS** |
| **TC-02** | **Data Engineering** | Size Threshold Compliance | Apply `GFA >= 50,000 sq ft` filter | Retain only buildings legally subject to LL97 | Retained 11,639 compliant properties | **PASS** |
| **TC-03** | **Data Engineering** | Borough Normalization | Input misspelled city names (`"Ny"`, `"Quuens"`, `"beonx"`) | Map to correct standard NYC borough strings | Exactly 0 invalid addresses remaining | **PASS** |
| **TC-04** | **Machine Learning** | Random Forest Regressor Accuracy | Train model on 80/20 train/test split | Achieve $R^2 \ge 75\%$ and MAE $\le 250$ MT CO₂e | **$R^2 = 81.65\%$**, **MAE = 212.99** | **PASS** |
| **TC-05** | **Machine Learning** | Outlier Alignment Parity | Ensure `train_ll97_model.py` and `ll97_playground.py` match | Both scripts filter `Site EUI < 2000` | Both scripts yield exact $81.6\%$ accuracy | **PASS** |
| **TC-06** | **Financial Engine** | LL97 Statutory Fine Calculation | 1930s Asset (150k sq. ft., predicted 1,422.1 MT CO₂e) | Exact calculation: $\$2.54$ penalty / sq. ft. | Verified exact match ($\$2.54$/ft²) | **PASS** |
| **TC-07** | **UI / Dashboard** | Interactive Slider Recalculation | Adjust Energy Star slider from 40 to 85 | Instant chart update showing reduced carbon penalty | Rendered under 0.3s | **PASS** |

---

## 5.2 Automated Testing Scripts

The project uses automated Python validation blocks within `train_ll97_model.py` and `Clean_Data_Pipeline.py` to assert data structure health before exporting artifacts:

```python
# Automated assertion check inside pipeline execution
assert len(df) > 10000, "CRITICAL ERROR: Cleaned dataset unexpectedly dropped below 10,000 records!"
assert df['Property GFA - Calculated (Buildings and Parking) (ft²)'].min() >= 50000, "ERROR: Non-compliant small building detected!"
assert not df['Total GHG Emissions (Metric Tons CO2e)'].isna().any(), "ERROR: Target feature contains NaN values!"
```

---

## 5.3 Bug Reports & Resolutions Log

| Bug ID | Date Reported | Description of Issue | Root Cause Analysis | Corrective Action & Resolution |
| :---: | :---: | :--- | :--- | :--- |
| **BUG-01** | 2026-06-30 | Playground accuracy dropped to **63.8%** compared to **81.6%** in main model training script. | `ll97_playground.py` had an outdated filter (`Site EUI < 1500`) that truncated extreme data variance compared to `train_ll97_model.py` (`Site EUI < 2000`). | Synchronized data cleaning filters across both files (`Site EUI < 2000`); playground accuracy restored to **81.6%**. |
| **BUG-02** | 2026-06-30 | Python terminal reported `SyntaxWarning: "\d" is an invalid escape sequence` on path load. | Windows relative file path `..\data\sample_nyc_energy.xlsx` was interpreted by Python regex tokenizer as escape sequence `\d`. | Standardized relative file paths to POSIX forward slashes (`../data/sample_nyc_energy.xlsx`) across all scripts. |
| **BUG-03** | 2026-07-02 | Microsoft SQL Server rejected DDL file with syntax error near `ON DELETE RESTRICT`. | Microsoft SQL Server (T-SQL) does not support standard ANSI `ON DELETE RESTRICT` syntax. | Created dedicated Microsoft SQL Server schema (`carbon_heist_schema_mssql.sql`) replacing `RESTRICT` with `ON DELETE NO ACTION`. |
