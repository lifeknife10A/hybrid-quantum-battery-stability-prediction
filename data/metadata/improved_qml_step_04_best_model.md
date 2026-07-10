# Improved QML Step 04: Best Model

Generated on: 2026-07-04

## Best Improved QML Test Result

| pca_component_count | kernel_name | angle_scale | c_value | quantum_state_size | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | entangled_pi | pi | 1 | 256 | 0.8200 | 0.8077 | 0.8400 | 0.8235 |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 80 | 20 |
| stable_1 | 16 | 84 |

## Classification Report

```text
              precision    recall  f1-score   support

    unstable       0.83      0.80      0.82       100
      stable       0.81      0.84      0.82       100

    accuracy                           0.82       200
   macro avg       0.82      0.82      0.82       200
weighted avg       0.82      0.82      0.82       200

```

## Prediction Output

`data/processed/improved qml best predictions.csv`

Rows saved: 200

## Comparison

| model | test_accuracy | test_stable_f1 |
| --- | --- | --- |
| Original QML baseline | 0.8100 | 0.8173 |
| Tuned QML baseline | 0.8200 | 0.8269 |
| Improved QML separate experiment | 0.8200 | 0.8235 |
| Improved QML with threshold tuning | 0.8300 | 0.8381 |
| Improved QML with kernel alignment | 0.8200 | 0.8302 |
| Same-data XGBoost baseline | 0.8300 | 0.8283 |
