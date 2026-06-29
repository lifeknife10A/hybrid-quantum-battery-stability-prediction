# Improved QML Step 03: Tuning Results

Generated on: 2026-06-28

## Output

`data/processed/improved qml tuning results.csv`

## Search Space

- PCA component counts: [4, 6, 8]
- Angle scales: pi/2, pi, 2pi
- Kernel types: product, entangled_pi_over_2, entangled_pi
- SVM C values: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
- Total experiments: 162

## Best Cross-Validation Result

| pca_component_count | kernel_name | entanglement_strength | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | entangled_pi | 3.1416 | pi | 3.1416 | 2 | 64 | 800 | 4 | 0.8575 | 0.8543 | 0.8675 | 0.8596 |

## Top 15 Results

| pca_component_count | kernel_name | entanglement_strength | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | entangled_pi | 3.1416 | pi | 3.1416 | 2 | 64 | 800 | 4 | 0.8575 | 0.8543 | 0.8675 | 0.8596 |
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 2 | 256 | 800 | 4 | 0.8575 | 0.8566 | 0.8625 | 0.8585 |
| 6 | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 5 | 64 | 800 | 4 | 0.8550 | 0.8484 | 0.8700 | 0.8578 |
| 6 | entangled_pi | 3.1416 | pi | 3.1416 | 5 | 64 | 800 | 4 | 0.8550 | 0.8486 | 0.8700 | 0.8578 |
| 8 | entangled_pi | 3.1416 | two_pi | 6.2832 | 5 | 256 | 800 | 4 | 0.8562 | 0.8548 | 0.8625 | 0.8574 |
| 8 | product | 0 | pi | 3.1416 | 5 | 256 | 800 | 4 | 0.8562 | 0.8537 | 0.8625 | 0.8573 |
| 8 | product | 0 | pi | 3.1416 | 10 | 256 | 800 | 4 | 0.8562 | 0.8537 | 0.8625 | 0.8573 |
| 8 | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 5 | 256 | 800 | 4 | 0.8562 | 0.8537 | 0.8625 | 0.8573 |
| 8 | entangled_pi | 3.1416 | two_pi | 6.2832 | 10 | 256 | 800 | 4 | 0.8562 | 0.8558 | 0.8600 | 0.8569 |
| 8 | entangled_pi | 3.1416 | two_pi | 6.2832 | 2 | 256 | 800 | 4 | 0.8550 | 0.8511 | 0.8650 | 0.8568 |
| 8 | entangled_pi_over_2 | 1.5708 | two_pi | 6.2832 | 2 | 256 | 800 | 4 | 0.8550 | 0.8525 | 0.8625 | 0.8564 |
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 5 | 256 | 800 | 4 | 0.8550 | 0.8516 | 0.8625 | 0.8562 |
| 8 | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 2 | 256 | 800 | 4 | 0.8525 | 0.8402 | 0.8750 | 0.8562 |
| 6 | entangled_pi | 3.1416 | pi | 3.1416 | 10 | 64 | 800 | 4 | 0.8538 | 0.8510 | 0.8625 | 0.8556 |
| 8 | entangled_pi_over_2 | 1.5708 | two_pi | 6.2832 | 10 | 256 | 800 | 4 | 0.8550 | 0.8554 | 0.8575 | 0.8555 |
