# Improved QML Step 04: Best Model

Generated on: 2026-06-28

## Best Improved QML Test Result

| pca_component_count | kernel_name | angle_scale | c_value | quantum_state_size | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | entangled_pi | pi | 2 | 64 | 0.8150 | 0.7890 | 0.8600 | 0.8230 |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 77 | 23 |
| stable_1 | 14 | 86 |

## Classification Report

```text
              precision    recall  f1-score   support

    unstable       0.85      0.77      0.81       100
      stable       0.79      0.86      0.82       100

    accuracy                           0.81       200
   macro avg       0.82      0.81      0.81       200
weighted avg       0.82      0.81      0.81       200

```

## Prediction Output

`data/processed/improved qml best predictions.csv`

Rows saved: 200

## Comparison

| model | test_accuracy | test_stable_f1 |
| --- | --- | --- |
| Original QML baseline | 0.8100 | 0.8173 |
| Tuned QML baseline | 0.8200 | 0.8269 |
| Improved QML separate experiment | 0.8150 | 0.8230 |
| Same-data XGBoost baseline | 0.8300 | 0.8283 |
