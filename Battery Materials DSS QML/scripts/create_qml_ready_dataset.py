from datetime import date
from pathlib import Path

import pandas as pd


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "lithium india scored.csv"
output_csv_path = processed_folder / "qml_ready_lithium_india.csv"

step_01_markdown_path = metadata_folder / "qml_step_01_input_data.md"
step_02_markdown_path = metadata_folder / "qml_step_02_feature_selection.md"
step_03_markdown_path = metadata_folder / "qml_step_03_cleaning.md"
step_04_markdown_path = metadata_folder / "qml_step_04_balancing.md"
step_05_markdown_path = metadata_folder / "qml_step_05_scaling.md"
step_06_markdown_path = metadata_folder / "qml_step_06_output_files.md"
summary_markdown_path = metadata_folder / "qml_ready_dataset_summary.md"

random_state = 42
maximum_rows_per_class = 500

metadata_columns = [
    "material_id",
    "formula",
    "battery_family",
    "india_feasibility_score",
    "india_decision_label",
]

feature_columns = [
    "space_group_number",
    "band_gap",
    "formation_energy_per_atom",
    "number_of_elements",
    "has_fe",
    "has_p",
    "has_mn",
    "has_c",
    "has_si",
    "has_s",
]

target_column = "is_stable"

boolean_feature_columns = [
    "has_fe",
    "has_p",
    "has_mn",
    "has_c",
    "has_si",
    "has_s",
]


def dataframe_to_markdown(dataframe):
    if dataframe.empty:
        return "_No rows found._"

    headers = list(dataframe.columns)
    rows = []

    for _, dataframe_row in dataframe.iterrows():
        row_values = []
        for column_name in headers:
            value = dataframe_row[column_name]
            if pd.isna(value):
                value_text = ""
            elif isinstance(value, float) and value.is_integer():
                value_text = str(int(value))
            else:
                value_text = str(value)
            value_text = value_text.replace("|", "/")
            row_values.append(value_text)
        rows.append(row_values)

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = []

    for row_values in rows:
        row_lines.append("| " + " | ".join(row_values) + " |")

    return "\n".join([header_line, separator_line] + row_lines)


def format_count(value):
    return f"{int(value):,}"


def convert_boolean_to_integer(dataframe, column_name):
    if dataframe[column_name].dtype == bool:
        dataframe[column_name] = dataframe[column_name].astype(int)
        return

    converted_values = (
        dataframe[column_name]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(
            {
                "true": 1,
                "false": 0,
                "1": 1,
                "0": 0,
            }
        )
    )

    dataframe[column_name] = converted_values.astype(int)


def get_count_table(dataframe, column_name):
    count_dataframe = dataframe[column_name].value_counts().reset_index()
    count_dataframe.columns = [column_name, "count"]
    count_dataframe["percentage"] = (
        count_dataframe["count"] / len(dataframe) * 100
    ).round(2)
    return count_dataframe


def get_missing_value_table(dataframe, columns_to_check):
    rows = []

    for column_name in columns_to_check:
        missing_count = int(dataframe[column_name].isna().sum())
        missing_percentage = round(missing_count / len(dataframe) * 100, 2)
        rows.append(
            {
                "column": column_name,
                "missing_count": missing_count,
                "missing_percentage": missing_percentage,
            }
        )

    return pd.DataFrame(rows)


def get_feature_purpose_table():
    rows = [
        {
            "feature": "space_group_number",
            "reason": "Represents crystal symmetry.",
        },
        {
            "feature": "band_gap",
            "reason": "Represents electronic behavior.",
        },
        {
            "feature": "formation_energy_per_atom",
            "reason": "Represents formation stability.",
        },
        {
            "feature": "number_of_elements",
            "reason": "Represents material complexity.",
        },
        {
            "feature": "has_fe",
            "reason": "Important for LFP and LMFP battery families.",
        },
        {
            "feature": "has_p",
            "reason": "Important for phosphate-based battery families.",
        },
        {
            "feature": "has_mn",
            "reason": "Important for manganese battery families.",
        },
        {
            "feature": "has_c",
            "reason": "Important for carbon-family materials.",
        },
        {
            "feature": "has_si",
            "reason": "Important for silicon-family materials.",
        },
        {
            "feature": "has_s",
            "reason": "Important for sulfur and sulfide-family materials.",
        },
    ]

    return pd.DataFrame(rows)


