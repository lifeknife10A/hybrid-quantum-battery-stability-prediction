# Lithium India Scored Dataset Summary

Input file: `data/processed/materials_project_lithium.csv`

Output file: `data/processed/lithium india scored.csv`

Rows kept: 24,957

No rows were removed. India feasibility is added as scoring columns so the ML
model can still train on the full lithium dataset first.

## Decision Label Counts

- Avoid / Benchmark: 4,370
- Caution: 13,524
- Recommend: 1,180
- Research Candidate: 5,883

## Battery Family Counts

- Carbon-family: 477
- LCO-family: 3,541
- LFP-family: 735
- LLZO-family: 3
- LMFP-family: 61
- LMO-family: 3,394
- LTO-family: 964
- Li-S or sulfide-family: 892
- NMC-family: 11
- Other lithium material: 14,027
- Silicon-family: 852

## Scoring Notes

- LFP and carbon-family materials are treated as the strongest India-first candidates.
- LMFP, LMO, LTO, silicon, sulfur/sulfide, and LLZO families are treated as research candidates.
- Nickel-heavy and cobalt-heavy families are kept, but marked as caution or benchmark classes.
- Deprecated entries are kept in the file but marked `Avoid / Benchmark`.
- The score is a project screening score, not a lab-certified battery efficiency value.

## Column Dictionary

| Column Name | Definition | Purpose |
| --- | --- | --- |
| `material_id` | Unique Materials Project identifier for the material. | Used to trace each row back to the original source material. |
| `formula` | Chemical formula of the material. | Main human-readable material identity and input for element parsing. |
| `space_group_number` | Numeric crystallographic space group. | Captures crystal symmetry for ML and material comparison. |
| `crystal_system` | Crystal system category such as Cubic, Monoclinic, or Trigonal. | Helps compare materials by broad structure type. |
| `formation_energy_per_atom` | Computed formation energy per atom. | Important stability-related target or feature for ML. |
| `energy_above_hull` | Computed energy above the convex hull. | Main stability indicator; lower values usually mean more stable materials. |
| `is_stable` | Boolean flag from the source dataset indicating stability. | Useful target column for classification models. |
| `band_gap` | Computed electronic band gap. | Helps identify metallic, semiconducting, or insulating behavior. |
| `is_metal` | Boolean flag showing whether the material is metallic. | Useful for separating conductive and non-conductive candidates. |
| `theoretical` | Boolean flag showing whether the material is theoretical. | Helps separate predicted/theoretical entries from known materials. |
| `deprecated` | Boolean flag showing whether the entry is deprecated in the source data. | Deprecated rows are kept but marked lower priority. |
| `parsed_elements` | Semicolon-separated list of elements parsed from the formula. | Makes the element rule logic visible and easy to audit. |
| `number_of_elements` | Count of unique elements in the formula. | Simple feature showing material complexity. |
| `has_li` | True if lithium is present. | Confirms the row belongs to the lithium-filtered dataset. |
| `has_o` | True if oxygen is present. | Helps detect oxide cathode or solid-electrolyte families. |
| `has_fe` | True if iron is present. | Supports LFP and India-favorable iron-based family detection. |
| `has_p` | True if phosphorous is present. | Supports phosphate-family detection such as LFP and LMFP. |
| `has_mn` | True if manganese is present. | Supports manganese-family detection such as LMO and LMFP. |
| `has_co` | True if cobalt is present. | Marks cobalt-heavy materials for caution due to supply-chain risk. |
| `has_ni` | True if nickel is present. | Marks nickel-heavy materials for caution due to supply-chain risk. |
| `has_ti` | True if titanium is present. | Supports LTO and titanium-based safety/fast-charge families. |
| `has_c` | True if carbon is present. | Supports carbon/graphite anode-family detection. |
| `has_si` | True if silicon is present. | Supports silicon-containing anode research candidates. |
| `has_s` | True if sulfur is present. | Supports sulfur and sulfide-family research candidates. |
| `has_al` | True if aluminum is present. | Helps detect NCA-like chemistry and aluminum-containing materials. |
| `has_la` | True if lanthanum is present. | Helps detect LLZO-like solid-electrolyte candidates. |
| `has_zr` | True if zirconium is present. | Helps detect LLZO-like solid-electrolyte candidates. |
| `has_f` | True if fluorine is present. | Marks fluorine-containing materials for safety/handling caution. |
| `has_cu` | True if copper is present. | Tracks copper-containing candidates because copper is battery-relevant. |
| `has_high_caution_element` | True if the material contains high-caution elements like cobalt, nickel, cadmium, lead, mercury, arsenic, or beryllium. | Provides a simple risk flag for India feasibility and safety screening. |
| `battery_family` | Rule-based family label such as LFP-family, LMO-family, LTO-family, NMC-family, or Other lithium material. | Groups materials into battery-relevant families for reporting and filtering. |
| `india_base_score` | Starting India feasibility score assigned from the battery family. | Encodes the report's family-level recommendation logic. |
| `india_stability_adjustment` | Score adjustment based on `is_stable`, `energy_above_hull`, and `deprecated`. | Rewards stable materials and penalizes weak or deprecated entries. |
| `india_element_adjustment` | Score adjustment based on helpful or risky elements. | Rewards India-favorable elements and penalizes supply-chain or safety-risk elements. |
| `india_feasibility_score` | Final score from 0 to 100 after base score and adjustments. | Main numeric score for India-based re-ranking after model prediction. |
| `india_decision_label` | Final rule-based label: Recommend, Research Candidate, Caution, or Avoid / Benchmark. | Makes the dataset easy to filter for project decisions. |
| `india_rule_reason` | Short explanation for why the row received its family-based decision. | Keeps the scoring explainable for the report and future evaluation. |
