# Summer Vacation Battery Materials Project

This project builds a simple, student-friendly pipeline for lithium-ion battery
material discovery with an India-first screening layer.

## Problem

The main goal is to find lithium battery material candidates that are:

- scientifically promising,
- useful for battery research,
- compatible with India-focused supply-chain and safety priorities,
- suitable for comparison between classical ML and future QML models.

## Main Dataset

Main source:

[Hugging Face Materials Project snapshot](https://huggingface.co/datasets/xpanceo-team/materials-project)

The raw parquet files are not committed to GitHub because they are large. The
project keeps scripts and summaries so the dataset can be reproduced locally.
The local PDF references in `Paper/` are also not uploaded because this
repository is public.

## Current Pipeline

1. Download Materials Project dataset.
2. Filter materials that contain lithium.
3. Add India feasibility scores and battery-family labels.
4. Run EDA.
5. Train XGBoost baseline models.
6. Apply India and safety filters after prediction.
7. Create the final India battery shortlist.

## Current Results

- Full raw dataset: 210,579 rows
- Lithium-only dataset: 24,957 rows
- India-scored lithium dataset: 24,957 rows and 37 columns
- Final India battery shortlist: 629 rows
- XGBoost classifier accuracy: 0.9091
- XGBoost regressor MAE: 0.1005

## Important Files

| File | Purpose |
| --- | --- |
| `Project understanding.md` | Main project understanding document. |
| `Indian Battery Materials Report.docx` | Report on India-relevant battery materials. |
| `Literature Review.xlsx` | Literature review workbook. |
| `scripts/process_materials_project_dataset.py` | Creates the lithium-filtered dataset. |
| `scripts/create_lithium_india_scored_dataset.py` | Adds India feasibility scoring. |
| `scripts/create_lithium_india_scored_eda.py` | Creates EDA summary. |
| `scripts/train_xgboost_baseline.py` | Trains XGBoost baseline models. |
| `scripts/create_final_india_battery_shortlist.py` | Creates the final India shortlist. |
| `data/metadata/project_pipeline_summary.md` | Full current pipeline summary. |

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
```

## Next Step

Create a QML-ready dataset and compare a simple QML classifier against the
current XGBoost baseline.
