from datetime import date
from pathlib import Path
import re

import pandas as pd


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_prediction_path = processed_folder / "xgboost predictions with india scores.csv"
output_shortlist_path = processed_folder / "final india battery shortlist.csv"
output_rejection_audit_path = processed_folder / "final shortlist rejected rows audit.csv"
summary_path = metadata_folder / "final_shortlist_summary.md"

allowed_decision_labels = [
    "Recommend",
    "Research Candidate",
]

allowed_battery_families = [
    "LFP-family",
    "LMFP-family",
    "LMO-family",
    "LTO-family",
    "Silicon-family",
    "Carbon-family",
    "Li-S or sulfide-family",
]

blocked_elements = [
    "Ac",
    "Am",
    "As",
    "At",
    "Be",
    "Bk",
    "Cd",
    "Cf",
    "Cm",
    "Es",
    "Fr",
    "Gd",
    "Ho",
    "Hg",
    "Ir",
    "La",
    "Lu",
    "Md",
    "No",
    "Np",
    "Os",
    "Pa",
    "Pb",
    "Pd",
    "Pm",
    "Po",
    "Pr",
    "Pt",
    "Pu",
    "Ra",
    "Re",
    "Rh",
    "Rn",
    "Ru",
    "Sc",
    "Sm",
    "Tc",
    "Tb",
    "Th",
    "Tl",
    "Tm",
    "U",
    "Y",
    "Yb",
]

minimum_stable_probability = 0.65
maximum_predicted_energy_above_hull = 0.10
minimum_india_feasibility_score = 70
benchmark_family_maximum_predicted_energy_above_hull = 0.06
benchmark_family_minimum_india_feasibility_score = 90


def get_elements_from_formula(formula):
    if not isinstance(formula, str):
        return []

    return sorted(set(re.findall(r"[A-Z][a-z]?", formula)))


def get_blocked_elements(elements):
    blocked = []

    for element_symbol in elements:
        if element_symbol in blocked_elements:
            blocked.append(element_symbol)

    return blocked


def is_benchmark_family_exception(row):
    if row["battery_family"] not in ["LFP-family", "LMFP-family"]:
        return False

    if row["india_decision_label"] not in allowed_decision_labels:
        return False

    if row["blocked_elements"]:
        return False

    if (
        row["predicted_energy_above_hull_clipped"]
        > benchmark_family_maximum_predicted_energy_above_hull
    ):
        return False

    if row["india_feasibility_score"] < benchmark_family_minimum_india_feasibility_score:
        return False

    return True


def is_strict_model_shortlist_row(row):
    if row["india_decision_label"] not in allowed_decision_labels:
        return False

    if row["battery_family"] not in allowed_battery_families:
        return False

    if row["blocked_elements"]:
        return False

    if row["predicted_stable_probability"] < minimum_stable_probability:
        return False

    if row["predicted_energy_above_hull_clipped"] > maximum_predicted_energy_above_hull:
        return False

    if row["india_feasibility_score"] < minimum_india_feasibility_score:
        return False

    if bool(row["predicted_is_stable"]) is False:
        return False

    return True


def get_shortlist_rule_type(row):
    if is_benchmark_family_exception(row):
        return "Benchmark family exception"

    if is_strict_model_shortlist_row(row):
        return "Strict model shortlist"

    return "Rejected"


def get_shortlist_rejection_reasons(row):
    if is_benchmark_family_exception(row):
        return "Included in final shortlist"

    if is_strict_model_shortlist_row(row):
        return "Included in final shortlist"

    reasons = []

    if row["india_decision_label"] not in allowed_decision_labels:
        reasons.append("India decision label is not Recommend or Research Candidate")

    if row["battery_family"] not in allowed_battery_families:
        reasons.append("Battery family is not in the final allowed family list")

    if row["blocked_elements"]:
        reasons.append("Contains blocked/problematic element(s): " + row["blocked_elements"])

    if row["predicted_stable_probability"] < minimum_stable_probability:
        reasons.append("Predicted stable probability is below threshold")

    if row["predicted_energy_above_hull_clipped"] > maximum_predicted_energy_above_hull:
        reasons.append("Predicted energy above hull is above threshold")

    if row["india_feasibility_score"] < minimum_india_feasibility_score:
        reasons.append("India feasibility score is below threshold")

    if bool(row["predicted_is_stable"]) is False and row["battery_family"] not in [
        "LFP-family",
        "LMFP-family",
    ]:
        reasons.append("XGBoost classifier predicted unstable")

    if row["battery_family"] in ["LFP-family", "LMFP-family"]:
        if (
            row["predicted_energy_above_hull_clipped"]
            > benchmark_family_maximum_predicted_energy_above_hull
        ):
            reasons.append("Benchmark family predicted hull is above exception threshold")
        if (
            row["india_feasibility_score"]
            < benchmark_family_minimum_india_feasibility_score
        ):
            reasons.append("Benchmark family India score is below exception threshold")

    if not reasons:
        return "Included in final shortlist"

    return "; ".join(reasons)


