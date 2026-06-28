# Summer Vacation Battery Materials Project

This project builds a simple, student-friendly pipeline for lithium-ion battery
material discovery with an India-first screening layer.

## Problem

The main goal is to find lithium battery material candidates that are:

- scientifically promising,
- useful for battery research,
- compatible with India-focused supply-chain and safety priorities,
- suitable for comparison between classical ML and QML models.

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
5. Train XGBoost baseline models.
6. Apply India and safety filters after prediction.
7. Create the final India battery shortlist.
8. Create the QML-ready balanced dataset.
9. Train and compare the first simple QML classifier.
10. Tune QML feature count, angle scale, and SVM `C`.
11. Run a separate improved-QML section using feature importance, PCA, and
    entangled-kernel testing.
12. Test probability-threshold tuning for the improved-QML model.
13. Test quantum-kernel alignment feature selection.
14. Validate the best QML setup across repeated random train/test splits.

## Current Results

- Full raw dataset: 210,579 rows
- Lithium-only dataset: 24,957 rows
- India-scored lithium dataset: 24,957 rows and 37 columns
- Final India battery shortlist: 629 rows
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
- Same-data XGBoost accuracy on QML-ready test split: 0.8300

## Important Files

| File | Purpose |
| --- | --- |
| `Project understanding.md` | Main project understanding document. |
| `Summer Vacation Main Presentation.ipynb` | Presentation-ready notebook with outputs in every cell. |
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
| `scripts/create_main_presentation_notebook.py` | Regenerates the presentation notebook. |
| `data/metadata/project_pipeline_summary.md` | Full current pipeline summary. |
| `data/metadata/qml_baseline_results.md` | QML classifier results and XGBoost comparison. |
| `data/metadata/qml_tuning_results.md` | QML hyperparameter tuning results. |
| `data/metadata/qml_best_model_summary.md` | Best tuned QML model summary. |
| `data/metadata/improved_qml_section_summary.md` | Separate improved-QML section summary. |
| `data/metadata/improved_qml_step_05_threshold_experiment.md` | Separate improved-QML threshold experiment. |
| `data/metadata/improved_qml_step_06_kernel_alignment.md` | Separate quantum-kernel alignment experiment. |
| `data/metadata/improved_qml_step_07_repeated_split_validation.md` | Repeated train/test split validation for the best QML setup. |

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
```

## Next Step

Create the final report section comparing XGBoost, the original QML baseline,
tuned QML, threshold QML, kernel-alignment QML, and the India-focused material
shortlist.