def check_required_columns(dataframe):
    required_columns = metadata_columns + feature_columns + [target_column]
    missing_columns = []

    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")


def prepare_clean_dataset(dataframe):
    selected_columns = metadata_columns + feature_columns + [target_column]
    selected_dataframe = dataframe[selected_columns].copy()
    rows_before_cleaning = len(selected_dataframe)
    missing_table = get_missing_value_table(
        selected_dataframe,
        feature_columns + [target_column],
    )

    clean_dataframe = selected_dataframe.dropna(
        subset=feature_columns + [target_column]
    ).copy()

    for column_name in boolean_feature_columns:
        convert_boolean_to_integer(clean_dataframe, column_name)

    convert_boolean_to_integer(clean_dataframe, target_column)
    clean_dataframe["target_is_stable"] = clean_dataframe[target_column]

    rows_after_cleaning = len(clean_dataframe)
    removed_rows = rows_before_cleaning - rows_after_cleaning

    return clean_dataframe, missing_table, removed_rows


def balance_dataset(clean_dataframe):
    stable_dataframe = clean_dataframe[clean_dataframe["target_is_stable"] == 1]
    unstable_dataframe = clean_dataframe[clean_dataframe["target_is_stable"] == 0]

    available_rows_per_class = min(len(stable_dataframe), len(unstable_dataframe))
    rows_per_class = min(maximum_rows_per_class, available_rows_per_class)

    balanced_stable_dataframe = stable_dataframe.sample(
        n=rows_per_class,
        random_state=random_state,
    )
    balanced_unstable_dataframe = unstable_dataframe.sample(
        n=rows_per_class,
        random_state=random_state,
    )

    balanced_dataframe = pd.concat(
        [balanced_stable_dataframe, balanced_unstable_dataframe],
        ignore_index=True,
    )

    balanced_dataframe = balanced_dataframe.sample(
        frac=1,
        random_state=random_state,
    ).reset_index(drop=True)

    return balanced_dataframe, rows_per_class


def scale_features(balanced_dataframe):
    scaling_rows = []
    scaled_feature_columns = []

    for column_name in feature_columns:
        scaled_column_name = f"scaled_{column_name}"
        minimum_value = balanced_dataframe[column_name].min()
        maximum_value = balanced_dataframe[column_name].max()

        if maximum_value == minimum_value:
            balanced_dataframe[scaled_column_name] = 0.0
        else:
            balanced_dataframe[scaled_column_name] = (
                balanced_dataframe[column_name] - minimum_value
            ) / (maximum_value - minimum_value)

        balanced_dataframe[scaled_column_name] = balanced_dataframe[
            scaled_column_name
        ].round(6)

        scaled_feature_columns.append(scaled_column_name)
        scaling_rows.append(
            {
                "feature": column_name,
                "scaled_feature": scaled_column_name,
                "minimum": round(float(minimum_value), 6),
                "maximum": round(float(maximum_value), 6),
            }
        )

    scaling_table = pd.DataFrame(scaling_rows)
    return balanced_dataframe, scaled_feature_columns, scaling_table


def write_step_01_report(dataframe):
    stable_rows = int(dataframe[target_column].sum())
    unstable_rows = len(dataframe) - stable_rows
    class_count_table = get_count_table(dataframe, target_column)

    report_text = f"""# QML Step 01: Input Data

Generated on: {date.today().isoformat()}

## Input File

`data/processed/lithium india scored.csv`

## Purpose

This step starts from the India-scored lithium dataset. We do not start from
the final shortlist because the QML model should learn from the wider lithium
dataset first.

## Input Size

- Rows: {format_count(len(dataframe))}
- Columns: {format_count(len(dataframe.columns))}
- Stable rows: {format_count(stable_rows)}
- Unstable rows: {format_count(unstable_rows)}

## Target Distribution

{dataframe_to_markdown(class_count_table)}

## Rule

Use the full lithium dataset for model preparation. India feasibility remains
available for later ranking and interpretation.
"""

    step_01_markdown_path.write_text(report_text)


