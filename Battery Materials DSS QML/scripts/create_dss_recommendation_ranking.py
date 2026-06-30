from datetime import date
from pathlib import Path

import pandas as pd


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_shortlist_path = processed_folder / "final india battery shortlist.csv"
material_output_path = processed_folder / "dss material recommendation ranking.csv"
compound_output_path = processed_folder / "dss compound recommendation ranking.csv"
family_output_path = processed_folder / "dss battery family recommendation ranking.csv"
summary_path = metadata_folder / "dss_recommendation_summary.md"


family_decision_rules = {
    "LFP-family": {
        "rank": 1,
        "decision": "Best near-term purchase direction",
        "reason": "India-friendly iron phosphate chemistry; avoids nickel and cobalt.",
    },
    "LMFP-family": {
        "rank": 2,
        "decision": "Good pilot and next-generation option",
        "reason": "LFP-like family with manganese; useful for improving performance.",
    },
    "LMO-family": {
        "rank": 3,
        "decision": "Selective low-cost option",
        "reason": "Manganese-based family; useful when cost matters, but needs checks.",
    },
    "Carbon-family": {
        "rank": 4,
        "decision": "Useful anode/support material",
        "reason": "Practical supporting material, but not a complete battery-cell choice.",
    },
    "Silicon-family": {
        "rank": 5,
        "decision": "R&D anode improvement option",
        "reason": "High-potential anode direction; better for blended or future designs.",
    },
    "Li-S or sulfide-family": {
        "rank": 6,
        "decision": "Long-term R&D option",
        "reason": "High-potential chemistry, but less direct for immediate purchase.",
    },
}


def dataframe_to_markdown(dataframe):
    if dataframe.empty:
        return "_No rows found._"

    headers = list(dataframe.columns)
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for _, dataframe_row in dataframe.iterrows():
        values = []
        for column_name in headers:
            value = dataframe_row[column_name]
            if pd.isna(value):
                value_text = ""
            elif isinstance(value, float):
                value_text = f"{value:.4f}"
            else:
                value_text = str(value)
            values.append(value_text.replace("|", "/"))
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def get_family_rule(battery_family):
    default_rule = {
        "rank": 99,
        "decision": "Review manually",
        "reason": "Family is not part of the main DSS priority list.",
    }
    return family_decision_rules.get(battery_family, default_rule)


def get_conceptual_reason(row):
    family_rule = get_family_rule(row["battery_family"])
    parameter_reason = (
        f"India score {row['india_feasibility_score']:.0f}; "
        f"predicted hull {row['predicted_energy_above_hull_clipped']:.4f}; "
        f"stable probability {row['predicted_stable_probability']:.4f}."
    )
    return family_rule["reason"] + " " + parameter_reason


def create_material_ranking(shortlist_dataframe):
    ranking_dataframe = shortlist_dataframe.copy()
    ranking_dataframe["dss_family_rank"] = ranking_dataframe["battery_family"].apply(
        lambda battery_family: get_family_rule(battery_family)["rank"]
    )
    ranking_dataframe["dss_decision"] = ranking_dataframe["battery_family"].apply(
        lambda battery_family: get_family_rule(battery_family)["decision"]
    )
    ranking_dataframe["short_conceptual_reason"] = ranking_dataframe.apply(
        get_conceptual_reason,
        axis=1,
    )

    ranking_dataframe = ranking_dataframe.sort_values(
        by=[
            "dss_family_rank",
            "shortlist_score",
            "india_feasibility_score",
            "predicted_energy_above_hull_clipped",
            "predicted_stable_probability",
        ],
        ascending=[True, False, False, True, False],
    ).reset_index(drop=True)
    ranking_dataframe.insert(0, "dss_rank", range(1, len(ranking_dataframe) + 1))

    output_columns = [
        "dss_rank",
        "formula",
        "material_id",
        "battery_family",
        "dss_decision",
        "shortlist_score",
        "india_feasibility_score",
        "predicted_stable_probability",
        "predicted_energy_above_hull_clipped",
        "band_gap",
        "is_stable",
        "shortlist_rule_type",
        "short_conceptual_reason",
    ]

    return ranking_dataframe[output_columns]


