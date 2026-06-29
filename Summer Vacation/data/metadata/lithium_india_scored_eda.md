# Lithium India Scored EDA

Generated on: 2026-06-28

Input file: `data/processed/lithium india scored.csv`

## Basic Dataset Size

- Total rows: 24,957
- Total columns: 37
- Stable rows: 4,052
- Unstable rows: 20,905

## Missing Values

| column | missing_count | missing_percentage |
| --- | --- | --- |
| formation_energy_per_atom | 889 | 3.56 |
| energy_above_hull | 889 | 3.56 |
| band_gap | 889 | 3.56 |
| is_stable | 0 | 0.0 |
| battery_family | 0 | 0.0 |
| india_feasibility_score | 0 | 0.0 |
| india_decision_label | 0 | 0.0 |

## Numeric Column Summary

| column | non_missing | mean | median | minimum | maximum |
| --- | --- | --- | --- | --- | --- |
| formation_energy_per_atom | 24068 | -1.8747 | -2.1208 | -4.0953 | 5.2541 |
| energy_above_hull | 24068 | 0.1237 | 0.0532 | 0.0 | 7.6076 |
| band_gap | 24068 | 1.2287 | 0.647 | 0.0 | 8.7161 |
| india_feasibility_score | 24957 | 59.2535 | 55.0 | 18.0 | 100.0 |

## India Decision Label Distribution

| india_decision_label | count | percentage |
| --- | --- | --- |
| Caution | 13524 | 54.19 |
| Research Candidate | 5883 | 23.57 |
| Avoid / Benchmark | 4370 | 17.51 |
| Recommend | 1180 | 4.73 |

## Battery Family Distribution

| battery_family | count | percentage |
| --- | --- | --- |
| Other lithium material | 14027 | 56.2 |
| LCO-family | 3541 | 14.19 |
| LMO-family | 3394 | 13.6 |
| LTO-family | 964 | 3.86 |
| Li-S or sulfide-family | 892 | 3.57 |
| Silicon-family | 852 | 3.41 |
| LFP-family | 735 | 2.95 |
| Carbon-family | 477 | 1.91 |
| LMFP-family | 61 | 0.24 |
| NMC-family | 11 | 0.04 |
| LLZO-family | 3 | 0.01 |

## Family-Level Summary

| battery_family | rows | stable_rows | average_india_score | average_energy_above_hull | median_energy_above_hull | average_band_gap | stable_percentage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LFP-family | 735 | 11 | 94.8272 | 0.1098 | 0.0499 | 2.1074 | 1.5 |
| LMFP-family | 61 | 0 | 93.4262 | 0.0829 | 0.0258 | 2.0907 | 0.0 |
| Carbon-family | 477 | 55 | 85.1719 | 0.136 | 0.0798 | 2.1582 | 11.53 |
| LMO-family | 3394 | 62 | 80.8854 | 0.112 | 0.0509 | 1.0759 | 1.83 |
| Silicon-family | 852 | 57 | 78.1573 | 0.1422 | 0.0635 | 2.4233 | 6.69 |
| LTO-family | 964 | 31 | 75.3039 | 0.1055 | 0.0522 | 0.8789 | 3.22 |
| Li-S or sulfide-family | 892 | 259 | 71.2769 | 0.081 | 0.0257 | 1.721 | 29.04 |
| LLZO-family | 3 | 0 | 62.0 | 0.0761 | 0.0932 | 1.3966 | 0.0 |
| Other lithium material | 14027 | 3546 | 52.4171 | 0.1279 | 0.041 | 1.2656 | 25.28 |
| NMC-family | 11 | 0 | 50.5455 | 0.0824 | 0.0867 | 0.3589 | 0.0 |
| LCO-family | 3541 | 31 | 42.2146 | 0.1314 | 0.0839 | 0.5911 | 0.88 |

## Family vs India Decision Label

| battery_family | Avoid / Benchmark | Caution | Recommend | Research Candidate |
| --- | --- | --- | --- | --- |
| Carbon-family | 12 | 3 | 462 | 0 |
| LCO-family | 3541 | 0 | 0 | 0 |
| LFP-family | 17 | 0 | 718 | 0 |
| LLZO-family | 0 | 0 | 0 | 3 |
| LMFP-family | 0 | 0 | 0 | 61 |
| LMO-family | 174 | 0 | 0 | 3220 |
| LTO-family | 67 | 0 | 0 | 897 |
| Li-S or sulfide-family | 18 | 0 | 0 | 874 |
| NMC-family | 0 | 11 | 0 | 0 |
| Other lithium material | 517 | 13510 | 0 | 0 |
| Silicon-family | 24 | 0 | 0 | 828 |

## Top Recommended Materials

These are the strongest India-first candidates by rule score.

