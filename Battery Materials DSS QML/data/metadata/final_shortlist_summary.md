# Final India Battery Shortlist Summary

Generated on: 2026-06-28

Input file: `data/processed/xgboost predictions with india scores.csv`

Output file: `data/processed/final india battery shortlist.csv`

Rejected-row audit file: `data/processed/final shortlist rejected rows audit.csv`

## Goal

Create a stricter final shortlist from the XGBoost predictions. This step keeps
the model output intact, then removes candidates that are not practical enough
for an India-first battery-material recommendation.

## Filtering Rules

- Keep only decision labels: Recommend, Research Candidate
- Keep only battery families: LFP-family, LMFP-family, LMO-family, LTO-family, Silicon-family, Carbon-family, Li-S or sulfide-family
- Remove formulas containing blocked/problematic elements: Ac, Am, As, At, Be, Bk, Cd, Cf, Cm, Es, Fr, Gd, Ho, Hg, Ir, La, Lu, Md, No, Np, Os, Pa, Pb, Pd, Pm, Po, Pr, Pt, Pu, Ra, Re, Rh, Rn, Ru, Sc, Sm, Tc, Tb, Th, Tl, Tm, U, Y, Yb
- Minimum predicted stable probability: 0.65
- Maximum predicted energy above hull: 0.1
- Minimum India feasibility score: 70
- Keep only rows predicted stable by the XGBoost classifier.
- Use `predicted_energy_above_hull_clipped` for filtering and scoring because
  raw regressor predictions can be slightly negative, while physical energy
  above hull should not be negative.
- Exception for LFP and LMFP benchmark families: include rows with India score
  at least 90 and predicted
  energy above hull at most 0.06,
  even when the classifier is conservative. This preserves the project benchmark
  chemistry instead of letting model bias remove it.

## Row Counts

- Input prediction rows: 24,957
- Final shortlist rows: 629
- Rejected rows: 24,328

## Shortlist Battery Family Counts

| battery_family | count | percentage |
| --- | --- | --- |
| LFP-family | 464 | 73.77 |
| Li-S or sulfide-family | 91 | 14.47 |
| LMFP-family | 48 | 7.63 |
| Silicon-family | 17 | 2.7 |
| Carbon-family | 5 | 0.79 |
| LMO-family | 4 | 0.64 |

## Shortlist India Label Counts

| india_decision_label | count | percentage |
| --- | --- | --- |
| Recommend | 469 | 74.56 |
| Research Candidate | 160 | 25.44 |

## Shortlist Rule Type Counts

| shortlist_rule_type | count | percentage |
| --- | --- | --- |
| Benchmark family exception | 512 | 81.4 |
| Strict model shortlist | 117 | 18.6 |

## Top Final Shortlist Materials

