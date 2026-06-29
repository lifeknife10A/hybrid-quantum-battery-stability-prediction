# DSS Recommendation Summary

Generated on: 2026-06-29

## Purpose

This step frames the project as a Decision Support System. The goal is to help a
business user, EV owner, or battery decision-maker compare material families and
material candidates using clear ranking parameters.

## Important Clarification

This is not direct commercial purchase advice for a branded battery product.
The dataset ranks lithium material candidates and battery-material families.
The DSS output should support human decision-making, not replace testing,
safety certification, supplier checks, or cost analysis.

## DSS Output Files

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

The family ranking is a decision-support ranking, not only a raw ML-score
ranking. For example, LFP is ranked first because it is the most practical
near-term business direction for Indian EV and battery use, even when some
individual material rows have conservative model probabilities. Li-S and
Silicon remain important, but they are marked more as R&D directions than
immediate purchase choices.

## Battery Family Ranking

| dss_rank | dss_family_rank | battery_family | dss_decision | shortlist_rows | average_shortlist_score | average_india_feasibility_score | average_predicted_stable_probability | median_predicted_energy_above_hull | top_material_id | top_formula | short_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | LFP-family | Best near-term purchase direction | 464 | 45.2782 | 96.0259 | 0.0148 | 0.0487 | mp-19430 | Li3Fe2(PO4)3 | India-friendly iron phosphate chemistry; avoids nickel and cobalt. |
| 2 | 2 | LMFP-family | Good pilot and next-generation option | 48 | 45.1400 | 94.2083 | 0.0094 | 0.0398 | mp-1221200 | Na4Li4MnFe3P4(O4F)4 | LFP-like family with manganese; useful for improving performance. |
| 3 | 3 | LMO-family | Selective low-cost option | 4 | 74.9500 | 89.2500 | 0.6783 | 0.0288 | mp-581301 | Li2MgMn3O8 | Manganese-based family; useful when cost matters, but needs checks. |
| 4 | 4 | Carbon-family | Useful anode/support material | 5 | 72.9580 | 94.8000 | 0.7261 | 0.0647 | mp-3247282 | LiEr4MnC8 | Practical supporting material, but not a complete battery-cell choice. |
| 5 | 5 | Silicon-family | R&D anode improvement option | 17 | 80.6224 | 87.0000 | 0.7376 | 0.0151 | mp-1191141 | SrLi2SiO4 | High-potential anode direction; better for blended or future designs. |
| 6 | 6 | Li-S or sulfide-family | Long-term R&D option | 91 | 81.3991 | 78.0220 | 0.7928 | 0.0034 | mp-3268644 | Li2MnGeS4 | High-potential chemistry, but less direct for immediate purchase. |

## Top Material Recommendations

| dss_rank | material_id | formula | battery_family | dss_decision | shortlist_score | india_feasibility_score | predicted_stable_probability | predicted_energy_above_hull_clipped | band_gap | is_stable | shortlist_rule_type | short_conceptual_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | mp-19430 | Li3Fe2(PO4)3 | LFP-family | Best near-term purchase direction | 59.5200 | 98 | 0.1677 | 0.0116 | 2.4773 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0116; stable probability 0.1677. |
| 2 | mp-554093 | Li9Fe3P8O29 | LFP-family | Best near-term purchase direction | 59.1000 | 98 | 0.1472 | 0.0091 | 2.5479 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0091; stable probability 0.1472. |
| 3 | mp-1195117 | LiFeP2(HO3)2 | LFP-family | Best near-term purchase direction | 57.4200 | 94 | 0.1729 | 0.0163 | 2.7734 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 94; predicted hull 0.0163; stable probability 0.1729. |
| 4 | mp-19294 | LiFeP2O7 | LFP-family | Best near-term purchase direction | 57.2600 | 100 | 0.2222 | 0.0387 | 1.7443 | True | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 100; predicted hull 0.0387; stable probability 0.2222. |
| 5 | mp-19017 | LiFePO4 | LFP-family | Best near-term purchase direction | 56.4800 | 100 | 0.1381 | 0.0237 | 3.9224 | True | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 100; predicted hull 0.0237; stable probability 0.1381. |
| 6 | mp-26985 | Li2Fe3(P2O7)2 | LFP-family | Best near-term purchase direction | 56.3900 | 98 | 0.1154 | 0.0155 | 3.9224 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0155; stable probability 0.1154. |
| 7 | mp-1198378 | NaLiFePO4F | LFP-family | Best near-term purchase direction | 56.2200 | 94 | 0.1673 | 0.0210 | 4.3042 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 94; predicted hull 0.0210; stable probability 0.1673. |
| 8 | mp-6373 | Li3Fe2(PO4)3 | LFP-family | Best near-term purchase direction | 55.5000 | 98 | 0.1317 | 0.0236 | 2.4096 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0236; stable probability 0.1317. |
| 9 | mp-25993 | Li3Fe2(PO4)3 | LFP-family | Best near-term purchase direction | 55.3200 | 98 | 0.1264 | 0.0233 | 2.6074 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0233; stable probability 0.1264. |
| 10 | mp-504179 | LiFe(PO3)3 | LFP-family | Best near-term purchase direction | 54.8800 | 98 | 0.1321 | 0.0269 | 4.1851 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0269; stable probability 0.1321. |
| 11 | mp-768618 | Li3Fe2P2(CO7)2 | LFP-family | Best near-term purchase direction | 54.4700 | 98 | 0.0037 | 0.0000 | 0.0000 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0000; stable probability 0.0037. |
| 12 | mp-768667 | Li5Fe2P2(CO7)2 | LFP-family | Best near-term purchase direction | 54.4700 | 98 | 0.0037 | 0.0000 | 0.0000 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0000; stable probability 0.0037. |
| 13 | mp-756197 | Li3Fe2P2(CO7)2 | LFP-family | Best near-term purchase direction | 54.4100 | 98 | 0.0024 | 0.0000 | 0.0000 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 98; predicted hull 0.0000; stable probability 0.0024. |
| 14 | mp-1177545 | Li3VFeP2(O4F)2 | LFP-family | Best near-term purchase direction | 53.8600 | 100 | 0.0898 | 0.0259 | 2.4464 | True | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 100; predicted hull 0.0259; stable probability 0.0898. |
| 15 | mp-25406 | LiFePCO7 | LFP-family | Best near-term purchase direction | 53.7700 | 96 | 0.0037 | 0.0000 | 0.0000 | False | Benchmark family exception | India-friendly iron phosphate chemistry; avoids nickel and cobalt. India score 96; predicted hull 0.0000; stable probability 0.0037. |

## How To Explain In Presentation

This project is a DSS because it does not only train a model. It converts model
outputs and India-focused rules into a ranked decision table. A user can see
which family is more practical, which material is ranked higher, and which
parameters caused the rank.
