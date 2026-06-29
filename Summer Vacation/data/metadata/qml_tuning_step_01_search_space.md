# QML Tuning Step 01: Search Space

Generated on: 2026-06-28

## Goal

Test multiple QML hyperparameter combinations and find the best combination
inside this search space.

## Data Split

- Train-validation rows used for tuning: 800
- Cross-validation folds: 4
- Untouched test rows: 200
- Random state: 42

## Total Experiments

72

## Feature Count Options

| feature_count | features_used |
| --- | --- |
| 4 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements |
| 6 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p |
| 8 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c |
| 10 | scaled_space_group_number; scaled_band_gap; scaled_formation_energy_per_atom; scaled_number_of_elements; scaled_has_fe; scaled_has_p; scaled_has_mn; scaled_has_c; scaled_has_si; scaled_has_s |

## Angle Scale Options

| angle_scale_name | angle_scale_value |
| --- | --- |
| pi_over_2 | 1.5708 |
| pi | 3.1416 |
| two_pi | 6.2832 |

## SVM C Values

| c_value |
| --- |
| 0.1000 |
| 0.5000 |
| 1 |
| 2 |
| 5 |
| 10 |

## Selection Rule

The best model is selected by highest cross-validation `stable_f1`. If there is
a tie, cross-validation accuracy and stable recall are used next.
