# QML Tuning Step 03: Best Model Test

Generated on: 2026-06-28

## Best Tuned QML Test Result

| feature_count | angle_scale | angle_scale_value | c_value | quantum_state_size | cv_accuracy | cv_stable_f1 | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | pi_over_2 | 1.5708 | 1 | 256 | 0.8038 | 0.8141 | 0.8200 | 0.7963 | 0.8600 | 0.8269 |

## Selected Features

| selected_feature |
| --- |
| scaled_space_group_number |
| scaled_band_gap |
| scaled_formation_energy_per_atom |
| scaled_number_of_elements |
| scaled_has_fe |
| scaled_has_p |
| scaled_has_mn |
| scaled_has_c |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 78 | 22 |
| stable_1 | 14 | 86 |

## Classification Report

```text
              precision    recall  f1-score   support

    unstable       0.85      0.78      0.81       100
      stable       0.80      0.86      0.83       100

    accuracy                           0.82       200
   macro avg       0.82      0.82      0.82       200
weighted avg       0.82      0.82      0.82       200

```

## Prediction Output

`data/processed/qml tuned best predictions.csv`

Rows saved: 200

## Kernel Matrix Shapes

- Train-validation kernel: (800, 800)
- Test kernel: (200, 800)
