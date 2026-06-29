# Improved QML Step 06: Quantum Kernel Alignment

Generated on: 2026-06-28

## Purpose

The earlier improved-QML section used Random Forest feature importance and PCA.
That is useful, but PCA is not quantum-aware. This step tests feature groups by
measuring how well each quantum kernel aligns with the stable/unstable target.

In simple terms:

- A good kernel should give similar values to materials with the same label.
- A good kernel should give different values to materials with different labels.
- Kernel-target alignment gives a score for that behavior before final testing.

## Leakage Control

- Alignment was calculated only on the train-validation split.
- The test split was used only once after the best alignment candidate was
  selected.
- `energy_above_hull`, `india_feasibility_score`, and `india_decision_label`
  were not used as classifier features.

## Feature Sets Tested

| feature_set_name | feature_count | feature_names | reason |
| --- | --- | --- | --- |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | Top 4 features from Random Forest importance. |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | Top 6 features from Random Forest importance. |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | Top 8 features from Random Forest importance. |
| physics_core | 6 | space_group_number;band_gap;formation_energy_per_atom;number_of_elements;is_metal;theoretical | Crystal and electronic-property features. |
| chemistry_core | 8 | has_o;has_fe;has_p;has_mn;has_co;has_ni;has_ti;has_s | Common cathode and sulfide chemistry indicators. |
| mixed_physics_chemistry | 8 | space_group_number;band_gap;formation_energy_per_atom;number_of_elements;has_fe;has_p;has_mn;has_s | Small mixed set of physics and chemistry features. |
| crystal_system_only | 7 | crystal_system_Cubic;crystal_system_Hexagonal;crystal_system_Monoclinic;crystal_system_Orthorhombic;crystal_system_Tetragonal;crystal_system_Triclinic;crystal_system_Trigonal | One-hot crystal-system features. |
| battery_family_only | 8 | battery_family_LFP-family;battery_family_LMFP-family;battery_family_LMO-family;battery_family_LTO-family;battery_family_Li-S or sulfide-family;battery_family_Silicon-family;battery_family_Carbon-family;battery_family_Other lithium material | One-hot battery-family features. |

## Alignment Search

- Feature sets tested: 8
- Angle scales tested: pi/2, pi, 2pi
- Kernel types tested: product, entangled_pi_over_2, entangled_pi
- Alignment candidates scored: 72
- Top alignment candidates cross-validated: 12
- SVM C values cross-validated: [0.5, 1.0, 2.0, 5.0]

## Top Kernel-Target Alignment Scores

| feature_set_name | feature_count | feature_names | kernel_name | entanglement_strength | angle_scale | angle_scale_value | quantum_state_size | kernel_target_alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 16 | 0.3959 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 16 | 0.3956 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | product | 0 | pi_over_2 | 1.5708 | 16 | 0.3949 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | product | 0 | pi | 3.1416 | 16 | 0.3858 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 16 | 0.3829 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi | 3.1416 | pi | 3.1416 | 16 | 0.3785 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 64 | 0.3549 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 64 | 0.3542 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | product | 0 | pi_over_2 | 1.5708 | 64 | 0.3534 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 256 | 0.3132 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 256 | 0.3130 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | product | 0 | pi_over_2 | 1.5708 | 256 | 0.3123 |
| chemistry_core | 8 | has_o;has_fe;has_p;has_mn;has_co;has_ni;has_ti;has_s | product | 0 | pi_over_2 | 1.5708 | 256 | 0.2886 |
| chemistry_core | 8 | has_o;has_fe;has_p;has_mn;has_co;has_ni;has_ti;has_s | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 256 | 0.2886 |
| chemistry_core | 8 | has_o;has_fe;has_p;has_mn;has_co;has_ni;has_ti;has_s | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 256 | 0.2886 |

## Best Cross-Validated Alignment Model

