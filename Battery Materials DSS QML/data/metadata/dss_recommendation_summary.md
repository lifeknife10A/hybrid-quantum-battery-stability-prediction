# DSS Recommendation Summary

Generated on: 2026-06-30

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

| dss_rank | formula | material_id | battery_family | dss_decision | hybrid_recommendation_score | hybrid_stable_probability | qml_stable_probability | xgboost_stable_probability | qml_weight | xgboost_correction_weight | qml_confidence_band | hybrid_decision_role | model_disagreement | qml_probability_std | shortlist_score | india_feasibility_score | predicted_energy_above_hull_clipped | band_gap | is_stable | shortlist_rule_type | short_conceptual_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SrLi2SiO4 | mp-1191141 | Silicon-family | R&D anode improvement option | 88.4616 | 0.8401 | 0.8502 | 0.8252 | 0.5952 | 0.4048 | QML confident stable | QML-led; XGBoost agrees | False | 0.0408 | 87.5800 | 87 | 0.0000 | 4.6041 | True | Strict model shortlist | High-potential anode direction; better for blended or future designs. India score 87; QML probability 0.8502; XGBoost probability 0.8252; hybrid probability 0.8401; predicted hull 0.0000. |
| 2 | Li2MnGeS4 | mp-3268644 | Li-S or sulfide-family | Long-term R&D option | 87.7709 | 0.8690 | 0.8453 | 0.9033 | 0.5917 | 0.4083 | QML confident stable | QML-led; XGBoost agrees | False | 0.0291 | 88.8300 | 81 | 0.0009 | 1.9728 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 81; QML probability 0.8453; XGBoost probability 0.9033; hybrid probability 0.8690; predicted hull 0.0009. |
| 3 | LiGaSiO4 | mp-18147 | Silicon-family | R&D anode improvement option | 87.5647 | 0.8329 | 0.8516 | 0.8054 | 0.5961 | 0.4039 | QML confident stable | QML-led; XGBoost agrees | False | 0.0391 | 86.2200 | 87 | 0.0024 | 4.2293 | True | Strict model shortlist | High-potential anode direction; better for blended or future designs. India score 87; QML probability 0.8516; XGBoost probability 0.8054; hybrid probability 0.8329; predicted hull 0.0024. |
| 4 | SrLi2SnS4 | mp-3210567 | Li-S or sulfide-family | Long-term R&D option | 87.2890 | 0.8782 | 0.8670 | 0.8955 | 0.6069 | 0.3931 | QML confident stable | QML-led; XGBoost agrees | False | 0.0188 | 87.6000 | 78 | 0.0000 | 3.0972 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8670; XGBoost probability 0.8955; hybrid probability 0.8782; predicted hull 0.0000. |
| 5 | Rb2Li2SnS4 | mp-3205208 | Li-S or sulfide-family | Long-term R&D option | 87.2332 | 0.8759 | 0.8569 | 0.9042 | 0.5999 | 0.4001 | QML confident stable | QML-led; XGBoost agrees | False | 0.0385 | 87.9900 | 78 | 0.0000 | 3.0399 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8569; XGBoost probability 0.9042; hybrid probability 0.8759; predicted hull 0.0000. |
| 6 | Cs2Li2SnS4 | mp-3209528 | Li-S or sulfide-family | Long-term R&D option | 87.2222 | 0.8755 | 0.8560 | 0.9047 | 0.5992 | 0.4008 | QML confident stable | QML-led; XGBoost agrees | False | 0.0393 | 88.0100 | 78 | 0.0000 | 3.2409 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8560; XGBoost probability 0.9047; hybrid probability 0.8755; predicted hull 0.0000. |
| 7 | BaLi2SnS4 | mp-3211122 | Li-S or sulfide-family | Long-term R&D option | 87.1720 | 0.8760 | 0.8670 | 0.8898 | 0.6069 | 0.3931 | QML confident stable | QML-led; XGBoost agrees | False | 0.0188 | 87.3400 | 78 | 0.0000 | 3.0828 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8670; XGBoost probability 0.8898; hybrid probability 0.8760; predicted hull 0.0000. |
| 8 | Li2ZnGeS4 | mp-1210804 | Li-S or sulfide-family | Long-term R&D option | 86.7154 | 0.8639 | 0.8417 | 0.8957 | 0.5892 | 0.4108 | QML confident stable | QML-led; XGBoost agrees | False | 0.0309 | 87.6100 | 78 | 0.0000 | 2.1846 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8417; XGBoost probability 0.8957; hybrid probability 0.8639; predicted hull 0.0000. |
| 9 | Rb2Li2TiS4 | mp-3215312 | Li-S or sulfide-family | Long-term R&D option | 86.5092 | 0.8503 | 0.8690 | 0.8213 | 0.6083 | 0.3917 | QML confident stable | QML-led; XGBoost agrees | False | 0.0276 | 84.9600 | 80 | 0.0000 | 2.6367 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 80; QML probability 0.8690; XGBoost probability 0.8213; hybrid probability 0.8503; predicted hull 0.0000. |
| 10 | K2Li2TiS4 | mp-3205916 | Li-S or sulfide-family | Long-term R&D option | 86.5061 | 0.8503 | 0.8694 | 0.8207 | 0.6086 | 0.3914 | QML confident stable | QML-led; XGBoost agrees | False | 0.0274 | 84.9300 | 80 | 0.0000 | 2.5669 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 80; QML probability 0.8694; XGBoost probability 0.8207; hybrid probability 0.8503; predicted hull 0.0000. |
| 11 | Li2MgSiS4 | mp-3203753 | Li-S or sulfide-family | Long-term R&D option | 86.4226 | 0.8426 | 0.8220 | 0.8706 | 0.5754 | 0.4246 | QML confident stable | QML-led; XGBoost agrees | False | 0.0384 | 87.1800 | 80 | 0.0000 | 3.9328 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 80; QML probability 0.8220; XGBoost probability 0.8706; hybrid probability 0.8426; predicted hull 0.0000. |
| 12 | Cs2LiTaS4 | mp-3215854 | Li-S or sulfide-family | Long-term R&D option | 86.2527 | 0.8625 | 0.8378 | 0.8975 | 0.5865 | 0.4135 | QML confident stable | QML-led; XGBoost agrees | False | 0.0500 | 87.3100 | 78 | 0.0019 | 3.0918 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8378; XGBoost probability 0.8975; hybrid probability 0.8625; predicted hull 0.0019. |
| 13 | NaLiZnS2 | mp-1220972 | Li-S or sulfide-family | Long-term R&D option | 86.0102 | 0.8531 | 0.8650 | 0.8348 | 0.6055 | 0.3945 | QML confident stable | QML-led; XGBoost agrees | False | 0.0180 | 84.8700 | 78 | 0.0000 | 1.8298 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8650; XGBoost probability 0.8348; hybrid probability 0.8531; predicted hull 0.0000. |
| 14 | CsLi2TaS4 | mp-3213228 | Li-S or sulfide-family | Long-term R&D option | 85.8956 | 0.8448 | 0.8164 | 0.8828 | 0.5715 | 0.4285 | QML confident stable | QML-led; XGBoost agrees | False | 0.0437 | 87.0200 | 78 | 0.0000 | 3.1835 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8164; XGBoost probability 0.8828; hybrid probability 0.8448; predicted hull 0.0000. |
| 15 | K2Li2SnS4 | mp-3209691 | Li-S or sulfide-family | Long-term R&D option | 85.5976 | 0.8555 | 0.8226 | 0.9002 | 0.5758 | 0.4242 | QML confident stable | QML-led; XGBoost agrees | False | 0.0357 | 87.0800 | 78 | 0.0037 | 3.0404 | True | Strict model shortlist | High-potential chemistry, but less direct for immediate purchase. India score 78; QML probability 0.8226; XGBoost probability 0.9002; hybrid probability 0.8555; predicted hull 0.0037. |

