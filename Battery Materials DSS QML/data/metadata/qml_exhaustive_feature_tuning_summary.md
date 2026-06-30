# QML Exhaustive Feature Combination Tuning Summary

Generated on: 2026-06-30

## Goal

This step tests true feature combinations for QML tuning. The earlier tuning
tested ordered top-N features. This step checks every feature combination for
the selected feature counts.

## Search Space

- Feature counts: [4, 6, 8, 10]
- Available scaled features: 10
- Feature combinations tested: 466
- Angle scales: `pi/2`, `pi`, `2pi`
- SVM C values: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
- Total saved configurations: 8,388
- Cross-validation folds: 4
- Train-validation rows: 800
- Untouched test rows: 200

## Best Cross-Validation Result

| feature_count | feature_names | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_c; scaled_has_s | pi | 3.1416 | 10.0000 | 256 | 800 | 4 | 0.8138 | 0.8041 | 0.8300 | 0.8162 |

## Top 20 Results

| feature_count | feature_names | angle_scale | angle_scale_value | c_value | quantum_state_size | train_validation_rows | cross_validation_splits | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_c; scaled_has_s | pi | 3.1416 | 10.0000 | 256 | 800 | 4 | 0.8138 | 0.8041 | 0.8300 | 0.8162 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_c; scaled_has_s | pi | 3.1416 | 10.0000 | 64 | 800 | 4 | 0.8050 | 0.7749 | 0.8600 | 0.8151 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_p; scaled_has_c | pi | 3.1416 | 10.0000 | 64 | 800 | 4 | 0.8088 | 0.7875 | 0.8450 | 0.8150 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_p; scaled_has_s | pi | 3.1416 | 1.0000 | 64 | 800 | 4 | 0.8050 | 0.7755 | 0.8575 | 0.8142 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 1.0000 | 256 | 800 | 4 | 0.8038 | 0.7731 | 0.8600 | 0.8142 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_s | pi_over_2 | 1.5708 | 2.0000 | 256 | 800 | 4 | 0.8038 | 0.7743 | 0.8575 | 0.8138 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 10.0000 | 256 | 800 | 4 | 0.8050 | 0.7796 | 0.8500 | 0.8131 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_s | pi_over_2 | 1.5708 | 1.0000 | 256 | 800 | 4 | 0.8038 | 0.7766 | 0.8525 | 0.8128 |
| 10 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c; scaled_has_si; scaled_has_s | pi_over_2 | 1.5708 | 10.0000 | 1024 | 800 | 4 | 0.8038 | 0.7768 | 0.8525 | 0.8126 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_c; scaled_has_s | pi | 3.1416 | 1.0000 | 64 | 800 | 4 | 0.8025 | 0.7725 | 0.8575 | 0.8126 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_p; scaled_has_c | pi | 3.1416 | 5.0000 | 64 | 800 | 4 | 0.8050 | 0.7807 | 0.8475 | 0.8125 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_c; scaled_has_s | pi_over_2 | 1.5708 | 5.0000 | 256 | 800 | 4 | 0.8038 | 0.7780 | 0.8500 | 0.8121 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_mn; scaled_has_c; scaled_has_s | pi | 3.1416 | 1.0000 | 256 | 800 | 4 | 0.8038 | 0.7800 | 0.8475 | 0.8120 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 2.0000 | 256 | 800 | 4 | 0.8025 | 0.7751 | 0.8525 | 0.8119 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_c; scaled_has_s | pi | 3.1416 | 5.0000 | 64 | 800 | 4 | 0.8012 | 0.7712 | 0.8575 | 0.8118 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_p; scaled_has_s | pi | 3.1416 | 10.0000 | 64 | 800 | 4 | 0.8038 | 0.7791 | 0.8475 | 0.8117 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c | pi_over_2 | 1.5708 | 5.0000 | 256 | 800 | 4 | 0.8025 | 0.7763 | 0.8500 | 0.8114 |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_si | pi_over_2 | 1.5708 | 2.0000 | 256 | 800 | 4 | 0.8012 | 0.7720 | 0.8550 | 0.8114 |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_fe; scaled_has_p; scaled_has_s | pi | 3.1416 | 2.0000 | 64 | 800 | 4 | 0.8025 | 0.7760 | 0.8500 | 0.8112 |
| 4 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_has_p | pi | 3.1416 | 10.0000 | 16 | 800 | 4 | 0.8038 | 0.7800 | 0.8450 | 0.8110 |

## Output Files

- `data/processed/qml exhaustive feature combination results.csv`
- `data/processed/qml exhaustive feature combination top results.csv`
- `data/metadata/qml_exhaustive_feature_tuning_summary.md`

## Simple Explanation

For each feature count, the script tries all possible feature groups. Each
feature group is tested with every angle scale and every SVM C value. The best
row is selected by highest cross-validation stable F1, then accuracy, then
stable recall.
