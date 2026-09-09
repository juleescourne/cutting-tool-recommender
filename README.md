# Cutting Tool Recommendation System

[![Python checks](https://github.com/juleescourne/cutting-tool-recommender/actions/workflows/python-tests.yml/badge.svg)](https://github.com/juleescourne/cutting-tool-recommender/actions/workflows/python-tests.yml)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

> Part of my Data portfolio: [juleescourne.github.io/portfolio-data-analyst](https://juleescourne.github.io/portfolio-data-analyst/)

A Python decision-support application for **machining experiment analysis and cutting-tool recommendation**.

The project was originally developed as an engineering/academic prototype in collaboration with the Mechanical Engineering department at the University of Tours. It combines a relational machining-experiment database, Excel ingestion, dimensionality reduction with PCA, similarity-based recommendation, and interactive Plotly/Dash visualizations.

> **Portfolio focus:** data engineering, relational data modeling, data analysis, PCA, decision support, and Python application architecture.

## What the application does

The application stores historical machining experiments and helps compare a new target configuration with previously observed experiments.

```text
Excel machining experiments
          |
          v
      Validation
          |
          v
      MySQL database
          |
          v
Feature selection + aggregation
          |
          v
Standardization -> PCA
          |
          v
Weighted similarity search
          |
          v
Cutting-tool recommendation
          |
          v
Plotly / Dash visual analysis
```

Two main workflows are available:

### Research / experiment workflow

- Import machining experiments from a structured Excel workbook.
- Store process, workpiece, cutting-tool and measurement data in MySQL.
- Explore force, temperature, wear, vibration and surface-quality measurements.
- Export an experiment back to an Excel workbook.
- Build interactive Plotly/Dash visualizations.

### Decision-support workflow

- Select a machining process and workpiece material.
- Define target constraints such as force, temperature, roughness, machining time or vibration.
- Aggregate historical experiment measurements.
- Standardize heterogeneous physical variables.
- Project historical experiments into a PCA space.
- Transform the user's target point into the same PCA representation.
- Rank the closest experiments using a weighted Euclidean distance.
- Inspect the most similar experiments and their cutting tools.

## Data model

The MySQL schema separates the different parts of a machining experiment into dedicated entities:

| Entity | Purpose |
| --- | --- |
| `experience` | Experiment identifier and name |
| `procede` | Machining-process parameters |
| `entree_piece` | Workpiece input parameters |
| `entree_outil` | Cutting-tool input parameters |
| `effort_piece` | Force measurements on the workpiece |
| `effort_outil` | Force measurements transformed into tool coordinates |
| `temperature_piece` | Workpiece temperature measurements |
| `temperature_outil` | Cutting-tool temperature measurements |
| `sortie_piece` | Roughness, hardness, endurance and residual stress |
| `usure_outil` | Tool-wear measurements |
| `copeaux` | Chip measurements |
| `vibration` | Vibration time series |

The application uses both **SQLAlchemy ORM** and direct MySQL queries for the historical prototype logic.

## Recommendation methodology

The recommendation module follows these steps:

1. Filter experiments by machining process and material.
2. Select the numerical variables requested by the user.
3. Aggregate time-series measurements using representative extrema where required.
4. Replace unavailable selected measurements with neutral values in the historical prototype workflow.
5. Standardize variables with `StandardScaler` so measurements expressed in different physical units are comparable.
6. Fit PCA on historical experiments only.
7. Transform the target configuration into the fitted PCA space.
8. Compute a weighted Euclidean distance, using PCA explained-variance ratios as component weights.
9. Rank the nearest historical experiments.

This is a **similarity-based decision-support approach**, not a supervised prediction model.

## Technology stack

- **Python**
- **Pandas / NumPy** — data processing
- **Scikit-learn** — PCA and feature scaling
- **MySQL** — relational storage
- **SQLAlchemy** — ORM and database access
- **Plotly / Dash** — interactive analytics dashboards
- **Tkinter** — desktop interface
- **openpyxl** — Excel import/export
- **pytest** — unit tests
- **GitHub Actions** — automated checks

## Project structure

```text
.
├── main.py
├── config.py
├── utils.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
│
├── controller/              # Application and decision-support logic
│   ├── ChoixOutilCoupant.py # PCA + recommendation workflow
│   ├── ImportExperience.py
│   ├── ExportExperience.py
│   └── ...
│
├── model/                   # SQLAlchemy entities and DB connection
├── view/                    # Tkinter / Dash presentation layer
├── db/
│   └── schema.sql
├── templates/
│   └── experiment_template.xlsx
├── downloads/               # Generated exports (ignored by Git)
├── tests/
│   └── test_utils.py
└── .github/workflows/
    └── python-tests.yml
```

## Local setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd cutting-tool-recommender
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Tkinter is part of the standard Python installation on Windows. On some Linux distributions it must be installed separately, for example `python3-tk`.

### 4. Create the MySQL schema

```bash
mysql -u root -p < db/schema.sql
```

Create an application user if needed:

```sql
CREATE USER 'cutting_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON cutting.* TO 'cutting_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure local credentials

Copy `.env.example` to `.env` and edit the local values:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=cutting_user
DB_PASSWORD=your-password
DB_NAME=cutting
SQLALCHEMY_ECHO=false
```

`.env` is excluded from Git and must never be committed.

### 6. Run the application

```bash
python main.py
```

## Excel experiment format

A reusable workbook is included at:

```text
templates/experiment_template.xlsx
```

The workbook contains:

- machining-process metadata;
- cutting-tool parameters;
- workpiece parameters;
- force time series;
- temperature measurements;
- surface-quality measurements;
- tool-wear measurements;
- chip measurements;
- vibration time series.

Exported experiments are written to the local `downloads/` directory, which is ignored by Git.

## Tests

Install development dependencies and run:

```bash
pip install -r requirements-dev.txt
pytest -q
```

The current tests cover the reusable numerical utilities and the restricted mathematical-expression evaluator. GitHub Actions also performs a Python compilation check on each push and pull request.

## GitHub-ready cleanup

This public-facing version includes several improvements over the original academic prototype:

- removed the original Git history and generated cache files;
- removed IDE metadata and generated HTML documentation;
- removed undocumented third-party branding/background assets from the UI;
- removed hard-coded database credentials and moved configuration to environment variables;
- switched SQLAlchemy to the MySQL Connector driver for easier cross-platform installation;
- standardized table naming for Linux/Windows MySQL compatibility;
- added an Excel experiment template and cross-platform export paths;
- updated the vibration key so multiple time-series observations can be stored per experiment;
- replaced unrestricted `eval()` usage with a restricted mathematical-expression evaluator;
- standardized physical features before PCA;
- fitted the scaler/PCA representation on historical experiments rather than the target query point;
- added a minimal test suite and GitHub Actions workflow;
- reduced the dependency list to packages actually used by the project.

## Data and reproducibility note

The repository does **not** include the original machining experiment dataset. The application was designed around experimental engineering data and the public repository therefore contains the schema and import template rather than the underlying research measurements.

As a result, the full recommendation quality cannot be benchmarked from this repository alone. The code demonstrates the application architecture and analysis workflow, while real evaluation requires an appropriate set of machining experiments.

## Further improvements

Potential next steps for a production-grade version include:

- migrate all direct SQL queries to a single repository/data-access layer;
- add database migrations;
- improve missing-value treatment instead of using neutral replacements;
- add integration tests against a disposable MySQL database;
- add synthetic demo experiments for end-to-end CI testing;
- separate data-processing logic from GUI controllers more strictly;
- benchmark the recommendation approach against supervised or metric-learning baselines.
