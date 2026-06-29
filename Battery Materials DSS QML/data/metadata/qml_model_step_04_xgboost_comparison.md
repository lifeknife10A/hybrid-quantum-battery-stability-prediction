# QML Model Step 04: XGBoost Comparison

Generated on: 2026-06-28

## Comparison Table

| model | dataset | accuracy | stable_precision | stable_recall | stable_f1 | test_rows |
| --- | --- | --- | --- | --- | --- | --- |
| QML quantum kernel | QML-ready balanced dataset | 0.8100 | 0.7870 | 0.8500 | 0.8173 | 200 |
| XGBoost same QML-ready data | QML-ready balanced dataset | 0.8300 | 0.8367 | 0.8200 | 0.8283 | 200 |
| XGBoost full project baseline | Full lithium India-scored dataset | 0.9091 | 0.7300 | 0.7000 | 0.7100 | 4992 |

## How To Read This

- `QML quantum kernel` is the simple simulated QML model trained on the
  QML-ready dataset.
- `XGBoost same QML-ready data` is the fair same-split comparison.
- `XGBoost full project baseline` is the existing project baseline from
  `data/metadata/xgboost_baseline_results.md`.

The same-data XGBoost comparison is the fairest direct comparison because it
uses the same 1,000-row balanced file and the same train/test split.