def write_step_02_report():
    feature_purpose_table = get_feature_purpose_table()

    feature_lines = []
    for column_name in feature_columns:
        feature_lines.append(f"- `{column_name}`")

    report_text = f"""# QML Step 02: Feature Selection

Generated on: {date.today().isoformat()}

## Target

`is_stable`

The target is converted into:

- `1` for stable material
- `0` for unstable material

## Selected Features

{chr(10).join(feature_lines)}

## Feature Meaning

{dataframe_to_markdown(feature_purpose_table)}

## Columns Kept For Reporting

- `material_id`
- `formula`
- `battery_family`
- `india_feasibility_score`
- `india_decision_label`

## Important Decision

`india_feasibility_score` is not used as a QML training feature in this dataset.
It is kept for final comparison and ranking after prediction.
"""

    step_02_markdown_path.write_text(report_text)


def write_step_03_report(input_dataframe, clean_dataframe, missing_table, removed_rows):
    report_text = f"""# QML Step 03: Cleaning

Generated on: {date.today().isoformat()}

## Cleaning Rule

Rows are removed only when required QML feature values or the target value are
missing.

## Missing Values Before Cleaning

{dataframe_to_markdown(missing_table)}

## Row Counts

- Rows before cleaning: {format_count(len(input_dataframe))}
- Rows removed: {format_count(removed_rows)}
- Rows after cleaning: {format_count(len(clean_dataframe))}

## Why This Step Matters

QML models need complete numeric input values. Missing values can break the
training code or create unclear results.
"""

    step_03_markdown_path.write_text(report_text)


def write_step_04_report(clean_dataframe, balanced_dataframe, rows_per_class):
    clean_class_table = get_count_table(clean_dataframe, "target_is_stable")
    balanced_class_table = get_count_table(balanced_dataframe, "target_is_stable")

    report_text = f"""# QML Step 04: Balancing

Generated on: {date.today().isoformat()}

## Reason

The full dataset has many more unstable materials than stable materials. If we
train directly on that imbalance, the model may learn to predict unstable too
often.

## Clean Dataset Class Counts

{dataframe_to_markdown(clean_class_table)}

## Balancing Rule

- Maximum rows per class: {format_count(maximum_rows_per_class)}
- Actual rows per class used: {format_count(rows_per_class)}
- Random state: {random_state}

## Balanced Dataset Class Counts

{dataframe_to_markdown(balanced_class_table)}

## Output Of This Step

- Balanced rows: {format_count(len(balanced_dataframe))}
- Stable rows: {format_count(rows_per_class)}
- Unstable rows: {format_count(rows_per_class)}
"""

    step_04_markdown_path.write_text(report_text)


def write_step_05_report(scaling_table):
    report_text = f"""# QML Step 05: Scaling

Generated on: {date.today().isoformat()}

## Scaling Method

Each selected feature is scaled between 0 and 1 using min-max scaling:

`scaled_value = (value - minimum) / (maximum - minimum)`

## Why Scaling Is Needed

QML circuits usually work better with small normalized feature values. Scaling
also keeps all features on a comparable range.

## Scaling Values

{dataframe_to_markdown(scaling_table)}

## Training Columns

Use the columns that start with `scaled_` for the QML model.
"""

    step_05_markdown_path.write_text(report_text)


def write_step_06_report(output_dataframe, scaled_feature_columns):
    output_columns = pd.DataFrame(
        {
            "column": list(output_dataframe.columns),
        }
    )

    scaled_feature_lines = []
    for column_name in scaled_feature_columns:
        scaled_feature_lines.append(f"- `{column_name}`")

    report_text = f"""# QML Step 06: Output Files

Generated on: {date.today().isoformat()}

## Output Dataset

`data/processed/qml_ready_lithium_india.csv`

## Output Size

- Rows: {format_count(len(output_dataframe))}
- Columns: {format_count(len(output_dataframe.columns))}

## QML Training Features

{chr(10).join(scaled_feature_lines)}

## Target

`target_is_stable`

## All Output Columns

{dataframe_to_markdown(output_columns)}

## Next Use

This file can now be used to train a small QML classifier and compare it with
the XGBoost baseline.
"""

    step_06_markdown_path.write_text(report_text)