## Supporting Battery Family Context

| dss_rank | dss_family_rank | battery_family | dss_decision | shortlist_rows | average_hybrid_recommendation_score | average_hybrid_stable_probability | average_qml_stable_probability | average_xgboost_stable_probability | average_shortlist_score | average_india_feasibility_score | average_predicted_stable_probability | median_predicted_energy_above_hull | top_material_id | top_formula | short_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | Silicon-family | R&D anode improvement option | 17 | 83.1593 | 0.8004 | 0.8436 | 0.7376 | 80.6224 | 87.0000 | 0.7376 | 0.0151 | mp-1191141 | SrLi2SiO4 | High-potential anode direction; better for blended or future designs. |
| 2 | 6 | Li-S or sulfide-family | Long-term R&D option | 91 | 81.8842 | 0.8022 | 0.8037 | 0.7928 | 81.3991 | 78.0220 | 0.7928 | 0.0034 | mp-3268644 | Li2MnGeS4 | High-potential chemistry, but less direct for immediate purchase. |
| 3 | 3 | LMO-family | Selective low-cost option | 4 | 77.7268 | 0.7567 | 0.8153 | 0.6783 | 74.9500 | 89.2500 | 0.6783 | 0.0288 | mp-581301 | Li2MgMn3O8 | Manganese-based family; useful when cost matters, but needs checks. |
| 4 | 4 | Carbon-family | Useful anode/support material | 5 | 70.6455 | 0.7201 | 0.7128 | 0.7261 | 72.9580 | 94.8000 | 0.7261 | 0.0647 | mp-3247282 | LiEr4MnC8 | Practical supporting material, but not a complete battery-cell choice. |
| 5 | 1 | LFP-family | Best near-term purchase direction | 464 | 48.3320 | 0.1033 | 0.1626 | 0.0148 | 45.2782 | 96.0259 | 0.0148 | 0.0487 | mp-554093 | Li9Fe3P8O29 | India-friendly iron phosphate chemistry; avoids nickel and cobalt. |
| 6 | 2 | LMFP-family | Good pilot and next-generation option | 48 | 48.0997 | 0.0894 | 0.1428 | 0.0094 | 45.1400 | 94.2083 | 0.0094 | 0.0398 | mp-1221200 | Na4Li4MnFe3P4(O4F)4 | LFP-like family with manganese; useful for improving performance. |

## How To Explain In Presentation

This project is a DSS because it does not only train a model. It converts model
outputs and India-focused rules into a ranked compound decision table. The user
can see the exact formula, QML probability, XGBoost probability, hybrid
probability, India feasibility score, and short conceptual reason.
