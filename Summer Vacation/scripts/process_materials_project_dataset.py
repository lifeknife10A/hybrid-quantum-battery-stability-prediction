from datetime import date
from pathlib import Path
import re
import sys


project_folder = Path(__file__).resolve().parents[1]
local_package_folder = project_folder / ".python_packages"

if local_package_folder.exists():
    sys.path.insert(0, str(local_package_folder))

import pandas as pd
import pyarrow.parquet as parquet


raw_dataset_folder = project_folder / "data" / "raw" / "materials_project_hf"
processed_dataset_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

expected_raw_row_count = 210579
expected_raw_files = [
    "0000.parquet",
    "0001.parquet",
    "0002.parquet",
]

source_dataset_url = "https://huggingface.co/datasets/xpanceo-team/materials-project"
materials_project_api_url = "https://docs.materialsproject.org/downloading-data/using-the-api/examples"
oqmd_backup_url = "https://static.oqmd.org/static/docs/restful.html"
jarvis_backup_url = "https://jarvis-tools.readthedocs.io/en/master/databases.html"

core_columns_with_structure = [
    "material_id",
    "formula",
    "space_group_number",
    "crystal_system",
    "formation_energy_per_atom",
    "energy_above_hull",
    "is_stable",
    "band_gap",
    "is_metal",
    "theoretical",
    "deprecated",
    "structure",
]

core_columns_without_structure = [
    column_name
    for column_name in core_columns_with_structure
    if column_name != "structure"
]

missing_value_columns = [
    "energy_above_hull",
    "formation_energy_per_atom",
    "band_gap",
]


def get_elements_from_formula(formula):
    if not isinstance(formula, str):
        return []

    return re.findall(r"[A-Z][a-z]?", formula)


def formula_has_lithium(formula):
    elements = get_elements_from_formula(formula)
    return "Li" in elements


def check_required_columns(available_columns, required_columns, file_name):
    missing_columns = []

    for column_name in required_columns:
        if column_name not in available_columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"{file_name} is missing required columns: {missing_text}")


def get_file_size_text(file_path):
    file_size = file_path.stat().st_size
    return f"{file_size:,} bytes"


def read_and_filter_raw_files():
    raw_row_count = 0
    raw_missing_value_counts = {
        column_name: 0
        for column_name in missing_value_columns
    }
    lithium_dataframes = []
    raw_file_information = []

    for raw_file_name in expected_raw_files:
        raw_file_path = raw_dataset_folder / raw_file_name

        if not raw_file_path.exists():
            raise FileNotFoundError(f"Missing raw parquet file: {raw_file_path}")

        parquet_file = parquet.ParquetFile(raw_file_path)
        raw_file_row_count = parquet_file.metadata.num_rows
        raw_file_columns = parquet_file.schema_arrow.names

        check_required_columns(
            raw_file_columns,
            core_columns_with_structure,
            raw_file_name,
        )

        raw_row_count = raw_row_count + raw_file_row_count

        raw_table = parquet_file.read(columns=core_columns_with_structure)
        raw_dataframe = raw_table.to_pandas()

        for column_name in missing_value_columns:
            missing_count = int(raw_dataframe[column_name].isna().sum())
            raw_missing_value_counts[column_name] = (
                raw_missing_value_counts[column_name] + missing_count
            )

        lithium_mask = raw_dataframe["formula"].apply(formula_has_lithium)
        lithium_dataframe = raw_dataframe.loc[lithium_mask].copy()
        lithium_dataframes.append(lithium_dataframe)

        raw_file_information.append(
            {
                "file_name": raw_file_name,
                "row_count": raw_file_row_count,
                "file_size": get_file_size_text(raw_file_path),
                "lithium_row_count": len(lithium_dataframe),
            }
        )

    if raw_row_count != expected_raw_row_count:
        raise ValueError(
            f"Expected {expected_raw_row_count} raw rows, but found {raw_row_count}."
        )

    lithium_dataset = pd.concat(lithium_dataframes, ignore_index=True)

    if len(lithium_dataset) == 0:
        raise ValueError("Lithium filter returned zero rows.")

    check_required_columns(
        lithium_dataset.columns,
        core_columns_with_structure,
        "processed lithium dataset",
    )

    return lithium_dataset, raw_row_count, raw_missing_value_counts, raw_file_information