| material_id | formula | battery_family | india_feasibility_score | energy_above_hull | band_gap | is_stable |
| --- | --- | --- | --- | --- | --- | --- |
| mp-26003 | LiFe(PO3)3 | LFP-family | 100 | 0.0 | 3.9487 | True |
| mp-19017 | LiFePO4 | LFP-family | 100 | 0.0 | 3.9224 | True |
| mp-27007 | LiFe2P3O10 | LFP-family | 100 | 0.0 | 3.1686 | True |
| mp-25977 | LiFe(PO3)4 | LFP-family | 100 | 0.0 | 2.938 | True |
| mp-1222830 | Li2InFe(P2O7)2 | LFP-family | 100 | 0.0 | 2.7432 | True |
| mp-1177545 | Li3VFeP2(O4F)2 | LFP-family | 100 | 0.0 | 2.4464 | True |
| mp-766101 | Li2FeP2HO8 | LFP-family | 100 | 0.0 | 2.4221 | True |
| mp-1222972 | Li2TiFe(PO4)3 | LFP-family | 100 | 0.0 | 2.3733 | True |
| mp-1177781 | Li2VFe(P2O7)2 | LFP-family | 100 | 0.0 | 1.9038 | True |
| mp-19294 | LiFeP2O7 | LFP-family | 100 | 0.0 | 1.7443 | True |
| mp-756507 | LiFePHO5 | LFP-family | 100 | 0.0 | 0.0 | True |
| mp-694934 | Li2TiFe(PO4)3 | LFP-family | 100 | 0.00062597 | 2.4993 | False |
| mp-1222519 | LiFe3SiPO8 | LFP-family | 100 | 0.004399614 | 3.5642 | False |
| mp-753770 | Li2FePCO7 | LFP-family | 100 | 0.008345268 | 2.3388 | False |
| mp-755968 | Na5LiFe2P2(CO7)2 | LFP-family | 100 | 0.009503854 | 3.7977 | False |

## Top Research Candidate Materials

These are promising candidates, but they need more checking before being treated
as direct recommendations.

| material_id | formula | battery_family | india_feasibility_score | energy_above_hull | band_gap | is_stable |
| --- | --- | --- | --- | --- | --- | --- |
| mp-761246 | Li2MnFe(PO4)2 | LMFP-family | 97 | 0.000534143 | 3.6926 | False |
| mp-759138 | Li2MnFe(PO4)2 | LMFP-family | 97 | 0.001083382 | 3.9508 | False |
| mp-754635 | Li2MnFe(PO4)2 | LMFP-family | 97 | 0.001092972 | 3.9838 | False |
| mp-861717 | Li8MnFe7(PO4)8 | LMFP-family | 97 | 0.001716703 | 3.8807 | False |
| mp-849430 | Li8MnFe7(PO4)8 | LMFP-family | 97 | 0.001812669 | 3.9032 | False |
| mp-849382 | Li16Mn15Fe(PO4)16 | LMFP-family | 97 | 0.001841759 | 3.4633 | False |
| mp-775195 | Li12Mn11Fe(PO4)12 | LMFP-family | 97 | 0.001875037 | 3.6905 | False |
| mp-783919 | Li4MnFe3(PO4)4 | LMFP-family | 97 | 0.002042868 | 3.8643 | False |
| mp-849356 | Li4Mn3Fe(PO4)4 | LMFP-family | 97 | 0.002103293 | 3.5657 | False |
| mp-764613 | Li4MnFe3(PO4)4 | LMFP-family | 97 | 0.00216876 | 4.0066 | False |
| mp-766376 | Li4Mn3Fe(PO4)4 | LMFP-family | 97 | 0.002360386 | 3.5811 | False |
| mp-775945 | Li2MnFe(PO4)2 | LMFP-family | 97 | 0.002493695 | 3.8121 | False |
| mp-773519 | Li4Mn3Fe(PO4)4 | LMFP-family | 97 | 0.002513214 | 3.6773 | False |
| mp-775189 | Li2MnFe(PO4)2 | LMFP-family | 97 | 0.002621204 | 3.0175 | False |
| mp-1176968 | Li7Mn2Fe6(PO4)8 | LMFP-family | 97 | 0.010048688 | 1.4371 | False |

## Sample Caution Materials

These rows are kept for training and comparison, but should not be treated as
India-first recommendations without extra justification.

| material_id | formula | battery_family | india_feasibility_score | energy_above_hull | band_gap | is_stable |
| --- | --- | --- | --- | --- | --- | --- |
| mp-560581 | LiBeH8CNOF4 | Carbon-family | 73 | 0.038504603 | 5.6948 | False |
| mp-771015 | Li3NiAsCO7 | Carbon-family | 73 | 0.047331232 | 3.5416 | False |
| mp-738611 | LiAsH20(C2O)4 | Carbon-family | 70 | 0.277781337 | 0.383 | False |
| mp-3207109 | Li4MnSi2Se7 | Other lithium material | 66 | 0.0 | 2.3577 | True |
| mp-3211616 | Li14FeSiN8 | Other lithium material | 66 | 0.0 | 0.6947 | True |
| mp-760680 | Li2Fe12P7 | Other lithium material | 66 | 0.0 | 0.0 | True |
| mp-1176614 | LiMnP | Other lithium material | 66 | 0.0 | 0.0 | True |
| mp-20049 | LiFeP | Other lithium material | 66 | 0.0 | 0.0 | True |
| mp-3223755 | Li2SiP2 | Other lithium material | 65 | 0.0 | 1.9269 | True |
| mp-3213913 | K3Li2SiP3 | Other lithium material | 65 | 0.0 | 1.9261 | True |

## Modeling Readiness Notes

- Rows available for full numeric target modeling: 24,068
- Stable rows: 4,052
- Unstable rows: 20,905
- The dataset is useful for both classification (`is_stable`) and regression (`energy_above_hull`).
- India columns should be used after prediction for filtering or re-ranking, not for deleting training rows first.

## Suggested Next Modeling Step

Train a simple classical baseline model on the full lithium dataset first.
Use `is_stable` as the first classification target and `energy_above_hull` as
the first regression target. After prediction, apply `india_feasibility_score`
and `india_decision_label` for final filtering and ranking.