def get_family_rank(battery_family):
    family_priority = {
        "LFP-family": 1,
        "LMFP-family": 2,
        "LMO-family": 3,
        "Carbon-family": 4,
        "Silicon-family": 5,
        "LTO-family": 6,
        "Li-S or sulfide-family": 7,
    }

    return family_priority.get(battery_family, 99)


def calculate_shortlist_score(row):
    stability_component = row["predicted_stable_probability"] * 45
    india_component = (row["india_feasibility_score"] / 100) * 35

    predicted_energy = row["predicted_energy_above_hull_clipped"]
    if predicted_energy <= 0:
        energy_component = 20
    elif predicted_energy >= maximum_predicted_energy_above_hull:
        energy_component = 0
    else:
        energy_component = (
            (maximum_predicted_energy_above_hull - predicted_energy)
            / maximum_predicted_energy_above_hull
            * 20
        )

    return round(stability_component + india_component + energy_component, 2)


def dataframe_to_markdown(dataframe):
    if dataframe.empty:
        return "_No rows found._"

    headers = list(dataframe.columns)
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for _, row in dataframe.iterrows():
        row_values = []
        for column_name in headers:
            value = row[column_name]
            if pd.isna(value):
                value_text = ""
            else:
                value_text = str(value)
            row_values.append(value_text.replace("|", "/"))
        lines.append("| " + " | ".join(row_values) + " |")

    return "\n".join(lines)


def get_count_table(dataframe, column_name):
    count_dataframe = dataframe[column_name].value_counts().reset_index()
    count_dataframe.columns = [column_name, "count"]
    count_dataframe["percentage"] = (
        count_dataframe["count"] / len(dataframe) * 100
    ).round(2)
    return count_dataframe


def write_summary(prediction_dataframe, shortlist_dataframe, rejected_dataframe):
    family_counts = get_count_table(shortlist_dataframe, "battery_family")
    label_counts = get_count_table(shortlist_dataframe, "india_decision_label")
    rule_type_counts = get_count_table(shortlist_dataframe, "shortlist_rule_type")

    top_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_decision_label",
        "shortlist_rule_type",
        "shortlist_score",
        "predicted_stable_probability",
        "predicted_energy_above_hull_clipped",
        "india_feasibility_score",
    ]

    top_shortlist = shortlist_dataframe[top_columns].head(25)

    rejection_counts = (
        rejected_dataframe["shortlist_rejection_reason"]
        .value_counts()
        .reset_index()
    )
    rejection_counts.columns = ["rejection_reason", "count"]
    rejection_counts = rejection_counts.head(20)

    summary_text = f"""# Final India Battery Shortlist Summary

Generated on: {date.today().isoformat()}

Input file: `data/processed/xgboost predictions with india scores.csv`

Output file: `data/processed/final india battery shortlist.csv`

Rejected-row audit file: `data/processed/final shortlist rejected rows audit.csv`

## Goal

Create a stricter final shortlist from the XGBoost predictions. This step keeps
the model output intact, then removes candidates that are not practical enough
for an India-first battery-material recommendation.

## Filtering Rules

- Keep only decision labels: {", ".join(allowed_decision_labels)}
- Keep only battery families: {", ".join(allowed_battery_families)}
- Remove formulas containing blocked/problematic elements: {", ".join(blocked_elements)}
- Minimum predicted stable probability: {minimum_stable_probability}
- Maximum predicted energy above hull: {maximum_predicted_energy_above_hull}
- Minimum India feasibility score: {minimum_india_feasibility_score}
- Keep only rows predicted stable by the XGBoost classifier.
- Use `predicted_energy_above_hull_clipped` for filtering and scoring because
  raw regressor predictions can be slightly negative, while physical energy
  above hull should not be negative.
- Exception for LFP and LMFP benchmark families: include rows with India score
  at least {benchmark_family_minimum_india_feasibility_score} and predicted
  energy above hull at most {benchmark_family_maximum_predicted_energy_above_hull},
  even when the classifier is conservative. This preserves the project benchmark
  chemistry instead of letting model bias remove it.

## Row Counts

- Input prediction rows: {len(prediction_dataframe):,}
- Final shortlist rows: {len(shortlist_dataframe):,}
- Rejected rows: {len(rejected_dataframe):,}

## Shortlist Battery Family Counts

{dataframe_to_markdown(family_counts)}

## Shortlist India Label Counts

{dataframe_to_markdown(label_counts)}

## Shortlist Rule Type Counts

{dataframe_to_markdown(rule_type_counts)}

## Top Final Shortlist Materials

{dataframe_to_markdown(top_shortlist)}

## Main Rejection Reasons

{dataframe_to_markdown(rejection_counts)}

## Interpretation

This final shortlist is stricter than the raw XGBoost ranking. It is intended
for human review, report writing, and the next candidate-selection step. It
should not replace the full training dataset.
"""

    metadata_folder.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary_text, encoding="utf-8")


