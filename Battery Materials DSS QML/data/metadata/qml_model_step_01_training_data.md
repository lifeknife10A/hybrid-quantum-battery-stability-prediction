# QML Model Step 01: Training Data

Generated on: 2026-06-28

## Input File

`data/processed/qml_ready_lithium_india.csv`

## Dataset Size

- Total rows: 1,000
- Training rows: 800
- Test rows: 200
- Test size: 0.2
- Random state: 42

## Target Balance

| target_is_stable | count | percentage |
| --- | --- | --- |
| 0 | 500 | 50 |
| 1 | 500 | 50 |

## Training Features

| training_feature |
| --- |
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

## Method

The model uses only the `scaled_` columns as training features and
`target_is_stable` as the target.
