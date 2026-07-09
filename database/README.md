# 🗄️ Relational Database & Persistence Layer

Welcome to the **Database Layer** of the **Carbon Heist Mitigation Platform**. This directory houses the relational database schemas, Entity-Relationship Diagrams (ERD), and normalization specifications designed to persist building dimensions, annual energy benchmarking measurements, and regulatory compliance alerts.

---

## 📂 Folder Contents

| File Name | Description |
| :--- | :--- |
| **`carbon_heist_schema_mysql.sql`** | SQL Data Definition Language (DDL) script optimized for **MySQL**, **MariaDB**, and **PostgreSQL**. Implements 3NF normalized tables, foreign key constraints, and indexing. |
| **`carbon_heist_schema_mssql.sql`** | Dedicated T-SQL Data Definition Language script optimized for **Microsoft SQL Server**. Adheres to enterprise T-SQL standards (`ON DELETE NO ACTION`, batch separators `GO`). |
| **`NYC_Energy_Chen_ERD.drawio`** | Complete relational Entity-Relationship Diagram (ERD) designed in Chen / Crow's Foot notation, editable in Draw.io. |
| **`Diagram.png`** | High-resolution exported image of the Entity-Relationship Diagram for quick visual reference. |
| **`NYC_Energy_CO2_Tables_V2.xlsx`** | Data modeling spreadsheet illustrating relational table structures, data types, and sample tuples. |

---

## 🏛️ Normalized Schema Architecture (3NF)

The database design splits wide municipal spreadsheets into clean, normalized relational entities:
- **`CITIES` & `BOROUGHS`:** Standardized geographical lookups enforcing unique address hierarchy.
- **`PROPERTY_TYPES`:** Categorical classifications for commercial, residential, and institutional buildings.
- **`PROPERTIES`:** Core entity storing physical building dimensions (`year_built`, `gfa_ft2`).
- **`ENERGY_METRICS` & `EMISSION_METRICS`:** Annual energy consumption facts (`site_eui`, `energy_star_score`) and carbon footprint metrics (`total_ghg_emissions`).
- **`LL97_PENALTIES`:** Statutory fine exposure (`base_ll97_penalty`, `penalty_per_ft2`).
- **`PROPERTY_FUEL_USAGE`:** Granular breakdown of heating oil, district steam, natural gas, and electricity consumption.
- **`PROPERTY_ALERTS`:** Compliance diagnostics and data integrity flags.

---

## 🚀 How to Initialize the Database

### For MySQL / MariaDB / PostgreSQL:
```bash
mysql -u root -p < database/carbon_heist_schema_mysql.sql
```

### For Microsoft SQL Server (T-SQL via SQLCMD):
```bash
sqlcmd -S localhost -U sa -P YourPassword -i database/carbon_heist_schema_mssql.sql
```