def create_family_ranking(material_ranking_dataframe):
    rows = []

    for battery_family, family_dataframe in material_ranking_dataframe.groupby(
        "battery_family"
    ):
        rule = get_family_rule(battery_family)
        top_material = family_dataframe.sort_values(
            by=["shortlist_score", "predicted_energy_above_hull_clipped"],
            ascending=[False, True],
        ).iloc[0]

        rows.append(
            {
                "dss_family_rank": rule["rank"],
                "battery_family": battery_family,
                "dss_decision": rule["decision"],
                "shortlist_rows": len(family_dataframe),
                "average_shortlist_score": round(
                    family_dataframe["shortlist_score"].mean(),
                    4,
                ),
                "average_india_feasibility_score": round(
                    family_dataframe["india_feasibility_score"].mean(),
                    4,
                ),
                "average_predicted_stable_probability": round(
                    family_dataframe["predicted_stable_probability"].mean(),
                    4,
                ),
                "median_predicted_energy_above_hull": round(
                    family_dataframe["predicted_energy_above_hull_clipped"].median(),
                    4,
                ),
                "top_material_id": top_material["material_id"],
                "top_formula": top_material["formula"],
                "short_reason": rule["reason"],
            }
        )

    family_ranking_dataframe = pd.DataFrame(rows)
    family_ranking_dataframe = family_ranking_dataframe.sort_values(
        by=["dss_family_rank", "average_shortlist_score"],
        ascending=[True, False],
    ).reset_index(drop=True)
    family_ranking_dataframe.insert(
        0,
        "dss_rank",
        range(1, len(family_ranking_dataframe) + 1),
    )
    return family_ranking_dataframe


def write_summary(material_ranking_dataframe, family_ranking_dataframe):
    top_materials = material_ranking_dataframe.head(15)

    summary_text = f"""# DSS Recommendation Summary

Generated on: {date.today().isoformat()}

## Purpose

This step frames the project as a Decision Support System. The goal is to help a
business user, EV owner, or battery decision-maker compare specific lithium
compound candidates using clear ranking parameters. Battery family is included
only as supporting context.

## Important Clarification

This is not direct commercial purchase advice for a branded battery product.
The dataset ranks lithium compound candidates. Battery family labels are used
as supporting context, not as the final recommendation by themselves.
The DSS output should support human decision-making, not replace testing,
safety certification, supplier checks, or cost analysis.

## DSS Output Files

- `data/processed/dss compound recommendation ranking.csv`
- `data/processed/dss battery family recommendation ranking.csv`
- `data/processed/dss material recommendation ranking.csv`

## Ranking Parameters Used

- Battery family priority for India-focused business use
- `shortlist_score`
- `india_feasibility_score`
- `predicted_stable_probability`
- `predicted_energy_above_hull_clipped`
- `band_gap`
- `shortlist_rule_type`

## Ranking Logic Note

The main recommendation is compound-level. The DSS ranks exact formulas such as
`LiFePO4`, `Li3Fe2(PO4)3`, or `Li2MgMn3O8`. The family label is used only to
give business context, because a formula belongs to a broader battery chemistry
group.

## Top Compound Recommendations

{dataframe_to_markdown(top_materials)}

## Supporting Battery Family Context

{dataframe_to_markdown(family_ranking_dataframe)}

## How To Explain In Presentation

This project is a DSS because it does not only train a model. It converts model
outputs and India-focused rules into a ranked compound decision table. A user
can see which exact compound formula is ranked higher, which family it belongs
to, and which parameters caused the rank.
"""

    metadata_folder.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary_text, encoding="utf-8")


def main():
    if not input_shortlist_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_shortlist_path}")

    shortlist_dataframe = pd.read_csv(input_shortlist_path)
    material_ranking_dataframe = create_material_ranking(shortlist_dataframe)
    family_ranking_dataframe = create_family_ranking(material_ranking_dataframe)

    processed_folder.mkdir(parents=True, exist_ok=True)
    material_ranking_dataframe.to_csv(material_output_path, index=False)
    material_ranking_dataframe.to_csv(compound_output_path, index=False)
    family_ranking_dataframe.to_csv(family_output_path, index=False)

    write_summary(material_ranking_dataframe, family_ranking_dataframe)

    print(f"Created: {family_output_path}")
    print(f"Created: {material_output_path}")
    print(f"Created: {compound_output_path}")
    print(f"Created: {summary_path}")
    print(f"Family rows: {len(family_ranking_dataframe)}")
    print(f"Material rows: {len(material_ranking_dataframe)}")


if __name__ == "__main__":
    main()
