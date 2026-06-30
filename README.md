# Battery Materials DSS QML

Decision Support System for lithium-ion battery compound recommendation using
Materials Project data, India-focused feasibility scoring, XGBoost, and a
simulated QML kernel.

## What This Project Is About

This project recommends **specific lithium battery compound formulas**, not only
broad chemistry families. The final DSS ranks compounds such as `SrLi2SiO4`,
`Li2MnGeS4`, `LiGaSiO4`, and other lithium compounds using:

- material stability signals,
- India feasibility score,
- simulated QML stable probability,
- XGBoost stable probability,
- predicted energy above hull,
- battery-family context.

The output is not direct commercial purchase advice. It is a decision-support
ranking for research, screening, and business discussion.

## What The Project Is Trying To Prove

The project is trying to show a safe student-level idea:

> Battery materials are quantum systems, so simulated QML can be used as the
> primary research signal for future-facing material screening, while XGBoost
> acts as a strong classical correction and benchmark.

We do **not** claim full quantum advantage. XGBoost is still stronger on the
full imbalanced tabular benchmark. The project uses QML as the main DSS
discovery signal, and uses XGBoost when QML is uncertain or when both models
disagree.

## Main Idea

1. Start with a large public Materials Project dataset.
2. Filter lithium-containing compounds.
3. Add India-focused feasibility and battery chemistry context.
4. Train XGBoost as the strong classical benchmark.
5. Build a balanced QML-ready dataset.
6. Tune a simulated QML kernel classifier.
7. Use a QML-primary hybrid score for final compound ranking.
8. Show exact compound recommendations in a presentation-ready notebook.

## Dataset

