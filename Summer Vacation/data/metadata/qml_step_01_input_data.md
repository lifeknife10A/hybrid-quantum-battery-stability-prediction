# QML Step 01: Input Data

Generated on: 2026-06-28

## Input File

`data/processed/lithium india scored.csv`

## Purpose

This step starts from the India-scored lithium dataset. We do not start from
the final shortlist because the QML model should learn from the wider lithium
dataset first.

## Input Size

- Rows: 24,957
- Columns: 37
- Stable rows: 4,052
- Unstable rows: 20,905

## Target Distribution

| is_stable | count | percentage |
| --- | --- | --- |
| False | 20905 | 83.76 |
| True | 4052 | 16.24 |

## Rule

Use the full lithium dataset for model preparation. India feasibility remains
available for later ranking and interpretation.
