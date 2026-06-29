# QML-Ready Dataset Summary

Generated on: 2026-06-28

## Goal

Create a smaller, clean, balanced, and scaled dataset for the next QML model.

## Input

`data/processed/lithium india scored.csv`

## Output

`data/processed/qml_ready_lithium_india.csv`

## Final Dataset Size

- Clean rows before balancing: 24,068
- Rows per class used: 500
- Final QML-ready rows: 1,000
- Final columns: 27

## Final Class Balance

| target_is_stable | count | percentage |
| --- | --- | --- |
| 0 | 500 | 50 |
| 1 | 500 | 50 |

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

## Important Methodology Note

The QML dataset is prepared from the full lithium dataset, not only from the
India shortlist. This follows the project decision:

1. Train on lithium materials first.
2. Predict stability.
3. Apply India feasibility and safety filtering after prediction.

## Step Markdown Files

| step | file | purpose |
| --- | --- | --- |
| 01 | data/metadata/qml_step_01_input_data.md | Explains the input dataset. |
| 02 | data/metadata/qml_step_02_feature_selection.md | Explains chosen features and target. |
| 03 | data/metadata/qml_step_03_cleaning.md | Explains missing-value cleaning. |
| 04 | data/metadata/qml_step_04_balancing.md | Explains class balancing. |
| 05 | data/metadata/qml_step_05_scaling.md | Explains feature scaling. |
| 06 | data/metadata/qml_step_06_output_files.md | Explains the final output file. |

## Next Step

Train a simple QML classifier using the `scaled_` feature columns and compare it
against the XGBoost classifier baseline.
