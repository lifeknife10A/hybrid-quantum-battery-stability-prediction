from datetime import date
from pathlib import Path
import math

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_shortlist_path = processed_folder / "final india battery shortlist.csv"
input_lithium_scored_path = processed_folder / "lithium india scored.csv"
material_output_path = processed_folder / "dss material recommendation ranking.csv"
compound_output_path = processed_folder / "dss compound recommendation ranking.csv"
hybrid_output_path = processed_folder / "hybrid qml xgboost compound ranking.csv"
family_output_path = processed_folder / "dss battery family recommendation ranking.csv"
summary_path = metadata_folder / "dss_recommendation_summary.md"

qml_feature_columns = [
    "formation_energy_per_atom",
    "has_o",
    "space_group_number",
    "theoretical",
]
qml_target_column = "is_stable"
qml_rows_per_class = 500
qml_random_states = [11, 22, 33, 44, 55, 66, 77, 88, 99, 111]
qml_angle_scale_value = math.pi
qml_entanglement_strength = math.pi
qml_c_value = 5.0


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


def convert_boolean_to_integer(dataframe, column_name):
    if dataframe[column_name].dtype == bool:
        dataframe[column_name] = dataframe[column_name].astype(int)
        return

    dataframe[column_name] = (
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


def get_bit_matrix(number_of_features):
    state_count = 2**number_of_features
    bit_matrix = np.zeros((state_count, number_of_features), dtype=float)

    for state_index in range(state_count):
        for feature_index in range(number_of_features):
            bit_value = (state_index >> (number_of_features - feature_index - 1)) & 1
            bit_matrix[state_index, feature_index] = bit_value

    return bit_matrix


def create_quantum_state_table(feature_table):
    number_of_features = feature_table.shape[1]
    bit_matrix = get_bit_matrix(number_of_features)
    state_rows = []

    for feature_row in feature_table:
        quantum_state = np.array([1.0 + 0.0j])

        for feature_value in feature_row:
            angle = qml_angle_scale_value * feature_value
            single_qubit_state = np.array(
                [
                    np.cos(angle / 2.0),
                    np.sin(angle / 2.0),
                ],
                dtype=np.complex128,
            )
            quantum_state = np.kron(quantum_state, single_qubit_state)

        phase_argument = np.zeros(len(quantum_state))
        for feature_index in range(number_of_features - 1):
            phase_argument += (
                bit_matrix[:, feature_index]
                * bit_matrix[:, feature_index + 1]
                * feature_row[feature_index]
                * feature_row[feature_index + 1]
            )

        phase_vector = np.exp(1j * qml_entanglement_strength * phase_argument)
        quantum_state = quantum_state * phase_vector
        state_rows.append(quantum_state)

    return np.vstack(state_rows)


def create_kernel_matrix(left_states, right_states):
    inner_product_matrix = left_states @ np.conjugate(right_states.T)
    return np.abs(inner_product_matrix) ** 2


def prepare_qml_dataframe(lithium_scored_dataframe):
    selected_columns = ["material_id"] + qml_feature_columns + [qml_target_column]
    clean_dataframe = lithium_scored_dataframe[selected_columns].copy()
    clean_dataframe = clean_dataframe.dropna(subset=qml_feature_columns + [qml_target_column])

    for column_name in ["has_o", "theoretical", qml_target_column]:
        convert_boolean_to_integer(clean_dataframe, column_name)

    for column_name in ["formation_energy_per_atom", "space_group_number"]:
        clean_dataframe[column_name] = pd.to_numeric(
            clean_dataframe[column_name],
            errors="coerce",
        )

    clean_dataframe = clean_dataframe.dropna(subset=qml_feature_columns + [qml_target_column])
    clean_dataframe["target_is_stable"] = clean_dataframe[qml_target_column].astype(int)
    return clean_dataframe


def create_qml_score_dataframe(lithium_scored_dataframe, shortlist_dataframe):
    qml_dataframe = prepare_qml_dataframe(lithium_scored_dataframe)
    shortlist_ids = set(shortlist_dataframe["material_id"])

    training_pool = qml_dataframe[~qml_dataframe["material_id"].isin(shortlist_ids)].copy()
    scoring_dataframe = shortlist_dataframe[["material_id"]].merge(
        qml_dataframe[["material_id"] + qml_feature_columns],
        on="material_id",
        how="left",
    )
    scoring_dataframe = scoring_dataframe.dropna(subset=qml_feature_columns)

    if len(scoring_dataframe) != len(shortlist_dataframe):
        missing_count = len(shortlist_dataframe) - len(scoring_dataframe)
        raise ValueError(
            f"QML scoring features are missing for {missing_count} shortlist rows."
        )

    stable_pool = training_pool[training_pool["target_is_stable"] == 1]
    unstable_pool = training_pool[training_pool["target_is_stable"] == 0]

    if len(stable_pool) < qml_rows_per_class or len(unstable_pool) < qml_rows_per_class:
        raise ValueError("Not enough rows to train balanced QML scoring model.")

    probability_columns = []
    result_dataframe = scoring_dataframe[["material_id"]].copy()

    for random_state in qml_random_states:
        stable_sample = stable_pool.sample(n=qml_rows_per_class, random_state=random_state)
        unstable_sample = unstable_pool.sample(n=qml_rows_per_class, random_state=random_state)
        training_dataframe = pd.concat(
            [stable_sample, unstable_sample],
            ignore_index=True,
        )
        training_dataframe = training_dataframe.sample(
            frac=1,
            random_state=random_state,
        ).reset_index(drop=True)

        scaler = MinMaxScaler()
        training_features = scaler.fit_transform(training_dataframe[qml_feature_columns])
        scoring_features = scaler.transform(scoring_dataframe[qml_feature_columns])

        training_states = create_quantum_state_table(training_features)
        scoring_states = create_quantum_state_table(scoring_features)

        train_kernel_matrix = create_kernel_matrix(training_states, training_states)
        score_kernel_matrix = create_kernel_matrix(scoring_states, training_states)

        classifier = SVC(
            kernel="precomputed",
            C=qml_c_value,
            probability=True,
            random_state=random_state,
        )
        classifier.fit(
            train_kernel_matrix,
            training_dataframe["target_is_stable"].to_numpy(dtype=int),
        )

        probability_column = f"qml_probability_seed_{random_state}"
        result_dataframe[probability_column] = classifier.predict_proba(
            score_kernel_matrix
        )[:, 1]
        probability_columns.append(probability_column)

    result_dataframe["qml_stable_probability"] = result_dataframe[
        probability_columns
    ].mean(axis=1)
    result_dataframe["qml_probability_std"] = result_dataframe[
        probability_columns
    ].std(axis=1)
    result_dataframe["qml_predicted_is_stable"] = (
        result_dataframe["qml_stable_probability"] >= 0.50
    )

    return result_dataframe[
        [
            "material_id",
            "qml_stable_probability",
            "qml_probability_std",
            "qml_predicted_is_stable",
        ]
    ]


def get_qml_confidence_band(qml_probability):
    if qml_probability >= 0.70:
        return "QML confident stable"
    if qml_probability >= 0.60:
        return "QML moderately stable"
    if qml_probability > 0.40:
        return "QML uncertain"
    if qml_probability > 0.30:
        return "QML moderately unstable"
    return "QML confident unstable"


def get_hybrid_role(row):
    qml_probability = row["qml_stable_probability"]
    xgboost_probability = row["xgboost_stable_probability"]

    if qml_probability >= 0.65 and xgboost_probability >= 0.50:
        return "QML-led; XGBoost agrees"
    if qml_probability >= 0.65 and xgboost_probability < 0.50:
        return "QML-led research review; XGBoost cautious"
    if 0.40 <= qml_probability <= 0.60:
        return "QML uncertain; XGBoost corrective backup"
    if qml_probability < 0.35 and xgboost_probability >= 0.50:
        return "QML caution; XGBoost recovery signal"
    return "QML-led ranking signal"


def add_hybrid_columns(shortlist_dataframe, lithium_scored_dataframe):
    qml_score_dataframe = create_qml_score_dataframe(
        lithium_scored_dataframe,
        shortlist_dataframe,
    )
    hybrid_dataframe = shortlist_dataframe.merge(
        qml_score_dataframe,
        on="material_id",
        how="left",
    )
    hybrid_dataframe["xgboost_stable_probability"] = hybrid_dataframe[
        "predicted_stable_probability"
    ]
    hybrid_dataframe["qml_confidence_band"] = hybrid_dataframe[
        "qml_stable_probability"
    ].apply(get_qml_confidence_band)

    qml_confidence_strength = (
        (hybrid_dataframe["qml_stable_probability"] - 0.50).abs() * 2.0
    ).clip(lower=0.0, upper=1.0)
    hybrid_dataframe["qml_weight"] = (0.35 + 0.35 * qml_confidence_strength).round(4)
    hybrid_dataframe["xgboost_correction_weight"] = (
        1.0 - hybrid_dataframe["qml_weight"]
    ).round(4)
    hybrid_dataframe["hybrid_stable_probability"] = (
        hybrid_dataframe["qml_weight"] * hybrid_dataframe["qml_stable_probability"]
        + hybrid_dataframe["xgboost_correction_weight"]
        * hybrid_dataframe["xgboost_stable_probability"]
    ).round(6)
    hybrid_dataframe["model_disagreement"] = (
        (
            hybrid_dataframe["qml_stable_probability"]
            - hybrid_dataframe["xgboost_stable_probability"]
        ).abs()
        >= 0.35
    )
    hybrid_dataframe["hybrid_decision_role"] = hybrid_dataframe.apply(
        get_hybrid_role,
        axis=1,
    )

    hull_score = (
        1.0
        - hybrid_dataframe["predicted_energy_above_hull_clipped"].clip(0.0, 0.10)
        / 0.10
    ) * 100.0
    disagreement_penalty = hybrid_dataframe["model_disagreement"].astype(int) * 5.0

    hybrid_dataframe["hybrid_recommendation_score"] = (
        40.0 * hybrid_dataframe["hybrid_stable_probability"]
        + 0.30 * hybrid_dataframe["india_feasibility_score"]
        + 0.20 * hull_score
        + 0.10 * hybrid_dataframe["shortlist_score"]
        - disagreement_penalty
    ).round(4)

    return hybrid_dataframe


def get_conceptual_reason(row):
    family_rule = get_family_rule(row["battery_family"])
    parameter_reason = (
        f"India score {row['india_feasibility_score']:.0f}; "
        f"QML probability {row['qml_stable_probability']:.4f}; "
        f"XGBoost probability {row['xgboost_stable_probability']:.4f}; "
        f"hybrid probability {row['hybrid_stable_probability']:.4f}; "
        f"predicted hull {row['predicted_energy_above_hull_clipped']:.4f}."
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
            "hybrid_recommendation_score",
            "hybrid_stable_probability",
            "india_feasibility_score",
            "predicted_energy_above_hull_clipped",
        ],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)
    ranking_dataframe.insert(0, "dss_rank", range(1, len(ranking_dataframe) + 1))

    output_columns = [
        "dss_rank",
        "formula",
        "material_id",
        "battery_family",
        "dss_decision",
        "hybrid_recommendation_score",
        "hybrid_stable_probability",
        "qml_stable_probability",
        "xgboost_stable_probability",
        "qml_weight",
        "xgboost_correction_weight",
        "qml_confidence_band",
        "hybrid_decision_role",
        "model_disagreement",
        "qml_probability_std",
        "shortlist_score",
        "india_feasibility_score",
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
            by=[
                "hybrid_recommendation_score",
                "hybrid_stable_probability",
                "predicted_energy_above_hull_clipped",
            ],
            ascending=[False, False, True],
        ).iloc[0]

        rows.append(
            {
                "dss_family_rank": rule["rank"],
                "battery_family": battery_family,
                "dss_decision": rule["decision"],
                "shortlist_rows": len(family_dataframe),
                "average_hybrid_recommendation_score": round(
                    family_dataframe["hybrid_recommendation_score"].mean(),
                    4,
                ),
                "average_hybrid_stable_probability": round(
                    family_dataframe["hybrid_stable_probability"].mean(),
                    4,
                ),
                "average_qml_stable_probability": round(
                    family_dataframe["qml_stable_probability"].mean(),
                    4,
                ),
                "average_xgboost_stable_probability": round(
                    family_dataframe["xgboost_stable_probability"].mean(),
                    4,
                ),
                "average_shortlist_score": round(
                    family_dataframe["shortlist_score"].mean(),
                    4,
                ),
                "average_india_feasibility_score": round(
                    family_dataframe["india_feasibility_score"].mean(),
                    4,
                ),
                "average_predicted_stable_probability": round(
                    family_dataframe["xgboost_stable_probability"].mean(),
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
        by=[
            "average_hybrid_recommendation_score",
            "average_hybrid_stable_probability",
            "average_india_feasibility_score",
        ],
        ascending=[False, False, False],
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

The DSS is now a QML-primary hybrid ranking. The simulated QML kernel gives the
first stability signal. XGBoost is used as a corrective backup when the QML
probability is uncertain or when the two models disagree strongly.

## Important Clarification

This is not direct commercial purchase advice for a branded battery product.
The dataset ranks lithium compound candidates. Battery family labels are used
as supporting context, not as the final recommendation by themselves.
The DSS output should support human decision-making, not replace testing,
safety certification, supplier checks, or cost analysis.

## DSS Output Files

- `data/processed/dss compound recommendation ranking.csv`
- `data/processed/hybrid qml xgboost compound ranking.csv`
- `data/processed/dss battery family recommendation ranking.csv`
- `data/processed/dss material recommendation ranking.csv`

## Ranking Parameters Used

- `hybrid_recommendation_score`
- `hybrid_stable_probability`
- `qml_stable_probability`
- `xgboost_stable_probability`
- `qml_confidence_band`
- `hybrid_decision_role`
- `india_feasibility_score`
- `predicted_energy_above_hull_clipped`
- `band_gap`
- `shortlist_rule_type`

## Ranking Logic Note

The main recommendation is compound-level. The DSS ranks exact formulas such as
`LiFePO4`, `Li3Fe2(PO4)3`, or `Li2MgMn3O8`. The family label is used only to
give business context, because a formula belongs to a broader battery chemistry
group.

QML has the larger role when it is confident. XGBoost has the larger corrective
role when QML is close to 0.50 or when the two models disagree. This keeps the
project quantum-led while still using XGBoost as a practical safety check.

## Top Compound Recommendations

{dataframe_to_markdown(top_materials)}

## Supporting Battery Family Context

{dataframe_to_markdown(family_ranking_dataframe)}

## How To Explain In Presentation

This project is a DSS because it does not only train a model. It converts model
outputs and India-focused rules into a ranked compound decision table. The user
can see the exact formula, QML probability, XGBoost probability, hybrid
probability, India feasibility score, and short conceptual reason.
"""

    metadata_folder.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary_text, encoding="utf-8")


def main():
    if not input_shortlist_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_shortlist_path}")
    if not input_lithium_scored_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_lithium_scored_path}")

    shortlist_dataframe = pd.read_csv(input_shortlist_path)
    lithium_scored_dataframe = pd.read_csv(input_lithium_scored_path)
    hybrid_shortlist_dataframe = add_hybrid_columns(
        shortlist_dataframe,
        lithium_scored_dataframe,
    )
    material_ranking_dataframe = create_material_ranking(hybrid_shortlist_dataframe)
    family_ranking_dataframe = create_family_ranking(material_ranking_dataframe)

    processed_folder.mkdir(parents=True, exist_ok=True)
    material_ranking_dataframe.to_csv(material_output_path, index=False)
    material_ranking_dataframe.to_csv(compound_output_path, index=False)
    material_ranking_dataframe.to_csv(hybrid_output_path, index=False)
    family_ranking_dataframe.to_csv(family_output_path, index=False)

    write_summary(material_ranking_dataframe, family_ranking_dataframe)

    print(f"Created: {family_output_path}")
    print(f"Created: {material_output_path}")
    print(f"Created: {compound_output_path}")
    print(f"Created: {hybrid_output_path}")
    print(f"Created: {summary_path}")
    print(f"Family rows: {len(family_ranking_dataframe)}")
    print(f"Material rows: {len(material_ranking_dataframe)}")


if __name__ == "__main__":
    main()
