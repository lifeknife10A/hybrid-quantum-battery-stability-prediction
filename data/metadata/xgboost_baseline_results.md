# XGBoost Baseline Results

Input file: `data/processed/lithium india scored.csv`

Prediction output: `data/processed/xgboost predictions with india scores.csv`

## Problem

Train on all lithium materials first, then use India feasibility columns after
prediction for filtering and ranking.

## Dataset

- Rows used for classification: 24,957
- Rows used for regression: 24,068
- Feature columns after one-hot encoding: 42
- Test size: 0.2
- Random state: 42

## Training Features

The model uses formula-derived, crystal, and basic property columns. It does not
train on `india_feasibility_score`, `india_decision_label`, `energy_above_hull`
for classification, or `is_stable` for regression.

Base features:

- `space_group_number`
- `band_gap`
- `is_metal`
- `theoretical`
- `deprecated`
- `number_of_elements`
- `has_o`
- `has_fe`
- `has_p`
- `has_mn`
- `has_co`
- `has_ni`
- `has_ti`
- `has_c`
- `has_si`
- `has_s`
- `has_al`
- `has_la`
- `has_zr`
- `has_f`
- `has_cu`
- `has_high_caution_element`
- `crystal_system`
- `battery_family`

## Classification Target: `is_stable`

- Model: `XGBClassifier`
- Accuracy: 0.9091

```text
              precision    recall  f1-score   support

    unstable       0.94      0.95      0.95      4182
      stable       0.73      0.70      0.71       810

    accuracy                           0.91      4992
   macro avg       0.84      0.82      0.83      4992
weighted avg       0.91      0.91      0.91      4992

```

## Regression Target: `energy_above_hull`

- Model: `XGBRegressor`
- Mean absolute error: 0.1005
- Root mean squared error: 0.3221
- R2 score: 0.3685

## Top Classifier Features

| feature | importance |
| --- | --- |
| has_o | 0.4500940442085266 |
| theoretical | 0.07527858018875122 |
| has_f | 0.06175295263528824 |
| number_of_elements | 0.045424267649650574 |
| battery_family_Other lithium material | 0.0340118482708931 |
| is_metal | 0.028371715918183327 |
| has_fe | 0.024898916482925415 |
| has_p | 0.019314195960760117 |
| space_group_number | 0.015507164411246777 |
| has_si | 0.015254606492817402 |
| crystal_system_Trigonal | 0.014527388848364353 |
| crystal_system_Orthorhombic | 0.014342350885272026 |
| band_gap | 0.014177258126437664 |
| has_ni | 0.012385653331875801 |
| battery_family_Li-S or sulfide-family | 0.012268086895346642 |

## Top Regressor Features

| feature | importance |
| --- | --- |
| battery_family_Silicon-family | 0.12254201620817184 |
| has_p | 0.08141078054904938 |
| crystal_system_Orthorhombic | 0.07476631551980972 |
| space_group_number | 0.06761787831783295 |
| crystal_system_Triclinic | 0.06155180186033249 |
| has_mn | 0.04273314028978348 |
| has_f | 0.0384957529604435 |
| is_metal | 0.03628840669989586 |
| has_si | 0.03553098067641258 |
| has_fe | 0.03478864207863808 |
| band_gap | 0.033638160675764084 |
| number_of_elements | 0.03127342835068703 |
| has_o | 0.028235187754034996 |
| battery_family_Li-S or sulfide-family | 0.02608807571232319 |
| battery_family_Other lithium material | 0.02567315846681595 |

## Top India-Friendly Predictions

| material_id | formula | battery_family | india_decision_label | india_feasibility_score | predicted_stable_probability | predicted_energy_above_hull | final_recommendation_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mp-3214455 | Sr2LiHC3 | Carbon-family | Recommend | 95 | 0.8286640644073486 | 0.07124193012714386 | 87.72 |
| mp-3268644 | Li2MnGeS4 | Li-S or sulfide-family | Research Candidate | 81 | 0.9033248424530029 | 0.000864186673425138 | 86.6 |
| mp-3213977 | LiCrSnS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.9049679636955261 | 0.017541823908686638 | 85.5 |
| mp-3209528 | Cs2Li2SnS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.9046651721000671 | -0.025410642847418785 | 85.48 |
| mp-3205208 | Rb2Li2SnS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.9042041897773743 | -0.02514760196208954 | 85.45 |
| mp-3253343 | KLiNpS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.9041699171066284 | 0.0023009912110865116 | 85.45 |
| mp-3209691 | K2Li2SnS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.9002243876457214 | 0.0036523761227726936 | 85.21 |
| mp-3215854 | Cs2LiTaS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.8974965810775757 | 0.0018885508179664612 | 85.05 |
| mp-1210804 | Li2ZnGeS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.8956897854804993 | -3.821245627477765e-05 | 84.94 |
| mp-3210567 | SrLi2SnS4 | Li-S or sulfide-family | Research Candidate | 78 | 0.8955100774765015 | -0.010870179161429405 | 84.93 |
| mp-3253559 | KLiThS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8945697546005249 | -0.005353656597435474 | 84.87 |
| mp-556649 | Li4Ga3Si3BrO12 | Silicon-family | Research Candidate | 87 | 0.8343666791915894 | 0.021773770451545715 | 84.86 |
| mp-3244683 | CsLiThS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8938699960708618 | -0.005353656597435474 | 84.83 |
| mp-3246030 | RbLiThS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8938699960708618 | -0.005353656597435474 | 84.83 |
| mp-3210350 | CsLi3Lu2S5 | Li-S or sulfide-family | Research Candidate | 78 | 0.8933629989624023 | -0.0050906166434288025 | 84.8 |
| mp-3249913 | BaLiPrS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8919712901115417 | -0.004582545254379511 | 84.72 |
| mp-3252745 | BaLiNdS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8919712901115417 | -0.004582545254379511 | 84.72 |
| mp-3245278 | BaLiHoS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8919712901115417 | -0.004582545254379511 | 84.72 |
| mp-3246559 | BaLiDyS3 | Li-S or sulfide-family | Research Candidate | 78 | 0.8919712901115417 | -0.005079491529613733 | 84.72 |
| mp-557112 | Li4Ga3Si3IO12 | Silicon-family | Research Candidate | 87 | 0.8313344120979309 | 0.0257889274507761 | 84.68 |

## Notes

- This is a baseline model, not the final model.
- The India columns are applied after prediction so the model still learns from
  all lithium families.
- The output file can be used to inspect predicted stable materials and then
  shortlist India-friendly candidates.
