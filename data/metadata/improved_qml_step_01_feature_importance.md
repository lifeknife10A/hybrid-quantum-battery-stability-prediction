# Improved QML Step 01: Feature Importance

Generated on: 2026-07-04

## Separate Section

This is a separate improved-QML experiment. It does not replace the original QML
baseline or tuned-QML baseline.

## Feature Rules

- Used safe non-leakage material features.
- Did not use `energy_above_hull` as a training feature.
- Did not use `india_feasibility_score` or `india_decision_label` as training
  features.
- Used Random Forest feature importance on the train-validation split only.

## Rows

- Rows before cleaning: 24,957
- Rows removed for missing numeric values: 889
- Balanced rows per class: 500
- Final balanced rows: 1,000

## Top Feature Importances

| feature | importance | rank |
| --- | --- | --- |
| formation_energy_per_atom | 0.2335 | 1 |
| has_o | 0.1882 | 2 |
| space_group_number | 0.1183 | 3 |
| theoretical | 0.0928 | 4 |
| band_gap | 0.0503 | 5 |
| battery_family_Other lithium material | 0.0449 | 6 |
| crystal_system_Triclinic | 0.0352 | 7 |
| has_mn | 0.0296 | 8 |
| number_of_elements | 0.0224 | 9 |
| battery_family_LCO-family | 0.0217 | 10 |
| has_f | 0.0184 | 11 |
| has_co | 0.0157 | 12 |
| crystal_system_Monoclinic | 0.0129 | 13 |
| crystal_system_Cubic | 0.0126 | 14 |
| has_fe | 0.0117 | 15 |
| has_s | 0.0114 | 16 |
| battery_family_LMO-family | 0.0110 | 17 |
| is_metal | 0.0107 | 18 |
| has_p | 0.0090 | 19 |
| battery_family_Li-S or sulfide-family | 0.0064 | 20 |

## Features Selected For PCA

| selected_feature_for_pca |
| --- |
| formation_energy_per_atom |
| has_o |
| space_group_number |
| theoretical |
| band_gap |
| battery_family_Other lithium material |
| crystal_system_Triclinic |
| has_mn |
| number_of_elements |
| battery_family_LCO-family |
| has_f |
| has_co |
| crystal_system_Monoclinic |
| crystal_system_Cubic |
| has_fe |
| has_s |
