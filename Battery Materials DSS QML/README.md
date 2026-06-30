# Battery Materials DSS QML

This folder contains the main lithium battery material Decision Support System
project.

The project is student-level by design: the code is kept simple, the QML
simulation is explained directly, and the final output is a clear compound
ranking table.

## Problem

The project asks:

> Which exact lithium compound formulas should be recommended first for
> India-focused battery material research and business screening?

The DSS does not recommend only broad names like LFP or LMFP. It ranks exact
formulas and material IDs.

## Current Project Position

The final DSS is now **QML-primary**:

1. QML gives the first stable-material probability.
2. XGBoost gives a strong classical correction signal.
3. If QML is confident, QML receives more ranking weight.
4. If QML is uncertain, XGBoost acts as backup.
5. If QML and XGBoost disagree strongly, the row is marked for review.

This is a safe presentation position because we are not claiming full quantum
advantage. We are showing that QML can lead the research signal while XGBoost
acts as a practical current benchmark.

## Main Dataset

Main source:

[Hugging Face Materials Project snapshot](https://huggingface.co/datasets/xpanceo-team/materials-project)

The large raw parquet files are not the main GitHub focus. The repo keeps the
scripts, processed summaries, and presentation artifacts needed to explain and
reproduce the project.

## Current Results

- Full raw dataset: 210,579 rows
- Lithium-only dataset: 24,957 rows
- India-scored lithium dataset: 24,957 rows and 37 columns
- Final India battery shortlist: 629 rows
- Hybrid DSS compound ranking: 629 rows and 22 columns
- Supporting battery-family context: 6 rows
- QML-ready balanced dataset: 1,000 rows and 27 columns
- XGBoost classifier accuracy: 0.9091
- XGBoost stable recall: 0.7000
- XGBoost stable F1: 0.7100
- Repeated-split best QML mean accuracy: 0.8550
- Repeated-split best QML mean stable recall: 0.8800
- Repeated-split best QML mean stable F1: 0.8583
- QML vs Logistic Regression mean accuracy: 0.8550 vs 0.8410
- QML vs Logistic Regression mean stable F1: 0.8583 vs 0.8473
- Same-data XGBoost accuracy on the first QML-ready test split: 0.8300

## Top Hybrid DSS Compounds

| Rank | Formula | Material ID | Battery Context | QML Stable Prob. | XGBoost Stable Prob. | Hybrid Score |
| ---: | --- | --- | --- | ---: | ---: | ---: |
| 1 | `SrLi2SiO4` | `mp-1191141` | Silicon-family | 0.8502 | 0.8252 | 88.4616 |
| 2 | `Li2MnGeS4` | `mp-3268644` | Li-S or sulfide-family | 0.8453 | 0.9033 | 87.7709 |
| 3 | `LiGaSiO4` | `mp-18147` | Silicon-family | 0.8516 | 0.8054 | 87.5647 |
| 4 | `SrLi2SnS4` | `mp-3210567` | Li-S or sulfide-family | 0.8670 | 0.8955 | 87.2890 |
| 5 | `Rb2Li2SnS4` | `mp-3205208` | Li-S or sulfide-family | 0.8569 | 0.9042 | 87.2332 |

These are DSS research-screening candidates, not final commercial purchase
instructions.

## Pipeline

1. Download Materials Project snapshot.
2. Filter materials that contain lithium.
3. Add India feasibility scores and battery-family labels.
4. Run EDA.
5. Train XGBoost baseline models.
6. Apply India and safety filters after prediction.
7. Create the final India battery shortlist.
8. Create the QML-ready balanced dataset.
9. Train and tune simulated QML kernel classifiers.
10. Validate best QML across repeated random train/test splits.
11. Compare best QML with Logistic Regression and same-data XGBoost.
12. Create a QML circuit diagram.
13. Create QML-primary hybrid DSS recommendation rankings.
14. Regenerate the presentation notebook with saved outputs.

## Important Files

| File | Purpose |
| --- | --- |
| `Student Level Project Flow.md` | Safe student-level explanation of the project story. |
| `Project understanding.md` | Main project understanding document. |
| `Battery Materials DSS QML Main Presentation.ipynb` | Presentation notebook with outputs in every cell. |
| `scripts/create_dss_recommendation_ranking.py` | Creates the QML-primary hybrid recommendation table. |
| `scripts/create_main_presentation_notebook.py` | Regenerates the presentation notebook. |
| `scripts/train_xgboost_baseline.py` | Trains XGBoost baseline models. |
| `scripts/run_best_qml_repeated_splits.py` | Runs repeated-split validation for best QML. |
| `scripts/create_qml_circuit_diagram.py` | Creates the QML circuit diagram. |
| `data/processed/hybrid qml xgboost compound ranking.csv` | Main hybrid compound ranking table. |
| `data/processed/dss compound recommendation ranking.csv` | Same compound ranking table for DSS naming. |
| `data/metadata/dss_recommendation_summary.md` | Summary of final DSS ranking logic. |
| `data/processed/qml circuit diagram.png` | Circuit visual for presentation. |

## Why XGBoost

XGBoost is used because the project data is tabular. It handles numeric,
boolean, and encoded categorical features well. It is also strong enough to be a
serious classical benchmark.

Classifier settings:

| Hyperparameter | Value |
| --- | ---: |
| `n_estimators` | 250 |
| `max_depth` | 5 |
| `learning_rate` | 0.05 |
| `subsample` | 0.90 |
| `colsample_bytree` | 0.90 |
| `objective` | `binary:logistic` |
| `eval_metric` | `logloss` |

These are conservative, explainable settings suitable for a student project.

## Why QML

Battery materials are quantum systems at atomic scale. QML is included because
quantum feature spaces are a future direction for material discovery.

The project does not use PennyLane. The QML kernel is simulated with NumPy and
then used as a precomputed kernel for an SVM classifier.

Final QML setup:

| Parameter | Value |
| --- | --- |
| Features | `formation_energy_per_atom`, `has_o`, `space_group_number`, `theoretical` |
| Qubits | 4 |
| Kernel | `entangled_pi` |
| Angle scale | `pi` |
| Entanglement strength | `pi` |
| SVM `C` | 5.0 |
| Rows per class | 500 stable + 500 unstable |
| Validation | 10 random train/test splits |

## Reproduce Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the final DSS and notebook scripts:

```bash
python3 scripts/create_dss_recommendation_ranking.py
python3 scripts/create_main_presentation_notebook.py
```

Run the complete pipeline if rebuilding from earlier stages:

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
