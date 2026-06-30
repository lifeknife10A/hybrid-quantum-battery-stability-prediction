# Battery Materials DSS QML

This project builds a simple, student-friendly pipeline for lithium-ion battery
material discovery with an India-first screening layer.

The main product is a Decision Support System. XGBoost is used as the strong
current classical ML benchmark. Simulated QML is used as a quantum-future
experiment, not as an unsupported claim that quantum already beats every
classical model.

## Problem

The main goal is to find lithium battery material candidates that are:

- scientifically promising,
- useful for battery research,
- compatible with India-focused supply-chain and safety priorities,
- suitable for comparison between classical ML and QML models.

The final recommendation is compound-level. The DSS should recommend exact
formulas such as `LiFePO4` or `Li3Fe2(PO4)3`, not only element names or broad
families like LFP.

## Why Quantum Is Included

Battery materials are controlled by atomic and electronic behavior. That
behavior is quantum mechanical. Classical ML is useful today, but future
quantum computers may be able to represent material interactions more naturally.

For this student-level project, the quantum section is used to explore that
future direction. The safe claim is:

> XGBoost is our strong present-day benchmark. Simulated QML is our
> future-facing experiment. QML is not presented as a full replacement for
> XGBoost, but as a first step toward quantum-assisted materials discovery.

## Student-Level Flow

1. Start with a large public Materials Project dataset.
2. Filter lithium-containing materials.
3. Add India-focused feasibility and battery-family rules.
4. Train XGBoost as the strong classical benchmark.
5. Train simple classical and simulated QML models on a balanced QML-ready task.
6. Compare QML with Logistic Regression and XGBoost.
7. Use DSS ranking tables to recommend exact compound formulas.
8. Explain the quantum part as future-facing evidence, not as unsupported
   quantum superiority.

## Main Dataset

Main source:

