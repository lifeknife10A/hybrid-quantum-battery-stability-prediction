# Improved QML Step 07: Repeated Split Validation

Generated on: 2026-06-28

## Purpose

This step checks whether the best QML setup is stable across multiple random
train/test splits. A single 200-row test split can be lucky or unlucky, so this
validation repeats the experiment with different random seeds.

## Best QML Setup Tested

| Parameter | Value |
| --- | --- |
| Features | `formation_energy_per_atom`, `has_o`, `space_group_number`, `theoretical` |
| Qubits | 4 |
| Kernel | `entangled_pi` |
| Angle scale | `pi` |
| SVM C | 5.0 |
| Rows per class per split | 500 |
| Train/test split | 80/20 |
| Random states | [11, 22, 33, 44, 55, 66, 77, 88, 99, 111] |

## Data Notes

- Source file: `data/processed/lithium india scored.csv`
- Rows removed for missing required values: 889
- Each split uses a fresh balanced sample of 500 stable and 500 unstable rows.
- The scaler is fit only on the training rows for that split.
- The test rows are not used during training.

## Per-Split Results

| split_random_state | train_rows | test_rows | stable_train_rows | unstable_train_rows | stable_test_rows | unstable_test_rows | accuracy | stable_precision | stable_recall | stable_f1 | true_unstable_predicted_unstable | true_unstable_predicted_stable | true_stable_predicted_unstable | true_stable_predicted_stable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8900 | 0.8421 | 0.9600 | 0.8972 | 82 | 18 | 4 | 96 |
| 22 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8450 | 0.8053 | 0.9100 | 0.8545 | 78 | 22 | 9 | 91 |
| 33 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8650 | 0.8687 | 0.8600 | 0.8643 | 87 | 13 | 14 | 86 |
| 44 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8700 | 0.8558 | 0.8900 | 0.8725 | 85 | 15 | 11 | 89 |
| 55 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8700 | 0.8854 | 0.8500 | 0.8673 | 89 | 11 | 15 | 85 |
| 66 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8700 | 0.8426 | 0.9100 | 0.8750 | 83 | 17 | 9 | 91 |
| 77 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8400 | 0.8269 | 0.8600 | 0.8431 | 82 | 18 | 14 | 86 |
| 88 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8350 | 0.8073 | 0.8800 | 0.8421 | 79 | 21 | 12 | 88 |
| 99 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8150 | 0.8119 | 0.8200 | 0.8159 | 81 | 19 | 18 | 82 |
| 111 | 800 | 200 | 400 | 400 | 100 | 100 | 0.8500 | 0.8431 | 0.8600 | 0.8515 | 84 | 16 | 14 | 86 |

## Summary Across Splits

| metric | mean | standard_deviation | minimum | maximum |
| --- | --- | --- | --- | --- |
| accuracy | 0.8550 | 0.0220 | 0.8150 | 0.8900 |
| stable_precision | 0.8389 | 0.0266 | 0.8053 | 0.8854 |
| stable_recall | 0.8800 | 0.0394 | 0.8200 | 0.9600 |
| stable_f1 | 0.8583 | 0.0223 | 0.8159 | 0.8972 |

## Main Interpretation

The repeated-split result is the number we should trust more than a single
train/test split. If the mean stable F1 stays close to the single-split result,
then the QML result is stable. If it drops a lot, the earlier result was partly
dependent on the random split.

## Output Files

- `data/processed/best qml repeated split results.csv`
- `data/processed/best qml repeated split predictions.csv`

Prediction rows saved: 2000
