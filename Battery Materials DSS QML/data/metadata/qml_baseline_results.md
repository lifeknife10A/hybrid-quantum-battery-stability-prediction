# QML Baseline Results

Generated on: 2026-06-28

## Input

`data/processed/qml_ready_lithium_india.csv`

## Prediction Output

`data/processed/qml baseline predictions.csv`

## Goal

Train the first simple QML classifier and compare it with XGBoost.

## Model Used

Simulated quantum kernel classifier with one qubit per scaled feature.

## Main Comparison

| model | dataset | accuracy | stable_precision | stable_recall | stable_f1 | test_rows |
| --- | --- | --- | --- | --- | --- | --- |
| QML quantum kernel | QML-ready balanced dataset | 0.8100 | 0.7870 | 0.8500 | 0.8173 | 200 |
| XGBoost same QML-ready data | QML-ready balanced dataset | 0.8300 | 0.8367 | 0.8200 | 0.8283 | 200 |
| XGBoost full project baseline | Full lithium India-scored dataset | 0.9091 | 0.7300 | 0.7000 | 0.7100 | 4992 |

## QML Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 77 | 23 |
| stable_1 | 15 | 85 |

## Prediction Rows Saved

200 test-set prediction rows were saved.

## Conclusion

The QML model is working as a first baseline. On the same QML-ready dataset,
XGBoost is still slightly stronger, but the QML model is close enough to be
useful for project comparison and future QML improvement.

## Step Markdown Files

| step | file | purpose |
| --- | --- | --- |
| 01 | `data/metadata/qml_model_step_01_training_data.md` | Training data setup |
| 02 | `data/metadata/qml_model_step_02_quantum_kernel.md` | Quantum kernel method |
| 03 | `data/metadata/qml_model_step_03_qml_results.md` | QML metrics |
| 04 | `data/metadata/qml_model_step_04_xgboost_comparison.md` | XGBoost comparison |
| 05 | `data/metadata/qml_model_step_05_interpretation.md` | Interpretation |