def write_summary_report(
    clean_dataframe,
    balanced_dataframe,
    scaled_feature_columns,
    rows_per_class,
):
    class_count_table = get_count_table(balanced_dataframe, "target_is_stable")

    scaled_feature_lines = []
    for column_name in scaled_feature_columns:
        scaled_feature_lines.append(f"- `{column_name}`")

    step_file_table = pd.DataFrame(
        [
            {
                "step": "01",
                "file": "data/metadata/qml_step_01_input_data.md",
                "purpose": "Explains the input dataset.",
            },
            {
                "step": "02",
                "file": "data/metadata/qml_step_02_feature_selection.md",
                "purpose": "Explains chosen features and target.",
            },
            {
                "step": "03",
                "file": "data/metadata/qml_step_03_cleaning.md",
                "purpose": "Explains missing-value cleaning.",
            },
            {
                "step": "04",
                "file": "data/metadata/qml_step_04_balancing.md",
                "purpose": "Explains class balancing.",
            },
            {
                "step": "05",
                "file": "data/metadata/qml_step_05_scaling.md",
                "purpose": "Explains feature scaling.",
            },
            {
                "step": "06",
                "file": "data/metadata/qml_step_06_output_files.md",
                "purpose": "Explains the final output file.",
            },
        ]
    )

    report_text = f"""# QML-Ready Dataset Summary

Generated on: {date.today().isoformat()}

## Goal

Create a smaller, clean, balanced, and scaled dataset for the next QML model.

## Input

`data/processed/lithium india scored.csv`

## Output

`data/processed/qml_ready_lithium_india.csv`

## Final Dataset Size

- Clean rows before balancing: {format_count(len(clean_dataframe))}
- Rows per class used: {format_count(rows_per_class)}
- Final QML-ready rows: {format_count(len(balanced_dataframe))}
- Final columns: {format_count(len(balanced_dataframe.columns))}

## Final Class Balance

{dataframe_to_markdown(class_count_table)}

## QML Training Features

{chr(10).join(scaled_feature_lines)}

## Target

`target_is_stable`

## Important Methodology Note

The QML dataset is prepared from the full lithium dataset, not only from the
India shortlist. This follows the project decision:

1. Train on lithium materials first.
2. Predict stability.
3. Apply India feasibility and safety filtering after prediction.

## Step Markdown Files

{dataframe_to_markdown(step_file_table)}

## Next Step

Train a simple QML classifier using the `scaled_` feature columns and compare it
against the XGBoost classifier baseline.
"""

    summary_markdown_path.write_text(report_text)


def main():
    metadata_folder.mkdir(parents=True, exist_ok=True)
    processed_folder.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(input_csv_path)
    check_required_columns(dataframe)

    clean_dataframe, missing_table, removed_rows = prepare_clean_dataset(dataframe)
    balanced_dataframe, rows_per_class = balance_dataset(clean_dataframe)
    output_dataframe, scaled_feature_columns, scaling_table = scale_features(
        balanced_dataframe
    )

    output_column_order = (
        metadata_columns
        + [target_column, "target_is_stable"]
        + feature_columns
        + scaled_feature_columns
    )
    output_dataframe = output_dataframe[output_column_order]
    output_dataframe.to_csv(output_csv_path, index=False)

    write_step_01_report(dataframe)
    write_step_02_report()
    write_step_03_report(dataframe, clean_dataframe, missing_table, removed_rows)
    write_step_04_report(clean_dataframe, output_dataframe, rows_per_class)
    write_step_05_report(scaling_table)
    write_step_06_report(output_dataframe, scaled_feature_columns)
    write_summary_report(
        clean_dataframe,
        output_dataframe,
        scaled_feature_columns,
        rows_per_class,
    )

    print(f"Created: {output_csv_path}")
    print(f"Rows: {len(output_dataframe):,}")
    print(f"Columns: {len(output_dataframe.columns):,}")
    print(f"Created summary: {summary_markdown_path}")


if __name__ == "__main__":
    main()
