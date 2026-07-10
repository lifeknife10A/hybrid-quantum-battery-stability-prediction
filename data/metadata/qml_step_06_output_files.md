# QML Step 06: Output Files

Generated on: 2026-06-28

## Output Dataset

`data/processed/qml_ready_lithium_india.csv`

## Output Size

- Rows: 1,000
- Columns: 27

## QML Training Features

- `scaled_space_group_number`
- `scaled_band_gap`
- `scaled_formation_energy_per_atom`
- `scaled_number_of_elements`
- `scaled_has_fe`
- `scaled_has_p`
- `scaled_has_mn`
- `scaled_has_c`
- `scaled_has_si`
- `scaled_has_s`

## Target

`target_is_stable`

## All Output Columns

| column |
| --- |
| material_id |
| formula |
| battery_family |
| india_feasibility_score |
| india_decision_label |
| is_stable |
| target_is_stable |
| space_group_number |
| band_gap |
| formation_energy_per_atom |
| number_of_elements |
| has_fe |
| has_p |
| has_mn |
| has_c |
| has_si |
| has_s |
| scaled_space_group_number |
| scaled_band_gap |
| scaled_formation_energy_per_atom |
| scaled_number_of_elements |
| scaled_has_fe |
| scaled_has_p |
| scaled_has_mn |
| scaled_has_c |
| scaled_has_si |
| scaled_has_s |

## Next Use

This file can now be used to train a small QML classifier and compare it with
the XGBoost baseline.
