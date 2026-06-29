# Improved QML Step 05: Threshold Experiment

Generated on: 2026-06-28

## Purpose

The QML model gives a stable-class probability. The normal prediction rule uses
`0.50` as the cutoff:

- probability >= 0.50 means stable
- probability < 0.50 means unstable

This experiment checks whether a different cutoff gives better stable-class
F1-score. The threshold is selected using cross-validation on the
train-validation split only. The test set is used only after the threshold is
selected.

## Thresholds Tested

[0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]

## Cross-Validation Results

| stable_threshold | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- |
| 0.3000 | 0.8450 | 0.8245 | 0.8850 | 0.8520 |
| 0.3500 | 0.8512 | 0.8381 | 0.8775 | 0.8559 |
| 0.4000 | 0.8500 | 0.8406 | 0.8700 | 0.8537 |
| 0.4500 | 0.8525 | 0.8464 | 0.8675 | 0.8554 |
| 0.5000 | 0.8562 | 0.8542 | 0.8650 | 0.8581 |
| 0.5500 | 0.8500 | 0.8524 | 0.8525 | 0.8511 |
| 0.6000 | 0.8475 | 0.8577 | 0.8375 | 0.8466 |
| 0.6500 | 0.8412 | 0.8562 | 0.8250 | 0.8391 |
| 0.7000 | 0.8375 | 0.8552 | 0.8175 | 0.8346 |

## Best Cross-Validation Threshold

| stable_threshold | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- |
| 0.5000 | 0.8562 | 0.8542 | 0.8650 | 0.8581 |

## Test Result With Selected Threshold

| selected_stable_threshold | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- |
| 0.5000 | 0.8200 | 0.7963 | 0.8600 | 0.8269 |

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

`data/processed/improved qml threshold predictions.csv`

Rows saved: 200