Main source: [Hugging Face Materials Project snapshot](https://huggingface.co/datasets/xpanceo-team/materials-project)

| Stage | Size |
| --- | ---: |
| Full Materials Project snapshot | 210,579 rows |
| Lithium-only dataset | 24,957 rows |
| India-scored lithium dataset | 24,957 rows x 37 columns |
| Final India battery shortlist | 629 rows |
| Hybrid DSS compound ranking | 629 rows x 22 columns |
| QML-ready balanced dataset | 1,000 rows x 27 columns |

## Final DSS Output

Main output file:

`Battery Materials DSS QML/data/processed/hybrid qml xgboost compound ranking.csv`

The same table is also saved as:

`Battery Materials DSS QML/data/processed/dss compound recommendation ranking.csv`

Top current QML-primary compound candidates:

| Rank | Compound Formula | Material ID | QML Stable Prob. | XGBoost Stable Prob. | Hybrid Score |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | `SrLi2SiO4` | `mp-1191141` | 0.8502 | 0.8252 | 88.4616 |
| 2 | `Li2MnGeS4` | `mp-3268644` | 0.8453 | 0.9033 | 87.7709 |
| 3 | `LiGaSiO4` | `mp-18147` | 0.8516 | 0.8054 | 87.5647 |
| 4 | `SrLi2SnS4` | `mp-3210567` | 0.8670 | 0.8955 | 87.2890 |
| 5 | `Rb2Li2SnS4` | `mp-3205208` | 0.8569 | 0.9042 | 87.2332 |

## Hybrid DSS Logic

The final DSS is **QML-primary**:

- QML gives the first stable-material probability.
- XGBoost gives a classical correction signal.
- If QML is confident, QML receives more ranking weight.
- If QML is uncertain, XGBoost receives more corrective weight.
- If QML and XGBoost strongly disagree, the row is flagged for research review.

Final score uses:

- `hybrid_recommendation_score`
- `hybrid_stable_probability`
- `qml_stable_probability`
- `xgboost_stable_probability`
- `india_feasibility_score`
- `predicted_energy_above_hull_clipped`
- `shortlist_score`
- model disagreement penalty

## Model Results

These two rows are from different evaluation settings, so they should not be
presented as a direct apples-to-apples battle.

| Model | Dataset Setting | Accuracy | Stable Recall | Stable F1 |
| --- | --- | ---: | ---: | ---: |
| XGBoost full classifier | Full lithium tabular benchmark | 0.9091 | 0.7000 | 0.7100 |
| Final repeated-split QML | Balanced QML task, 10 splits | 0.8550 | 0.8800 | 0.8583 |

The useful interpretation is:

- XGBoost is the strong present-day benchmark.
- QML gives stronger stable-class recall and F1 on the balanced QML task.
- The final DSS uses QML first, with XGBoost as a correction layer.

## Why XGBoost

XGBoost was chosen because the main dataset is structured tabular data:
formation energy, band gap, symmetry, element flags, battery-family labels, and
stability-related columns.

XGBoost is suitable because:

- it works well on tabular data,
- it handles non-linear patterns,
- it gives probability outputs for ranking,
- it is a strong classical benchmark,
- it is explainable enough for a student-level project.

## XGBoost Hyperparameters

Classifier target: `is_stable`

| Hyperparameter | Value | Reason |
| --- | ---: | --- |
| `n_estimators` | 250 | Enough trees for stable learning. |
| `max_depth` | 5 | Keeps trees moderately simple. |
| `learning_rate` | 0.05 | Slower, smoother learning. |
| `subsample` | 0.90 | Helps reduce overfitting. |
| `colsample_bytree` | 0.90 | Reduces feature overdependence. |
| `objective` | `binary:logistic` | Stable vs unstable classification. |
| `eval_metric` | `logloss` | Checks probability quality. |
| `random_state` | 42 | Reproducible result. |

These values were chosen as conservative student-level settings: strong enough
for a serious baseline, but still easy to explain.

## Why QML

Battery materials are controlled by atomic and electronic behavior. That is why
quantum computing is relevant to the problem. In this project, QML is used as a
simulated quantum-kernel experiment.

The implementation does not use PennyLane. The quantum kernel is simulated with
NumPy linear algebra and then used with an SVM precomputed kernel. This keeps the
code simple enough to study while still showing the QML idea.

## QML Hyperparameters

Final repeated-split QML setup:

| Hyperparameter | Value |
| --- | --- |
| Features | `formation_energy_per_atom`, `has_o`, `space_group_number`, `theoretical` |
| Qubits | 4 |
| Kernel | `entangled_pi` |
| Angle scale | `pi` |
| Entanglement strength | `pi` |
| Classifier | SVM with precomputed quantum kernel |
| SVM `C` | 5.0 |
| Rows per class | 500 stable + 500 unstable |
| Validation | 10 random train/test splits |

## How QML Hyperparameters Were Found

The project tested combinations instead of guessing manually:

- feature counts: `4`, `6`, `8`, `10`
- angle scales: `pi/2`, `pi`, `2pi`
- SVM `C`: `0.1`, `0.5`, `1.0`, `2.0`, `5.0`, `10.0`
- total initial tuning experiments: `72`
- validation method: 4-fold cross-validation

The best improved QML setup was then checked across 10 random balanced splits.

## Important Files

| File | Purpose |
| --- | --- |
| `Battery Materials DSS QML/Battery Materials DSS QML Main Presentation.ipynb` | Main presentation notebook with outputs in every cell. |
| `Battery Materials DSS QML/scripts/create_dss_recommendation_ranking.py` | Builds the QML-primary hybrid DSS table. |
| `Battery Materials DSS QML/data/processed/hybrid qml xgboost compound ranking.csv` | Main hybrid recommendation table. |
| `Battery Materials DSS QML/data/metadata/dss_recommendation_summary.md` | Explanation of DSS ranking logic. |
| `Battery Materials DSS QML/data/processed/qml circuit diagram.png` | QML circuit diagram for presentation. |

## How To Run

```bash
python3 -m pip install -r requirements.txt
cd "Battery Materials DSS QML"
python3 scripts/create_dss_recommendation_ranking.py
python3 scripts/create_main_presentation_notebook.py
```

Full pipeline scripts are inside `Battery Materials DSS QML/scripts/`.
