# Improved QML Step 01: Feature Importance

Generated on: 2026-06-28

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
| formation_energy_per_atom | 0.2491 | 1 |
| has_o | 0.1797 | 2 |
| space_group_number | 0.1181 | 3 |
| theoretical | 0.0880 | 4 |
| band_gap | 0.0553 | 5 |
| battery_family_Other lithium material | 0.0458 | 6 |
| crystal_system_Triclinic | 0.0310 | 7 |
| has_mn | 0.0293 | 8 |
| number_of_elements | 0.0215 | 9 |
| has_co | 0.0183 | 10 |
| has_f | 0.0178 | 11 |
| battery_family_LCO-family | 0.0163 | 12 |
| crystal_system_Monoclinic | 0.0144 | 13 |
| battery_family_LMO-family | 0.0128 | 14 |
| crystal_system_Cubic | 0.0115 | 15 |
| is_metal | 0.0109 | 16 |
| has_p | 0.0105 | 17 |
| has_fe | 0.0103 | 18 |
| has_s | 0.0081 | 19 |
| battery_family_Li-S or sulfide-family | 0.0072 | 20 |

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
| has_co |
| has_f |
| battery_family_LCO-family |
| crystal_system_Monoclinic |
| battery_family_LMO-family |
| crystal_system_Cubic |
| is_metal |
