# QML Step 03: Cleaning

Generated on: 2026-06-28

## Cleaning Rule

Rows are removed only when required QML feature values or the target value are
missing.

## Missing Values Before Cleaning

| column | missing_count | missing_percentage |
| --- | --- | --- |
| space_group_number | 0 | 0 |
| band_gap | 889 | 3.56 |
| formation_energy_per_atom | 889 | 3.56 |
| number_of_elements | 0 | 0 |
| has_fe | 0 | 0 |
| has_p | 0 | 0 |
| has_mn | 0 | 0 |
| has_c | 0 | 0 |
| has_si | 0 | 0 |
| has_s | 0 | 0 |
| is_stable | 0 | 0 |

## Row Counts

- Rows before cleaning: 24,957
- Rows removed: 889
- Rows after cleaning: 24,068

## Why This Step Matters

QML models need complete numeric input values. Missing values can break the
training code or create unclear results.
