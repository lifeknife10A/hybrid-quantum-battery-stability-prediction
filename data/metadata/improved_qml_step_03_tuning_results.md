# Improved QML Step 03: Tuning Results

Generated on: 2026-07-04

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
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 1 | 256 | 800 | 4 | 0.8575 | 0.8531 | 0.8675 | 0.8594 |

## Top 15 Results

| pca_component_count | kernel_name | entanglement_strength | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 1 | 256 | 800 | 4 | 0.8575 | 0.8531 | 0.8675 | 0.8594 |
| 6 | entangled_pi | 3.1416 | pi | 3.1416 | 5 | 64 | 800 | 4 | 0.8562 | 0.8518 | 0.8675 | 0.8585 |
| 6 | entangled_pi | 3.1416 | pi | 3.1416 | 10 | 64 | 800 | 4 | 0.8562 | 0.8536 | 0.8650 | 0.8580 |
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 0.5000 | 256 | 800 | 4 | 0.8562 | 0.8527 | 0.8650 | 0.8580 |
| 8 | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 0.1000 | 256 | 800 | 4 | 0.8562 | 0.8530 | 0.8650 | 0.8578 |
| 8 | product | 0 | pi | 3.1416 | 0.1000 | 256 | 800 | 4 | 0.8562 | 0.8562 | 0.8600 | 0.8570 |
| 8 | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 2 | 256 | 800 | 4 | 0.8550 | 0.8502 | 0.8650 | 0.8569 |
| 6 | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 10 | 64 | 800 | 4 | 0.8538 | 0.8474 | 0.8675 | 0.8562 |
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 2 | 256 | 800 | 4 | 0.8538 | 0.8482 | 0.8650 | 0.8558 |
| 8 | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 0.5000 | 256 | 800 | 4 | 0.8525 | 0.8420 | 0.8725 | 0.8558 |
| 8 | entangled_pi | 3.1416 | pi | 3.1416 | 0.1000 | 256 | 800 | 4 | 0.8538 | 0.8515 | 0.8600 | 0.8552 |
| 8 | product | 0 | pi | 3.1416 | 0.5000 | 256 | 800 | 4 | 0.8538 | 0.8538 | 0.8575 | 0.8548 |
| 8 | product | 0 | pi | 3.1416 | 1 | 256 | 800 | 4 | 0.8538 | 0.8538 | 0.8575 | 0.8548 |
| 8 | product | 0 | pi | 3.1416 | 2 | 256 | 800 | 4 | 0.8538 | 0.8538 | 0.8575 | 0.8548 |
| 8 | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 0.5000 | 256 | 800 | 4 | 0.8538 | 0.8538 | 0.8575 | 0.8548 |
