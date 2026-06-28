# QML Tuning Results

Generated on: 2026-06-28

## Goal

Iterate QML hyperparameters and angle scales to find the best combination inside
the tested search space.

## Search Space

- Feature counts tested: [4, 6, 8, 10]
- Angle scales tested: pi/2, pi, 2pi
- SVM C values tested: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
- Total experiments: 72

## Best Cross-Validation Combination

| feature_count | feature_names | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 1 | 256 | 800 | 4 | 0.8038 | 0.7732 | 0.8600 | 0.8141 |

## Top 10 Cross-Validation Results

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

## Test Comparison

| model | test_accuracy | test_stable_f1 |
| --- | --- | --- |
| Original QML baseline | 0.8100 | 0.8173 |
| Tuned QML best model | 0.8200 | 0.8269 |
| Same-data XGBoost baseline | 0.8300 | 0.8283 |

## Important Conclusion

This tuning finds the best QML combination inside our tested search space. It is
not a mathematical guarantee of the perfect QML model.
