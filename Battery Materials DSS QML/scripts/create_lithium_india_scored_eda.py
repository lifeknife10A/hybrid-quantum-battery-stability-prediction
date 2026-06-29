from datetime import date
from pathlib import Path

import pandas as pd


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "lithium india scored.csv"
output_markdown_path = metadata_folder / "lithium_india_scored_eda.md"

important_numeric_columns = [
    "formation_energy_per_atom",
    "energy_above_hull",
    "band_gap",
    "india_feasibility_score",
]

important_columns_for_missing_values = [
    "formation_energy_per_atom",
    "energy_above_hull",
    "band_gap",
    "is_stable",
    "battery_family",
    "india_feasibility_score",
    "india_decision_label",
]


def format_number(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:,.3f}"


def format_count(value):
    return f"{int(value):,}"


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


def get_count_table(dataframe, column_name):
    count_dataframe = dataframe[column_name].value_counts().reset_index()
    count_dataframe.columns = [column_name, "count"]
    count_dataframe["percentage"] = (
        count_dataframe["count"] / len(dataframe) * 100
    ).round(2)
    return count_dataframe


def get_missing_value_table(dataframe):
    rows = []

    for column_name in important_columns_for_missing_values:
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


def get_numeric_summary(dataframe):
    rows = []

    for column_name in important_numeric_columns:
        column_data = dataframe[column_name].dropna()

        rows.append(
            {
                "column": column_name,
                "non_missing": len(column_data),
                "mean": round(column_data.mean(), 4),
                "median": round(column_data.median(), 4),
                "minimum": round(column_data.min(), 4),
                "maximum": round(column_data.max(), 4),
            }
        )

    return pd.DataFrame(rows)


def get_family_summary(dataframe):
    grouped_data = dataframe.groupby("battery_family", dropna=False)

    summary_dataframe = grouped_data.agg(
        rows=("material_id", "count"),
        stable_rows=("is_stable", "sum"),
        average_india_score=("india_feasibility_score", "mean"),
        average_energy_above_hull=("energy_above_hull", "mean"),
        median_energy_above_hull=("energy_above_hull", "median"),
        average_band_gap=("band_gap", "mean"),
    ).reset_index()

    summary_dataframe["stable_percentage"] = (
        summary_dataframe["stable_rows"] / summary_dataframe["rows"] * 100
    ).round(2)

    numeric_columns = [
        "average_india_score",
        "average_energy_above_hull",
        "median_energy_above_hull",
        "average_band_gap",
    ]

    for column_name in numeric_columns:
        summary_dataframe[column_name] = summary_dataframe[column_name].round(4)

    return summary_dataframe.sort_values(
        by=["average_india_score", "rows"],
        ascending=[False, False],
    )


def get_label_family_table(dataframe):
    cross_table = pd.crosstab(
        dataframe["battery_family"],
        dataframe["india_decision_label"],
    )
    cross_table = cross_table.reset_index()
    return cross_table


def get_top_materials(dataframe, label_name, number_of_rows):
    label_dataframe = dataframe[dataframe["india_decision_label"] == label_name].copy()

    label_dataframe = label_dataframe.sort_values(
        by=[
            "india_feasibility_score",
            "is_stable",
            "energy_above_hull",
            "band_gap",
        ],
        ascending=[False, False, True, False],
    )

    columns_to_show = [
        "material_id",
        "formula",
        "battery_family",
        "india_feasibility_score",
        "energy_above_hull",
        "band_gap",
        "is_stable",
    ]

    return label_dataframe[columns_to_show].head(number_of_rows)


def get_modeling_readiness_notes(dataframe):
    rows_with_targets = dataframe.dropna(
        subset=["energy_above_hull", "formation_energy_per_atom", "band_gap"]
    )
    stable_rows = int(dataframe["is_stable"].sum())
    unstable_rows = len(dataframe) - stable_rows

    notes = [
        f"Rows available for full numeric target modeling: {len(rows_with_targets):,}",
        f"Stable rows: {stable_rows:,}",
        f"Unstable rows: {unstable_rows:,}",
        "The dataset is useful for both classification (`is_stable`) and regression (`energy_above_hull`).",
        "India columns should be used after prediction for filtering or re-ranking, not for deleting training rows first.",
    ]

    return notes


def write_report(dataframe):
    total_rows = len(dataframe)
    total_columns = len(dataframe.columns)
    stable_rows = int(dataframe["is_stable"].sum())
    unstable_rows = total_rows - stable_rows

    missing_table = get_missing_value_table(dataframe)
    numeric_summary = get_numeric_summary(dataframe)
    label_counts = get_count_table(dataframe, "india_decision_label")
    family_counts = get_count_table(dataframe, "battery_family")
    family_summary = get_family_summary(dataframe)
    label_family_table = get_label_family_table(dataframe)
    top_recommended = get_top_materials(dataframe, "Recommend", 15)
    top_research = get_top_materials(dataframe, "Research Candidate", 15)
    top_caution = get_top_materials(dataframe, "Caution", 10)
    modeling_notes = get_modeling_readiness_notes(dataframe)

    modeling_note_lines = []
    for note in modeling_notes:
        modeling_note_lines.append(f"- {note}")

    report_text = f"""# Lithium India Scored EDA

Generated on: {date.today().isoformat()}

Input file: `data/processed/lithium india scored.csv`

## Basic Dataset Size

- Total rows: {total_rows:,}
- Total columns: {total_columns:,}
- Stable rows: {stable_rows:,}
- Unstable rows: {unstable_rows:,}

## Missing Values

{dataframe_to_markdown(missing_table)}

## Numeric Column Summary

{dataframe_to_markdown(numeric_summary)}

## India Decision Label Distribution

{dataframe_to_markdown(label_counts)}

## Battery Family Distribution

{dataframe_to_markdown(family_counts)}

## Family-Level Summary

{dataframe_to_markdown(family_summary)}

## Family vs India Decision Label

{dataframe_to_markdown(label_family_table)}

## Top Recommended Materials

These are the strongest India-first candidates by rule score.

{dataframe_to_markdown(top_recommended)}

## Top Research Candidate Materials

These are promising candidates, but they need more checking before being treated
as direct recommendations.

{dataframe_to_markdown(top_research)}

## Sample Caution Materials

These rows are kept for training and comparison, but should not be treated as
India-first recommendations without extra justification.

{dataframe_to_markdown(top_caution)}

## Modeling Readiness Notes

{chr(10).join(modeling_note_lines)}

## Suggested Next Modeling Step

Train a simple classical baseline model on the full lithium dataset first.
Use `is_stable` as the first classification target and `energy_above_hull` as
the first regression target. After prediction, apply `india_feasibility_score`
and `india_decision_label` for final filtering and ranking.
"""

    metadata_folder.mkdir(parents=True, exist_ok=True)
    output_markdown_path.write_text(report_text, encoding="utf-8")


def main():
    if not input_csv_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_csv_path}")

    dataframe = pd.read_csv(input_csv_path)
    write_report(dataframe)

    print(f"Rows analyzed: {len(dataframe):,}")
    print(f"EDA report: {output_markdown_path}")


if __name__ == "__main__":
    main()