def main():
    if not input_prediction_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_prediction_path}")

    prediction_dataframe = pd.read_csv(input_prediction_path)

    prediction_dataframe["parsed_elements"] = prediction_dataframe["formula"].apply(
        get_elements_from_formula
    )
    prediction_dataframe["blocked_elements"] = prediction_dataframe[
        "parsed_elements"
    ].apply(lambda elements: ";".join(get_blocked_elements(elements)))
    prediction_dataframe["predicted_energy_above_hull_clipped"] = prediction_dataframe[
        "predicted_energy_above_hull"
    ].clip(lower=0)
    prediction_dataframe["parsed_elements"] = prediction_dataframe[
        "parsed_elements"
    ].apply(lambda elements: ";".join(elements))
    prediction_dataframe["family_rank"] = prediction_dataframe["battery_family"].apply(
        get_family_rank
    )
    prediction_dataframe["shortlist_rule_type"] = prediction_dataframe.apply(
        get_shortlist_rule_type,
        axis=1,
    )
    prediction_dataframe["shortlist_rejection_reason"] = prediction_dataframe.apply(
        get_shortlist_rejection_reasons,
        axis=1,
    )
    prediction_dataframe["shortlist_score"] = prediction_dataframe.apply(
        calculate_shortlist_score,
        axis=1,
    )

    shortlist_dataframe = prediction_dataframe[
        prediction_dataframe["shortlist_rejection_reason"] == "Included in final shortlist"
    ].copy()

    rejected_dataframe = prediction_dataframe[
        prediction_dataframe["shortlist_rejection_reason"] != "Included in final shortlist"
    ].copy()

    shortlist_dataframe = shortlist_dataframe.sort_values(
        by=[
            "family_rank",
            "shortlist_score",
            "predicted_stable_probability",
            "india_feasibility_score",
            "predicted_energy_above_hull_clipped",
        ],
        ascending=[True, False, False, False, True],
    )

    rejected_dataframe = rejected_dataframe.sort_values(
        by=[
            "final_recommendation_score",
            "predicted_stable_probability",
            "india_feasibility_score",
        ],
        ascending=[False, False, False],
    )

    processed_folder.mkdir(parents=True, exist_ok=True)
    shortlist_dataframe.to_csv(output_shortlist_path, index=False)
    rejected_dataframe.to_csv(output_rejection_audit_path, index=False)

    write_summary(prediction_dataframe, shortlist_dataframe, rejected_dataframe)

    print(f"Input rows: {len(prediction_dataframe):,}")
    print(f"Shortlist rows: {len(shortlist_dataframe):,}")
    print(f"Rejected rows: {len(rejected_dataframe):,}")
    print(f"Shortlist saved: {output_shortlist_path}")
    print(f"Summary saved: {summary_path}")


if __name__ == "__main__":
    main()
