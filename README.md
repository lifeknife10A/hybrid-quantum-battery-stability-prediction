# Battery Materials DSS QML

Decision support system for lithium-ion battery material screening using
classical machine learning, simulated QML comparison, and India-focused
material feasibility rules.

## Important Clarification

This project is a DSS for lithium battery material decision support, using
classical ML and simulated QML comparison.

It is not commercial purchase advice for a specific branded battery product.
It ranks exact lithium compound candidates using available materials data, ML
predictions, India feasibility scoring, and simple explainable decision rules.
Battery family is kept as supporting chemistry context.

The project does not claim that QML already beats XGBoost on the full dataset.
XGBoost is treated as the strong present-day classical benchmark. The simulated
QML section is included as a future-facing quantum experiment because battery
materials are quantum systems at the atomic level, and quantum feature spaces
may become useful for this type of materials discovery as QML methods improve.

## Active Project Folder

The active project is here:

```text
Battery Materials DSS QML/
```

The older notebook-only experiment was moved here:

```text
_legacy/initial_notebook_project/
```

## What This Project Does

1. Uses a large Materials Project snapshot as the main source dataset.
2. Filters the dataset to lithium-containing materials.
3. Adds India-focused feasibility and battery-family scoring.
4. Trains XGBoost as the strong classical ML benchmark.
5. Builds simulated QML classifiers as the quantum-future experiment.
6. Compares QML with simple and strong classical baselines.
7. Creates DSS recommendation rankings for exact lithium compound candidates.
8. Provides a presentation-ready Jupyter notebook with outputs in each cell.

## Student-Level Project Flow

The safe presentation flow is:

1. DSS is the main product.
2. XGBoost is the current reliable ML benchmark.
3. Logistic Regression is the simple classical baseline.
4. Simulated QML is the quantum exploration layer.
5. The final recommendation is based on DSS ranking, not on an unsupported
   claim of quantum advantage.

Short explanation:

> XGBoost is strong for today's tabular materials data. QML is included because
> materials are quantum systems, and future quantum computers may represent
> material behavior more naturally. Our project shows a student-level bridge
> from classical DSS to quantum-assisted materials discovery.

## Current Data Size

| Dataset Stage | Size |
| --- | ---: |
| Full raw Materials Project snapshot | 210,579 rows |
| Lithium-only dataset | 24,957 rows |
| India-scored lithium dataset | 24,957 rows x 37 columns |
| Final India battery shortlist | 629 rows |
| QML-ready balanced dataset | 1,000 rows x 27 columns |
| DSS compound recommendation ranking | 629 rows |
| Supporting battery-family context | 6 rows |

## Current Model Results

| Model / Experiment | Result |
| --- | ---: |
| XGBoost classifier accuracy | 0.9091 |
| XGBoost regressor MAE | 0.1005 |
| QML quantum-kernel accuracy | 0.8100 |
| Tuned QML accuracy | 0.8200 |
| Repeated-split best QML mean accuracy | 0.8550 |
| QML vs Logistic Regression mean accuracy | 0.8550 vs 0.8410 |
| Same-data XGBoost accuracy on QML-ready split | 0.8300 |

## Main Files

| File | Purpose |
| --- | --- |
| `Battery Materials DSS QML/Battery Materials DSS QML Main Presentation.ipynb` | Main presentation notebook with saved outputs. |
| `Battery Materials DSS QML/Student Level Project Flow.md` | Safe student-level story and judge explanation. |
| `Battery Materials DSS QML/Project understanding.md` | Ground-up project understanding document. |
| `Battery Materials DSS QML/Indian Battery Materials Report.docx` | India-relevant battery materials report. |
| `Battery Materials DSS QML/data/processed/dss compound recommendation ranking.csv` | Main compound-level DSS ranking. |
| `Battery Materials DSS QML/data/processed/dss material recommendation ranking.csv` | Material-level DSS ranking. |
| `Battery Materials DSS QML/data/processed/dss battery family recommendation ranking.csv` | Supporting family context. |
| `Battery Materials DSS QML/data/processed/qml circuit diagram.png` | Visual circuit diagram for the simulated QML feature map. |
| `Battery Materials DSS QML/data/metadata/project_pipeline_summary.md` | Full pipeline summary. |
| `Battery Materials DSS QML/data/metadata/dss_recommendation_summary.md` | DSS recommendation explanation. |

## Project Structure

```text
hybrid-quantum-battery-stability-prediction/
├── Battery Materials DSS QML/
│   ├── Battery Materials DSS QML Main Presentation.ipynb
│   ├── Project understanding.md
│   ├── Indian Battery Materials Report.docx
│   ├── Literature Review.xlsx
│   ├── Paper/
│   ├── data/
│   │   ├── metadata/
│   │   ├── models/
│   │   ├── processed/
│   │   └── raw/
│   ├── scripts/
│   └── requirements.txt
├── _legacy/
│   └── initial_notebook_project/
├── README.md
└── requirements.txt
```

## How To Run

Install dependencies from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

Go to the active project folder:

```bash
cd "Battery Materials DSS QML"
```

Regenerate the main presentation notebook:

```bash
python3 scripts/create_main_presentation_notebook.py
```

Run the main pipeline scripts from the active project folder:

```bash
python3 scripts/process_materials_project_dataset.py
python3 scripts/create_lithium_india_scored_dataset.py
python3 scripts/create_lithium_india_scored_eda.py
python3 scripts/train_xgboost_baseline.py
python3 scripts/create_final_india_battery_shortlist.py
python3 scripts/create_qml_ready_dataset.py
python3 scripts/train_qml_baseline.py
python3 scripts/tune_qml_baseline.py
python3 scripts/run_improved_qml_experiments.py
python3 scripts/run_best_qml_repeated_splits.py
python3 scripts/compare_qml_with_logistic_baseline.py
python3 scripts/create_qml_circuit_diagram.py
python3 scripts/create_dss_recommendation_ranking.py
python3 scripts/create_main_presentation_notebook.py
```

## Notes

- The QML work is simulator-based and exploratory.
- The project compares QML against classical baselines honestly.
- The DSS output should be treated as decision support, not as a final
  engineering certification for battery manufacturing.
- Dependency versions are intentionally not pinned yet. Version pinning can be
  added in the next cleanup step.
