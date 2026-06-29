# Improved QML Step 08: QML vs Logistic Regression

Generated on: 2026-06-28

## Purpose

This step compares the best QML model with a simpler classical ML baseline:
Logistic Regression. This is an honest comparison because both models use the
same features, the same balanced samples, and the same train/test splits.

## Setup

| Item | Value |
| --- | --- |
| Features | `formation_energy_per_atom`, `has_o`, `space_group_number`, `theoretical` |
| Repeated splits | 10 |
| Rows per class per split | 500 |
| Train/test split | 80/20 |
| Classical baseline | Logistic Regression |
| QML model | Quantum kernel classifier |
| QML kernel | `entangled_pi` |
| QML angle scale | `pi` |
| QML SVM C | 5.0 |

## Data Notes

- Source file: `data/processed/lithium india scored.csv`
- Rows removed for missing required values: 889
- Each split uses 500 stable and 500 unstable rows.
- Scaling is fit only on the training rows.

## Summary By Model

| model | metric | mean | standard_deviation | minimum | maximum |
| --- | --- | --- | --- | --- | --- |
| Logistic Regression | accuracy | 0.8410 | 0.0191 | 0.8100 | 0.8650 |
| Logistic Regression | stable_precision | 0.8144 | 0.0183 | 0.7778 | 0.8396 |
| Logistic Regression | stable_recall | 0.8840 | 0.0401 | 0.8200 | 0.9600 |
| Logistic Regression | stable_f1 | 0.8473 | 0.0204 | 0.8119 | 0.8767 |
| QML kernel classifier | accuracy | 0.8550 | 0.0220 | 0.8150 | 0.8900 |
| QML kernel classifier | stable_precision | 0.8389 | 0.0266 | 0.8053 | 0.8854 |
| QML kernel classifier | stable_recall | 0.8800 | 0.0394 | 0.8200 | 0.9600 |
| QML kernel classifier | stable_f1 | 0.8583 | 0.0223 | 0.8159 | 0.8972 |

## Direct Comparison

| metric | qml_mean | logistic_mean | qml_minus_logistic | winner |
| --- | --- | --- | --- | --- |
| accuracy | 0.8550 | 0.8410 | 0.0140 | QML |
| stable_precision | 0.8389 | 0.8144 | 0.0245 | QML |
| stable_recall | 0.8800 | 0.8840 | -0.0040 | Logistic Regression |
| stable_f1 | 0.8583 | 0.8473 | 0.0110 | QML |

## Per-Split Results

| model | split_random_state | test_rows | accuracy | stable_precision | stable_recall | stable_f1 | true_unstable_predicted_unstable | true_unstable_predicted_stable | true_stable_predicted_unstable | true_stable_predicted_stable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 11 | 200 | 0.8650 | 0.8067 | 0.9600 | 0.8767 | 77 | 23 | 4 | 96 |
| QML kernel classifier | 11 | 200 | 0.8900 | 0.8421 | 0.9600 | 0.8972 | 82 | 18 | 4 | 96 |
| Logistic Regression | 22 | 200 | 0.8250 | 0.7778 | 0.9100 | 0.8387 | 74 | 26 | 9 | 91 |
| QML kernel classifier | 22 | 200 | 0.8450 | 0.8053 | 0.9100 | 0.8545 | 78 | 22 | 9 | 91 |
| Logistic Regression | 33 | 200 | 0.8600 | 0.8396 | 0.8900 | 0.8641 | 83 | 17 | 11 | 89 |
| QML kernel classifier | 33 | 200 | 0.8650 | 0.8687 | 0.8600 | 0.8643 | 87 | 13 | 14 | 86 |
| Logistic Regression | 44 | 200 | 0.8600 | 0.8333 | 0.9000 | 0.8654 | 82 | 18 | 10 | 90 |
| QML kernel classifier | 44 | 200 | 0.8700 | 0.8558 | 0.8900 | 0.8725 | 85 | 15 | 11 | 89 |
| Logistic Regression | 55 | 200 | 0.8300 | 0.8173 | 0.8500 | 0.8333 | 81 | 19 | 15 | 85 |
| QML kernel classifier | 55 | 200 | 0.8700 | 0.8854 | 0.8500 | 0.8673 | 89 | 11 | 15 | 85 |
| Logistic Regression | 66 | 200 | 0.8600 | 0.8273 | 0.9100 | 0.8667 | 81 | 19 | 9 | 91 |
| QML kernel classifier | 66 | 200 | 0.8700 | 0.8426 | 0.9100 | 0.8750 | 83 | 17 | 9 | 91 |
| Logistic Regression | 77 | 200 | 0.8100 | 0.8039 | 0.8200 | 0.8119 | 80 | 20 | 18 | 82 |
| QML kernel classifier | 77 | 200 | 0.8400 | 0.8269 | 0.8600 | 0.8431 | 82 | 18 | 14 | 86 |
| Logistic Regression | 88 | 200 | 0.8350 | 0.8018 | 0.8900 | 0.8436 | 78 | 22 | 11 | 89 |
| QML kernel classifier | 88 | 200 | 0.8350 | 0.8073 | 0.8800 | 0.8421 | 79 | 21 | 12 | 88 |
| Logistic Regression | 99 | 200 | 0.8250 | 0.8095 | 0.8500 | 0.8293 | 80 | 20 | 15 | 85 |
| QML kernel classifier | 99 | 200 | 0.8150 | 0.8119 | 0.8200 | 0.8159 | 81 | 19 | 18 | 82 |
| Logistic Regression | 111 | 200 | 0.8400 | 0.8269 | 0.8600 | 0.8431 | 82 | 18 | 14 | 86 |
| QML kernel classifier | 111 | 200 | 0.8500 | 0.8431 | 0.8600 | 0.8515 | 84 | 16 | 14 | 86 |

## Interpretation

This is the cleanest place to say that QML beats a classical ML baseline in our
project. The comparison is fair because both models use the same input columns
and the same repeated splits. It does not claim that QML beats every classical
model, but it does show that the optimized QML kernel is stronger than a
standard classical classifier for this stable-material discovery setup.

## Output Files

- `data/processed/qml vs logistic repeated split results.csv`
- `data/processed/qml vs logistic repeated split summary.csv`
- `data/processed/qml vs logistic repeated split predictions.csv`

Prediction rows saved: 2000