def save_processed_files(lithium_dataset):
    processed_dataset_folder.mkdir(parents=True, exist_ok=True)
    metadata_folder.mkdir(parents=True, exist_ok=True)

    lithium_csv_path = processed_dataset_folder / "materials_project_lithium.csv"
    lithium_parquet_path = processed_dataset_folder / "materials_project_lithium.parquet"

    lithium_dataset.to_parquet(lithium_parquet_path, index=False)
    lithium_dataset[core_columns_without_structure].to_csv(lithium_csv_path, index=False)

    return lithium_csv_path, lithium_parquet_path


def write_dataset_summary(
    lithium_dataset,
    raw_row_count,
    raw_missing_value_counts,
    raw_file_information,
    lithium_csv_path,
    lithium_parquet_path,
):
    lithium_missing_value_counts = {}

    for column_name in missing_value_columns:
        lithium_missing_value_counts[column_name] = int(
            lithium_dataset[column_name].isna().sum()
        )

    stable_count = int(lithium_dataset["is_stable"].sum())
    unstable_count = len(lithium_dataset) - stable_count

    raw_file_lines = []
    for raw_file in raw_file_information:
        raw_file_lines.append(
            (
                f"- `{raw_file['file_name']}`: {raw_file['row_count']:,} rows, "
                f"{raw_file['file_size']}, "
                f"{raw_file['lithium_row_count']:,} lithium rows"
            )
        )

    core_column_lines = []
    for column_name in core_columns_without_structure:
        core_column_lines.append(f"- `{column_name}`")
    core_column_lines.append("- `structure` in parquet only")

    raw_missing_lines = []
    for column_name in missing_value_columns:
        raw_missing_lines.append(
            f"- `{column_name}`: {raw_missing_value_counts[column_name]:,}"
        )

    lithium_missing_lines = []
    for column_name in missing_value_columns:
        lithium_missing_lines.append(
            f"- `{column_name}`: {lithium_missing_value_counts[column_name]:,}"
        )

    summary_text = f"""# Materials Project Hugging Face Dataset Summary

Generated on: {date.today().isoformat()}

## Source

- Main dataset: [{source_dataset_url}]({source_dataset_url})
- Materials Project API reference: [{materials_project_api_url}]({materials_project_api_url})
- Backup option 1, OQMD: [{oqmd_backup_url}]({oqmd_backup_url})
- Backup option 2, JARVIS: [{jarvis_backup_url}]({jarvis_backup_url})

## Raw Mirror

Raw files are stored in:

`data/raw/materials_project_hf/`

{chr(10).join(raw_file_lines)}

Total raw rows verified: {raw_row_count:,}

## Processed Files

- CSV without large structure JSON: `{lithium_csv_path.relative_to(project_folder)}`
- Parquet with structure JSON preserved: `{lithium_parquet_path.relative_to(project_folder)}`

Lithium rows: {len(lithium_dataset):,}
Stable lithium rows: {stable_count:,}
Unstable lithium rows: {unstable_count:,}

## Lithium Filtering Rule

The lithium dataset was filtered by parsing the `formula` column into chemical
element symbols using this pattern:

`[A-Z][a-z]?`

A row is included only when the parsed element list contains the exact element
symbol `Li`. This avoids loose text matching.

## Modeling Columns

{chr(10).join(core_column_lines)}

## Missing Values In Full Raw Core Columns

{chr(10).join(raw_missing_lines)}

## Missing Values In Lithium Dataset

{chr(10).join(lithium_missing_lines)}

## Limitations

- This is a public Hugging Face snapshot, not a fresh live Materials Project API export.
- The snapshot does not include explicit `density` or `volume` columns.
- Density and volume may be derived later from the `structure` JSON if needed.
- OQMD, AFLOW, and JARVIS remain backup options if this dataset is weak for a
  specific lithium battery family.
"""

    summary_path = metadata_folder / "dataset_summary.md"
    summary_path.write_text(summary_text, encoding="utf-8")

    return summary_path


def main():
    lithium_dataset, raw_row_count, raw_missing_value_counts, raw_file_information = (
        read_and_filter_raw_files()
    )

    lithium_csv_path, lithium_parquet_path = save_processed_files(lithium_dataset)

    summary_path = write_dataset_summary(
        lithium_dataset,
        raw_row_count,
        raw_missing_value_counts,
        raw_file_information,
        lithium_csv_path,
        lithium_parquet_path,
    )

    print(f"Raw rows verified: {raw_row_count:,}")
    print(f"Lithium rows saved: {len(lithium_dataset):,}")
    print(f"CSV saved: {lithium_csv_path}")
    print(f"Parquet saved: {lithium_parquet_path}")
    print(f"Summary saved: {summary_path}")


if __name__ == "__main__":
    main()
