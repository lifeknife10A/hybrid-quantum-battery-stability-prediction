# Improved QML Step 05: Threshold Experiment

Generated on: 2026-07-04

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
| 0.3000 | 0.8587 | 0.8466 | 0.8800 | 0.8622 |
| 0.3500 | 0.8575 | 0.8462 | 0.8775 | 0.8608 |
| 0.4000 | 0.8525 | 0.8446 | 0.8675 | 0.8552 |
| 0.4500 | 0.8562 | 0.8510 | 0.8675 | 0.8583 |
| 0.5000 | 0.8575 | 0.8531 | 0.8675 | 0.8594 |
| 0.5500 | 0.8512 | 0.8531 | 0.8525 | 0.8518 |
| 0.6000 | 0.8500 | 0.8529 | 0.8500 | 0.8504 |
| 0.6500 | 0.8462 | 0.8574 | 0.8350 | 0.8448 |
| 0.7000 | 0.8388 | 0.8614 | 0.8125 | 0.8346 |

## Best Cross-Validation Threshold

| stable_threshold | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- |
| 0.3000 | 0.8587 | 0.8466 | 0.8800 | 0.8622 |

## Test Result With Selected Threshold

| selected_stable_threshold | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- |
| 0.3000 | 0.8300 | 0.8000 | 0.8800 | 0.8381 |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 78 | 22 |
| stable_1 | 12 | 88 |

## Classification Report

```text
              precision    recall  f1-score   support

    unstable       0.87      0.78      0.82       100
      stable       0.80      0.88      0.84       100

    accuracy                           0.83       200
   macro avg       0.83      0.83      0.83       200
weighted avg       0.83      0.83      0.83       200

```

## Prediction Output

`data/processed/improved qml threshold predictions.csv`

Rows saved: 200
