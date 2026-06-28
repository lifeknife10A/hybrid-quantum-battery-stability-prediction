# QML Best Model Summary

Generated on: 2026-06-28

## Best Tuned Model

| feature_count | feature_names | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 1 | 256 | 800 | 4 | 0.8038 | 0.7732 | 0.8600 | 0.8141 |

## Final Test Metrics

| accuracy | stable_precision | stable_recall | stable_f1 |
| --- | --- | --- | --- |
| 0.8200 | 0.7963 | 0.8600 | 0.8269 |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 78 | 22 |
| stable_1 | 14 | 86 |

## Comparison Against Previous Baselines

| model | test_accuracy | test_stable_f1 |
| --- | --- | --- |
| Original QML baseline | 0.8100 | 0.8173 |
| Tuned QML best model | 0.8200 | 0.8269 |
| Same-data XGBoost baseline | 0.8300 | 0.8283 |

## Files Created

- `scripts/tune_qml_baseline.py`
- `data/processed/qml tuning results.csv`
- `data/processed/qml tuned best predictions.csv`
- `data/metadata/qml_tuning_results.md`
- `data/metadata/qml_best_model_summary.md`
- `data/metadata/qml_tuning_step_01_search_space.md`
- `data/metadata/qml_tuning_step_02_validation_results.md`
- `data/metadata/qml_tuning_step_03_best_model_test.md`
