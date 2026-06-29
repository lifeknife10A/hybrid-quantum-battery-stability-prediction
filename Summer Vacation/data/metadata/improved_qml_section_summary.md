# Improved QML Separate Section Summary

Generated on: 2026-06-28

## Goal

Try a separate improved-QML experiment using feature importance, PCA, and an
optional entangled quantum-kernel simulation.

## Files Created

- `scripts/run_improved_qml_experiments.py`
- `data/processed/improved qml feature pca.csv`
- `data/processed/improved qml tuning results.csv`
- `data/processed/improved qml best predictions.csv`
- `data/processed/improved qml threshold results.csv`
- `data/processed/improved qml threshold predictions.csv`
- `data/processed/improved qml alignment scores.csv`
- `data/processed/improved qml alignment results.csv`
- `data/processed/improved qml alignment predictions.csv`
- `data/metadata/improved_qml_step_01_feature_importance.md`
- `data/metadata/improved_qml_step_02_pca_dataset.md`
- `data/metadata/improved_qml_step_03_tuning_results.md`
- `data/metadata/improved_qml_step_04_best_model.md`
- `data/metadata/improved_qml_step_05_threshold_experiment.md`
- `data/metadata/improved_qml_step_06_kernel_alignment.md`

## Best Improved QML Result

| pca_component_count | kernel_name | angle_scale | c_value | quantum_state_size | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | entangled_pi | pi | 2 | 64 | 0.8150 | 0.7890 | 0.8600 | 0.8230 |

## Threshold Experiment Result

| selected_stable_threshold | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- |
| 0.5000 | 0.8200 | 0.7963 | 0.8600 | 0.8269 |

## Kernel Alignment Experiment Result

| feature_set_name | feature_count | kernel_name | angle_scale | c_value | kernel_target_alignment | quantum_state_size | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rf_top_4 | 4 | entangled_pi | pi | 5 | 0.3785 | 16 | 0.8200 | 0.7857 | 0.8800 | 0.8302 |

## Comparison Against Existing Results

| model | test_accuracy | test_stable_f1 |
| --- | --- | --- |
| Original QML baseline | 0.8100 | 0.8173 |
| Tuned QML baseline | 0.8200 | 0.8269 |
| Improved QML separate experiment | 0.8150 | 0.8230 |
| Improved QML with threshold tuning | 0.8200 | 0.8269 |
| Improved QML with kernel alignment | 0.8200 | 0.8302 |
| Same-data XGBoost baseline | 0.8300 | 0.8283 |

## Interpretation

This experiment is useful because it tests a more advanced QML preparation
route. The result should be reported as a separate experiment, not as a
replacement for the original baseline.
