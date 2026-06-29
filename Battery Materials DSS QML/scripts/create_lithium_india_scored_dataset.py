from pathlib import Path
import re

import pandas as pd


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "materials_project_lithium.csv"
output_csv_path = processed_folder / "lithium india scored.csv"
summary_path = metadata_folder / "lithium_india_scored_summary.md"

required_columns = [
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
]

important_elements = [
    "Li",
    "O",
    "Fe",
    "P",
    "Mn",
    "Co",
    "Ni",
    "Ti",
    "C",
    "Si",
    "S",
    "Al",
    "La",
    "Zr",
    "F",
    "Cu",
]

high_caution_elements = [
    "Co",
    "Ni",
    "Cd",
    "Pb",
    "Hg",
    "As",
    "Be",
]


def get_elements_from_formula(formula):
    if not isinstance(formula, str):
        return []

    return sorted(set(re.findall(r"[A-Z][a-z]?", formula)))


def has_all_elements(elements, needed_elements):
    element_set = set(elements)
    return set(needed_elements).issubset(element_set)


def has_any_element(elements, needed_elements):
    element_set = set(elements)
    return len(set(needed_elements).intersection(element_set)) > 0


def get_battery_family(elements):
    if has_all_elements(elements, ["Li", "Ni", "Co", "Al", "O"]):
        return "NCA-family"

    if has_all_elements(elements, ["Li", "Ni", "Mn", "Co", "O"]):
        return "NMC-family"

    if has_all_elements(elements, ["Li", "Mn", "Fe", "P", "O"]):
        return "LMFP-family"

    if has_all_elements(elements, ["Li", "Fe", "P", "O"]):
        return "LFP-family"

    if has_all_elements(elements, ["Li", "Co", "O"]):
        return "LCO-family"

    if has_all_elements(elements, ["Li", "Mn", "O"]):
        return "LMO-family"

    if has_all_elements(elements, ["Li", "La", "Zr", "O"]):
        return "LLZO-family"

    if has_all_elements(elements, ["Li", "Ti", "O"]):
        return "LTO-family"

    if has_all_elements(elements, ["Li", "S"]):
        return "Li-S or sulfide-family"

    if has_all_elements(elements, ["Li", "Si", "O"]):
        return "Silicon-family"

    if has_all_elements(elements, ["Li", "C"]):
        return "Carbon-family"

    return "Other lithium material"


def get_base_score(battery_family):
    base_scores = {
        "LFP-family": 88,
        "LMFP-family": 84,
        "Carbon-family": 82,
        "LMO-family": 76,
        "Silicon-family": 74,
        "LTO-family": 72,
        "Li-S or sulfide-family": 66,
        "LLZO-family": 60,
        "NMC-family": 55,
        "NCA-family": 48,
        "LCO-family": 45,
        "Other lithium material": 50,
    }

    return base_scores[battery_family]


def get_stability_adjustment(row):
    adjustment = 0

    if bool(row["is_stable"]):
        adjustment = adjustment + 6

    energy_above_hull = row["energy_above_hull"]

    if pd.isna(energy_above_hull):
        adjustment = adjustment - 3
    elif energy_above_hull <= 0.025:
        adjustment = adjustment + 5
    elif energy_above_hull <= 0.05:
        adjustment = adjustment + 3
    elif energy_above_hull <= 0.10:
        adjustment = adjustment + 1
    elif energy_above_hull > 0.20:
        adjustment = adjustment - 4

    if bool(row["deprecated"]):
        adjustment = adjustment - 15

    return adjustment


def get_element_adjustment(elements):
    adjustment = 0

    if "Fe" in elements:
        adjustment = adjustment + 3
    if "Mn" in elements:
        adjustment = adjustment + 3
    if "P" in elements:
        adjustment = adjustment + 2
    if "C" in elements:
        adjustment = adjustment + 2
    if "Si" in elements:
        adjustment = adjustment + 2
    if "Ti" in elements:
        adjustment = adjustment + 2
    if "S" in elements:
        adjustment = adjustment + 1

    if "Co" in elements:
        adjustment = adjustment - 5
    if "Ni" in elements:
        adjustment = adjustment - 4
    if "F" in elements:
        adjustment = adjustment - 4

    risky_elements = ["Cd", "Pb", "Hg", "As", "Be"]
    if has_any_element(elements, risky_elements):
        adjustment = adjustment - 10

    return adjustment


def get_india_decision_label(row):
    if bool(row["deprecated"]):
        return "Avoid / Benchmark"

    battery_family = row["battery_family"]
    score = row["india_feasibility_score"]

    if battery_family in ["LFP-family", "Carbon-family"] and score >= 75:
        return "Recommend"

    if battery_family in [
        "LMFP-family",
        "LMO-family",
        "Silicon-family",
        "LTO-family",
        "Li-S or sulfide-family",
        "LLZO-family",
    ]:
        if score >= 55:
            return "Research Candidate"
        return "Caution"

    if battery_family in ["NMC-family", "NCA-family"]:
        return "Caution"

    if battery_family == "LCO-family":
        return "Avoid / Benchmark"

    if score >= 70 and not row["has_high_caution_element"]:
        return "Research Candidate"

    return "Caution"