[Hugging Face Materials Project snapshot](https://huggingface.co/datasets/xpanceo-team/materials-project)

The raw parquet files are not committed to GitHub because they are large. The
project keeps scripts and summaries so the dataset can be reproduced locally.

## Current Pipeline

1. Download Materials Project dataset.
2. Filter materials that contain lithium.
3. Add India feasibility scores and battery-family labels.
4. Run EDA.
5. Train XGBoost baseline models as the strong classical benchmark.
6. Apply India and safety filters after prediction.
7. Create the final India battery shortlist.
8. Create the QML-ready balanced dataset.
9. Train and compare the first simple simulated QML classifier.
10. Tune QML feature count, angle scale, and SVM `C`.
11. Run a separate improved-QML section using feature importance, PCA, and
    entangled-kernel testing.
12. Test probability-threshold tuning for the improved-QML model.
13. Test quantum-kernel alignment feature selection.
14. Validate the best QML setup across repeated random train/test splits.
15. Compare best QML with Logistic Regression as a simpler classical baseline.
16. Add a gate-level visual diagram for the best 4-qubit QML feature map.
17. Create DSS recommendation rankings for exact compound formulas.

## Current Results

- Full raw dataset: 210,579 rows
- Lithium-only dataset: 24,957 rows
- India-scored lithium dataset: 24,957 rows and 37 columns
- Final India battery shortlist: 629 rows
- DSS compound recommendation ranking: 629 rows
- Supporting battery-family context: 6 rows
- QML-ready balanced dataset: 1,000 rows and 27 columns
- XGBoost classifier accuracy: 0.9091
- XGBoost regressor MAE: 0.1005
- QML quantum-kernel accuracy on QML-ready test split: 0.8100
- Tuned QML quantum-kernel accuracy on QML-ready test split: 0.8200
- Tuned QML stable F1 on QML-ready test split: 0.8269
- Improved QML separate-section accuracy: 0.8150
- Improved QML separate-section stable F1: 0.8230
- Improved QML threshold-tuned accuracy: 0.8200
- Improved QML threshold-tuned stable F1: 0.8269
- Improved QML alignment-selected accuracy: 0.8200
- Improved QML alignment-selected stable F1: 0.8302
- Repeated-split best QML mean accuracy: 0.8550
- Repeated-split best QML mean stable F1: 0.8583
- QML vs Logistic Regression mean accuracy: 0.8550 vs 0.8410
- QML vs Logistic Regression mean stable F1: 0.8583 vs 0.8473
- Same-data XGBoost accuracy on QML-ready test split: 0.8300

## Important Files

| File | Purpose |
| --- | --- |
| `Student Level Project Flow.md` | Safe student-level explanation of the full project story. |
| `Project understanding.md` | Main project understanding document. |
| `Battery Materials DSS QML Main Presentation.ipynb` | Presentation-ready notebook with outputs in every cell. |
| `Indian Battery Materials Report.docx` | Report on India-relevant battery materials. |
| `Literature Review.xlsx` | Literature review workbook. |
| `scripts/process_materials_project_dataset.py` | Creates the lithium-filtered dataset. |
| `scripts/create_lithium_india_scored_dataset.py` | Adds India feasibility scoring. |
| `scripts/create_lithium_india_scored_eda.py` | Creates EDA summary. |
| `scripts/train_xgboost_baseline.py` | Trains XGBoost baseline models. |
| `scripts/create_final_india_battery_shortlist.py` | Creates the final India shortlist. |
| `scripts/create_qml_ready_dataset.py` | Creates the balanced and scaled QML-ready dataset. |
| `scripts/train_qml_baseline.py` | Trains the first simple QML classifier and compares it with XGBoost. |
| `scripts/tune_qml_baseline.py` | Tunes QML feature count, angle scale, and SVM `C`. |
| `scripts/run_improved_qml_experiments.py` | Runs the separate improved-QML section with feature importance, PCA, and entangled kernels. |
| `scripts/compare_qml_with_logistic_baseline.py` | Compares best QML with Logistic Regression on repeated balanced splits. |
| `scripts/create_qml_circuit_diagram.py` | Creates the gate-level QML circuit diagram and explanation. |
| `scripts/create_dss_recommendation_ranking.py` | Creates DSS compound recommendation rankings. |
| `scripts/create_main_presentation_notebook.py` | Regenerates the presentation notebook. |
| `data/metadata/project_pipeline_summary.md` | Full current pipeline summary. |
| `data/metadata/qml_baseline_results.md` | QML classifier results and XGBoost comparison. |
| `data/metadata/qml_tuning_results.md` | QML hyperparameter tuning results. |
| `data/metadata/qml_best_model_summary.md` | Best tuned QML model summary. |
| `data/metadata/improved_qml_section_summary.md` | Separate improved-QML section summary. |
| `data/metadata/improved_qml_step_05_threshold_experiment.md` | Separate improved-QML threshold experiment. |
| `data/metadata/improved_qml_step_06_kernel_alignment.md` | Separate quantum-kernel alignment experiment. |
| `data/metadata/improved_qml_step_07_repeated_split_validation.md` | Repeated train/test split validation for the best QML setup. |
| `data/metadata/improved_qml_step_08_qml_vs_logistic.md` | Repeated-split QML vs Logistic Regression comparison. |
| `data/metadata/qml_circuit_diagram_summary.md` | Gate-level explanation of the best QML feature map. |
| `data/metadata/dss_recommendation_summary.md` | DSS explanation and recommendation ranking summary. |
| `data/processed/qml circuit diagram.png` | Visual QML circuit diagram for presentation. |
| `data/processed/dss compound recommendation ranking.csv` | Main compound-level DSS recommendation table. |
| `data/processed/dss material recommendation ranking.csv` | Backward-compatible copy of the compound recommendation table. |
| `data/processed/dss battery family recommendation ranking.csv` | Supporting family context table. |

## Reproduce Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run scripts from the project folder:

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

## Next Step

Convert the final presentation into a student-defensible story: DSS first,
XGBoost as the strong current benchmark, and simulated QML as the future-facing
quantum experiment.