| material_id | formula | battery_family | india_decision_label | shortlist_rule_type | shortlist_score | predicted_stable_probability | predicted_energy_above_hull_clipped | india_feasibility_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mp-19430 | Li3Fe2(PO4)3 | LFP-family | Recommend | Benchmark family exception | 59.52 | 0.16767046 | 0.011649002 | 98 |
| mp-554093 | Li9Fe3P8O29 | LFP-family | Recommend | Benchmark family exception | 59.1 | 0.1472201 | 0.009104118 | 98 |
| mp-1195117 | LiFeP2(HO3)2 | LFP-family | Recommend | Benchmark family exception | 57.42 | 0.17289971 | 0.016301585 | 94 |
| mp-19294 | LiFeP2O7 | LFP-family | Recommend | Benchmark family exception | 57.26 | 0.2221644 | 0.038671542 | 100 |
| mp-19017 | LiFePO4 | LFP-family | Recommend | Benchmark family exception | 56.48 | 0.13813923 | 0.023703082 | 100 |
| mp-26985 | Li2Fe3(P2O7)2 | LFP-family | Recommend | Benchmark family exception | 56.39 | 0.11544099 | 0.01552477 | 98 |
| mp-1198378 | NaLiFePO4F | LFP-family | Recommend | Benchmark family exception | 56.22 | 0.16727781 | 0.021042392 | 94 |
| mp-6373 | Li3Fe2(PO4)3 | LFP-family | Recommend | Benchmark family exception | 55.5 | 0.13168135 | 0.023631247 | 98 |
| mp-25993 | Li3Fe2(PO4)3 | LFP-family | Recommend | Benchmark family exception | 55.32 | 0.12640509 | 0.023346053 | 98 |
| mp-504179 | LiFe(PO3)3 | LFP-family | Recommend | Benchmark family exception | 54.88 | 0.13213262 | 0.02685131 | 98 |
| mp-768618 | Li3Fe2P2(CO7)2 | LFP-family | Recommend | Benchmark family exception | 54.47 | 0.0037309455 | 0.0 | 98 |
| mp-768667 | Li5Fe2P2(CO7)2 | LFP-family | Recommend | Benchmark family exception | 54.47 | 0.0037309455 | 0.0 | 98 |
| mp-756197 | Li3Fe2P2(CO7)2 | LFP-family | Recommend | Benchmark family exception | 54.41 | 0.0023854375 | 0.0 | 98 |
| mp-1177545 | Li3VFeP2(O4F)2 | LFP-family | Recommend | Benchmark family exception | 53.86 | 0.089776345 | 0.025876654 | 100 |
| mp-25406 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.77 | 0.0037309455 | 0.0 | 96 |
| mp-768562 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-768629 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-768630 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-779262 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-779778 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-1176696 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-1176704 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-1176714 | LiFePCO7 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-1177738 | Li3Fe2P2(CO7)2 | LFP-family | Recommend | Benchmark family exception | 53.71 | 0.0023854375 | 0.0 | 96 |
| mp-1177097 | Li8Fe7Cu(PO4)12 | LFP-family | Recommend | Benchmark family exception | 53.67 | 0.0016338566 | 0.0 | 96 |

## Main Rejection Reasons

| rejection_reason | count |
| --- | --- |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 8113 |
| Predicted stable probability is below threshold; XGBoost classifier predicted unstable | 4454 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Predicted stable probability is below threshold; Predicted energy above hull is above threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 4218 |
| Predicted stable probability is below threshold; Predicted energy above hull is above threshold; XGBoost classifier predicted unstable | 1028 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; India feasibility score is below threshold | 678 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Predicted stable probability is below threshold; India feasibility score is below threshold | 635 |
| Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 169 |
| Predicted stable probability is below threshold; Benchmark family predicted hull is above exception threshold | 154 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Contains blocked/problematic element(s): La; Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 126 |
| India decision label is not Recommend or Research Candidate; Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 123 |
| Predicted stable probability is below threshold; Predicted energy above hull is above threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 105 |
| Predicted stable probability is below threshold | 93 |
| India decision label is not Recommend or Research Candidate; Predicted stable probability is below threshold; Predicted energy above hull is above threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 87 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Contains blocked/problematic element(s): As; India feasibility score is below threshold | 75 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Contains blocked/problematic element(s): Y; Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 75 |
| Predicted stable probability is below threshold; Predicted energy above hull is above threshold; Benchmark family predicted hull is above exception threshold | 74 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Predicted stable probability is below threshold; Predicted energy above hull is above threshold; India feasibility score is below threshold | 67 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Contains blocked/problematic element(s): Pr; Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 63 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Contains blocked/problematic element(s): As; Predicted stable probability is below threshold; India feasibility score is below threshold; XGBoost classifier predicted unstable | 63 |
| India decision label is not Recommend or Research Candidate; Battery family is not in the final allowed family list; Contains blocked/problematic element(s): Pt; India feasibility score is below threshold | 61 |

## Interpretation

This final shortlist is stricter than the raw XGBoost ranking. It is intended
for human review, report writing, and the next candidate-selection step. It
should not replace the full training dataset.