def get_rule_reason(row):
    battery_family = row["battery_family"]

    if bool(row["deprecated"]):
        return "Deprecated Materials Project entry; keep only for reference."

    reasons = {
        "LFP-family": "India-friendly benchmark family; avoids nickel and cobalt.",
        "LMFP-family": "Manganese phosphate research family; useful extension of LFP.",
        "Carbon-family": "Anode-side carbon family; graphite is strategically important.",
        "LMO-family": "Manganese oxide family; useful but needs cycle-life caution.",
        "Silicon-family": "Silicon-containing research family; high-capacity anode direction.",
        "LTO-family": "Titanium oxide family; useful for safety and fast-charge niches.",
        "Li-S or sulfide-family": "Sulfur or sulfide research family; useful for future battery directions.",
        "LLZO-family": "Solid-electrolyte research family; useful but less dataset coverage.",
        "NMC-family": "Nickel and cobalt intensive; keep as caution or comparison class.",
        "NCA-family": "Nickel and cobalt intensive; low India-first priority.",
        "LCO-family": "Cobalt-heavy family; keep only as benchmark or caution class.",
        "Other lithium material": "No clear India-priority battery family detected from formula.",
    }

    return reasons[battery_family]


def check_required_columns(dataframe):
    missing_columns = []

    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Input file is missing required columns: {missing_text}")


def clamp_score(score):
    if score < 0:
        return 0
    if score > 100:
        return 100
    return int(round(score))


def create_summary(scored_dataframe):
    label_counts = scored_dataframe["india_decision_label"].value_counts().sort_index()
    family_counts = scored_dataframe["battery_family"].value_counts().sort_index()

    label_lines = []
    for label, count in label_counts.items():
        label_lines.append(f"- {label}: {count:,}")

    family_lines = []
    for family, count in family_counts.items():
        family_lines.append(f"- {family}: {count:,}")

    summary_text = f"""# Lithium India Scored Dataset Summary

Input file: `data/processed/materials_project_lithium.csv`

Output file: `data/processed/lithium india scored.csv`

Rows kept: {len(scored_dataframe):,}

No rows were removed. India feasibility is added as scoring columns so the ML
model can still train on the full lithium dataset first.

## Decision Label Counts

{chr(10).join(label_lines)}

## Battery Family Counts

{chr(10).join(family_lines)}

## Scoring Notes

- LFP and carbon-family materials are treated as the strongest India-first candidates.
- LMFP, LMO, LTO, silicon, sulfur/sulfide, and LLZO families are treated as research candidates.
- Nickel-heavy and cobalt-heavy families are kept, but marked as caution or benchmark classes.
- Deprecated entries are kept in the file but marked `Avoid / Benchmark`.
- The score is a project screening score, not a lab-certified battery efficiency value.
"""

    metadata_folder.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary_text, encoding="utf-8")


def main():
    if not input_csv_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_csv_path}")

    dataframe = pd.read_csv(input_csv_path)
    check_required_columns(dataframe)

    dataframe["parsed_elements"] = dataframe["formula"].apply(get_elements_from_formula)
    dataframe["number_of_elements"] = dataframe["parsed_elements"].apply(len)

    for element_symbol in important_elements:
        column_name = "has_" + element_symbol.lower()
        dataframe[column_name] = dataframe["parsed_elements"].apply(
            lambda elements, symbol=element_symbol: symbol in elements
        )

    dataframe["has_high_caution_element"] = dataframe["parsed_elements"].apply(
        lambda elements: has_any_element(elements, high_caution_elements)
    )

    dataframe["battery_family"] = dataframe["parsed_elements"].apply(get_battery_family)
    dataframe["india_base_score"] = dataframe["battery_family"].apply(get_base_score)
    dataframe["india_stability_adjustment"] = dataframe.apply(
        get_stability_adjustment,
        axis=1,
    )
    dataframe["india_element_adjustment"] = dataframe["parsed_elements"].apply(
        get_element_adjustment
    )
    dataframe["india_feasibility_score"] = dataframe.apply(
        lambda row: clamp_score(
            row["india_base_score"]
            + row["india_stability_adjustment"]
            + row["india_element_adjustment"]
        ),
        axis=1,
    )
    dataframe["india_decision_label"] = dataframe.apply(get_india_decision_label, axis=1)
    dataframe["india_rule_reason"] = dataframe.apply(get_rule_reason, axis=1)
    dataframe["parsed_elements"] = dataframe["parsed_elements"].apply(
        lambda elements: ";".join(elements)
    )

    dataframe.to_csv(output_csv_path, index=False)
    create_summary(dataframe)

    print(f"Rows written: {len(dataframe):,}")
    print(f"Output CSV: {output_csv_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
