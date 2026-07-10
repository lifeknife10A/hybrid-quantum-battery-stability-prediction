# QML Step 02: Feature Selection

Generated on: 2026-06-28

## Target

`is_stable`

The target is converted into:

- `1` for stable material
- `0` for unstable material

## Selected Features

- `space_group_number`
- `band_gap`
- `formation_energy_per_atom`
- `number_of_elements`
- `has_fe`
- `has_p`
- `has_mn`
- `has_c`
- `has_si`
- `has_s`

## Feature Meaning

| feature | reason |
| --- | --- |
| space_group_number | Represents crystal symmetry. |
| band_gap | Represents electronic behavior. |
| formation_energy_per_atom | Represents formation stability. |
| number_of_elements | Represents material complexity. |
| has_fe | Important for LFP and LMFP battery families. |
| has_p | Important for phosphate-based battery families. |
| has_mn | Important for manganese battery families. |
| has_c | Important for carbon-family materials. |
| has_si | Important for silicon-family materials. |
| has_s | Important for sulfur and sulfide-family materials. |

## Columns Kept For Reporting

- `material_id`
- `formula`
- `battery_family`
- `india_feasibility_score`
- `india_decision_label`

## Important Decision

`india_feasibility_score` is not used as a QML training feature in this dataset.
It is kept for final comparison and ranking after prediction.
