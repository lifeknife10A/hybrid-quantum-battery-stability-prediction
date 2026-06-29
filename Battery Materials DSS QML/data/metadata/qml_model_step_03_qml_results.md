# QML Model Step 03: QML Results

Generated on: 2026-06-28

## QML Metrics

| model | dataset | accuracy | stable_precision | stable_recall | stable_f1 | test_rows |
| --- | --- | --- | --- | --- | --- | --- |
| QML quantum kernel | QML-ready balanced dataset | 0.8100 | 0.7870 | 0.8500 | 0.8173 | 200 |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 77 | 23 |
| stable_1 | 15 | 85 |

## Classification Report

```text
              precision    recall  f1-score   support

    unstable       0.84      0.77      0.80       100
      stable       0.79      0.85      0.82       100

    accuracy                           0.81       200
   macro avg       0.81      0.81      0.81       200
weighted avg       0.81      0.81      0.81       200

```
