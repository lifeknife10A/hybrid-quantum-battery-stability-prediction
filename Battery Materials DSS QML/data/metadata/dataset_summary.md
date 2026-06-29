# Materials Project Hugging Face Dataset Summary

Generated on: 2026-06-14

## Source

- Main dataset: [https://huggingface.co/datasets/xpanceo-team/materials-project](https://huggingface.co/datasets/xpanceo-team/materials-project)
- Materials Project API reference: [https://docs.materialsproject.org/downloading-data/using-the-api/examples](https://docs.materialsproject.org/downloading-data/using-the-api/examples)
- Backup option 1, OQMD: [https://static.oqmd.org/static/docs/restful.html](https://static.oqmd.org/static/docs/restful.html)
- Backup option 2, JARVIS: [https://jarvis-tools.readthedocs.io/en/master/databases.html](https://jarvis-tools.readthedocs.io/en/master/databases.html)

## Raw Mirror

Raw files are stored in:

`data/raw/materials_project_hf/`

- `0000.parquet`: 70,193 rows, 165,275,744 bytes, 10,457 lithium rows
- `0001.parquet`: 70,193 rows, 142,378,362 bytes, 11,120 lithium rows
- `0002.parquet`: 70,193 rows, 166,219,608 bytes, 3,380 lithium rows

Total raw rows verified: 210,579

## Processed Files

- CSV without large structure JSON: `data/processed/materials_project_lithium.csv`
- Parquet with structure JSON preserved: `data/processed/materials_project_lithium.parquet`

Lithium rows: 24,957
Stable lithium rows: 4,052
Unstable lithium rows: 20,905

## Lithium Filtering Rule

The lithium dataset was filtered by parsing the `formula` column into chemical
element symbols using this pattern:

`[A-Z][a-z]?`

A row is included only when the parsed element list contains the exact element
symbol `Li`. This avoids loose text matching.

## Modeling Columns

- `material_id`
- `formula`
- `space_group_number`
- `crystal_system`
- `formation_energy_per_atom`
- `energy_above_hull`
- `is_stable`
- `band_gap`
- `is_metal`
- `theoretical`
- `deprecated`
- `structure` in parquet only

## Missing Values In Full Raw Core Columns

- `energy_above_hull`: 10,092
- `formation_energy_per_atom`: 10,092
- `band_gap`: 10,092

## Missing Values In Lithium Dataset

- `energy_above_hull`: 889
- `formation_energy_per_atom`: 889
- `band_gap`: 889

## Limitations

- This is a public Hugging Face snapshot, not a fresh live Materials Project API export.
- The snapshot does not include explicit `density` or `volume` columns.
- Density and volume may be derived later from the `structure` JSON if needed.
- OQMD, AFLOW, and JARVIS remain backup options if this dataset is weak for a
  specific lithium battery family.
