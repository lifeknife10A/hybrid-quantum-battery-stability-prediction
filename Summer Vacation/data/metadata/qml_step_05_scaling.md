# QML Step 05: Scaling

Generated on: 2026-06-28

## Scaling Method

Each selected feature is scaled between 0 and 1 using min-max scaling:

`scaled_value = (value - minimum) / (maximum - minimum)`

## Why Scaling Is Needed

QML circuits usually work better with small normalized feature values. Scaling
also keeps all features on a comparable range.

## Scaling Values

| feature | scaled_feature | minimum | maximum |
| --- | --- | --- | --- |
| space_group_number | scaled_space_group_number | 1 | 230 |
| band_gap | scaled_band_gap | 0 | 7.4719 |
| formation_energy_per_atom | scaled_formation_energy_per_atom | -4.029101 | 4.05724 |
| number_of_elements | scaled_number_of_elements | 2 | 6 |
| has_fe | scaled_has_fe | 0 | 1 |
| has_p | scaled_has_p | 0 | 1 |
| has_mn | scaled_has_mn | 0 | 1 |
| has_c | scaled_has_c | 0 | 1 |
| has_si | scaled_has_si | 0 | 1 |
| has_s | scaled_has_s | 0 | 1 |

## Training Columns

Use the columns that start with `scaled_` for the QML model.
