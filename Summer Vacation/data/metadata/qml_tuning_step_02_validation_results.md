# QML Tuning Step 02: Cross-Validation Results

Generated on: 2026-06-28

## Tuning Output

`data/processed/qml tuning results.csv`

## Number Of Experiments

72

## Best Cross-Validation Combination

| feature_count | feature_names | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 1 | 256 | 800 | 4 | 0.8038 | 0.7732 | 0.8600 | 0.8141 |

## Top 15 Cross-Validation Results

| feature_count | feature_names | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 1 | 256 | 800 | 4 | 0.8038 | 0.7732 | 0.8600 | 0.8141 |
| 10 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c; scaled_has_si; scaled_has_s | pi_over_2 | 1.5708 | 10 | 1024 | 800 | 4 | 0.8050 | 0.7773 | 0.8550 | 0.8140 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 10 | 256 | 800 | 4 | 0.8050 | 0.7796 | 0.8500 | 0.8131 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 2 | 256 | 800 | 4 | 0.8025 | 0.7751 | 0.8525 | 0.8119 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 5 | 256 | 800 | 4 | 0.8025 | 0.7762 | 0.8500 | 0.8114 |
| 10 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c; scaled_has_si; scaled_has_s | pi_over_2 | 1.5708 | 2 | 1024 | 800 | 4 | 0.8012 | 0.7747 | 0.8500 | 0.8105 |
| 10 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c; scaled_has_si; scaled_has_s | pi_over_2 | 1.5708 | 5 | 1024 | 800 | 4 | 0.8000 | 0.7754 | 0.8450 | 0.8084 |
| 10 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c; scaled_has_si; scaled_has_s | pi_over_2 | 1.5708 | 1 | 1024 | 800 | 4 | 0.7975 | 0.7668 | 0.8550 | 0.8084 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p | pi_over_2 | 1.5708 | 5 | 64 | 800 | 4 | 0.7988 | 0.7732 | 0.8450 | 0.8074 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p | pi | 3.1416 | 10 | 64 | 800 | 4 | 0.8025 | 0.7869 | 0.8300 | 0.8073 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi | 3.1416 | 2 | 256 | 800 | 4 | 0.7975 | 0.7757 | 0.8375 | 0.8049 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi | 3.1416 | 0.5000 | 256 | 800 | 4 | 0.7962 | 0.7735 | 0.8375 | 0.8041 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p | pi | 3.1416 | 1 | 64 | 800 | 4 | 0.7950 | 0.7706 | 0.8400 | 0.8036 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p | pi | 3.1416 | 5 | 64 | 800 | 4 | 0.7962 | 0.7764 | 0.8325 | 0.8030 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p | pi_over_2 | 1.5708 | 10 | 64 | 800 | 4 | 0.7938 | 0.7674 | 0.8425 | 0.8030 |

## Important Note

These are cross-validation results from the train-validation split only. The
test set is not used to choose the best combination.