| feature_set_name | feature_count | feature_names | kernel_name | entanglement_strength | angle_scale | angle_scale_value | quantum_state_size | kernel_target_alignment | c_value | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi | 3.1416 | pi | 3.1416 | 16 | 0.3785 | 5 | 0.8538 | 0.8432 | 0.8725 | 0.8568 |

## Top Cross-Validation Results

| feature_set_name | feature_count | feature_names | kernel_name | entanglement_strength | angle_scale | angle_scale_value | quantum_state_size | kernel_target_alignment | c_value | cv_accuracy | cv_stable_precision | cv_stable_recall | cv_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi | 3.1416 | pi | 3.1416 | 16 | 0.3785 | 5 | 0.8538 | 0.8432 | 0.8725 | 0.8568 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 16 | 0.3829 | 5 | 0.8512 | 0.8410 | 0.8700 | 0.8544 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | product | 0 | pi | 3.1416 | 16 | 0.3858 | 5 | 0.8500 | 0.8388 | 0.8700 | 0.8534 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 64 | 0.3549 | 5 | 0.8462 | 0.8271 | 0.8800 | 0.8519 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 64 | 0.3549 | 2 | 0.8425 | 0.8163 | 0.8875 | 0.8498 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | product | 0 | pi | 3.1416 | 16 | 0.3858 | 2 | 0.8450 | 0.8301 | 0.8725 | 0.8497 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi_over_2 | 1.5708 | pi | 3.1416 | 16 | 0.3829 | 2 | 0.8450 | 0.8301 | 0.8725 | 0.8497 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | entangled_pi | 3.1416 | pi | 3.1416 | 16 | 0.3785 | 2 | 0.8450 | 0.8301 | 0.8725 | 0.8497 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 64 | 0.3542 | 5 | 0.8450 | 0.8296 | 0.8725 | 0.8496 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 256 | 0.3132 | 0.5000 | 0.8425 | 0.8213 | 0.8800 | 0.8487 |
| rf_top_6 | 6 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 64 | 0.3549 | 1 | 0.8412 | 0.8159 | 0.8850 | 0.8484 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | entangled_pi | 3.1416 | pi_over_2 | 1.5708 | 256 | 0.3132 | 2 | 0.8425 | 0.8228 | 0.8775 | 0.8483 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | entangled_pi_over_2 | 1.5708 | pi_over_2 | 1.5708 | 256 | 0.3130 | 0.5000 | 0.8412 | 0.8210 | 0.8775 | 0.8473 |
| rf_top_8 | 8 | formation_energy_per_atom;has_o;space_group_number;theoretical;band_gap;battery_family_Other lithium material;crystal_system_Triclinic;has_mn | product | 0 | pi_over_2 | 1.5708 | 256 | 0.3123 | 0.5000 | 0.8412 | 0.8210 | 0.8775 | 0.8473 |
| rf_top_4 | 4 | formation_energy_per_atom;has_o;space_group_number;theoretical | product | 0 | pi | 3.1416 | 16 | 0.3858 | 1 | 0.8412 | 0.8206 | 0.8775 | 0.8472 |

## Test Result

| feature_set_name | feature_count | kernel_name | angle_scale | c_value | kernel_target_alignment | quantum_state_size | test_accuracy | test_stable_precision | test_stable_recall | test_stable_f1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rf_top_4 | 4 | entangled_pi | pi | 5 | 0.3785 | 16 | 0.8200 | 0.7857 | 0.8800 | 0.8302 |

## Confusion Matrix

| actual_class | predicted_unstable_0 | predicted_stable_1 |
| --- | --- | --- |
| unstable_0 | 76 | 24 |
| stable_1 | 12 | 88 |

## Classification Report

```text
              precision    recall  f1-score   support

    unstable       0.86      0.76      0.81       100
      stable       0.79      0.88      0.83       100

    accuracy                           0.82       200
   macro avg       0.82      0.82      0.82       200
weighted avg       0.82      0.82      0.82       200

```

## Prediction Output

`data/processed/improved qml alignment predictions.csv`

Rows saved: 200
