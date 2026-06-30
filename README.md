# Battery Materials DSS QML

Decision Support System for lithium-ion battery compound recommendation using
Materials Project data, XGBoost, India-focused feasibility scoring, and
simulated Quantum Machine Learning.

## What This Project Is About

This project recommends **specific lithium battery compound formulas**, not
only broad chemistry families. The final DSS output ranks compounds such as
`Li3Fe2(PO4)3`, `LiFePO4`, and related lithium compounds using material
stability, India feasibility, and model predictions.

The project is designed for a student-level quantum/materials hackathon
presentation: practical enough to defend, but still connected to quantum
computing because battery materials are quantum systems at the atomic and
electronic level.

## What The Project Is Trying To Prove

The project does **not** claim that QML already beats XGBoost on the full
dataset. The claim is more careful:

> A practical DSS can use strong classical ML today, while using simulated QML
> as a future-facing experiment for quantum-assisted materials discovery.

The strongest result is that XGBoost gives better overall accuracy, while the
final QML experiment gives stronger stable-class recall and F1 on the balanced
QML task.

| Model | Accuracy | Stable Recall | Stable F1 |
| --- | ---: | ---: | ---: |
| XGBoost full classifier | 0.9091 | 0.7000 | 0.7100 |
| Final repeated-split QML | 0.8550 | 0.8800 | 0.8583 |

## Main Idea

1. Start with a large public materials dataset.
2. Filter lithium-containing compounds.
3. Add India-focused feasibility and battery chemistry context.
4. Train XGBoost as the strong present-day classical benchmark.
5. Build a QML-ready balanced dataset.
6. Test simulated QML as a quantum-future comparison.
7. Rank exact lithium compound formulas for DSS-style decision support.

## Dataset

Main source: [Hugging Face Materials Project snapshot](https://huggingface.co/datasets/xpanceo-team/materials-project)

| Stage | Size |
| --- | ---: |
| Full Materials Project snapshot | 210,579 rows |
| Lithium-only dataset | 24,957 rows |
| India-scored lithium dataset | 24,957 rows x 37 columns |
| Final India battery shortlist | 629 rows |
| DSS compound recommendation ranking | 629 rows |
| QML-ready balanced dataset | 1,000 rows x 27 columns |

## What The Project Provides

- A compound-level recommendation table:
  `Battery Materials DSS QML/data/processed/dss compound recommendation ranking.csv`
- A presentation notebook with saved outputs:
  `Battery Materials DSS QML/Battery Materials DSS QML Main Presentation.ipynb`
- XGBoost classification and regression baselines.
- Simulated QML experiments with tuning and repeated-split validation.
- A QML circuit diagram for explaining the quantum feature map.
- DSS reports explaining why compounds were ranked.

Top current compound recommendations:

| Rank | Compound Formula | Material ID | Context |
| --- | --- | --- | --- |
| 1 | `Li3Fe2(PO4)3` | `mp-19430` | LFP chemistry context |
| 2 | `Li9Fe3P8O29` | `mp-554093` | LFP chemistry context |
| 3 | `LiFeP2(HO3)2` | `mp-1195117` | LFP chemistry context |
| 4 | `LiFeP2O7` | `mp-19294` | LFP chemistry context |
| 5 | `LiFePO4` | `mp-19017` | LFP chemistry context |

## Why XGBoost

XGBoost was chosen because the main dataset is structured tabular data:
numbers, boolean element flags, crystal-system labels, battery-family context,
band gap, and stability-related columns.

XGBoost is suitable here because:

- it handles tabular features well,
- it models non-linear relationships better than simple linear models,
- it is strong enough to act as a serious classical benchmark,
- it provides reliable probability outputs for ranking compounds,
- it is easier to explain and defend than a large neural network for this
  student-level project.

## XGBoost Hyperparameters

Classifier target: `is_stable`

| Hyperparameter | Value | Why |
| --- | ---: | --- |
| `n_estimators` | 250 | Enough trees for stable learning without making the model too large. |
| `max_depth` | 5 | Keeps each tree moderately simple and reduces overfitting risk. |
| `learning_rate` | 0.05 | Slower learning for smoother improvement. |
| `subsample` | 0.90 | Uses 90% of rows per boosting step for better generalization. |
| `colsample_bytree` | 0.90 | Uses 90% of features per tree to reduce feature overdependence. |
| `objective` | `binary:logistic` | Stable vs unstable is a binary classification problem. |
| `eval_metric` | `logloss` | Measures probability quality for binary classification. |
| `test_size` | 0.20 | Standard 80/20 train-test split. |
| `random_state` | 42 | Reproducible results. |

Regressor target: `energy_above_hull`

| Hyperparameter | Value |
| --- | ---: |
| `n_estimators` | 300 |
| `max_depth` | 5 |
| `learning_rate` | 0.05 |
| `subsample` | 0.90 |
| `colsample_bytree` | 0.90 |
| `objective` | `reg:squarederror` |

These values were chosen as conservative, explainable defaults: not too shallow,
not too large, and suitable for a student project with reproducible evaluation.

## Why QML

The QML part is included because battery materials are quantum systems at the
atomic scale. Classical ML is useful today, but quantum feature spaces may
become useful as quantum hardware and QML methods improve.

In this project, QML is used as a **simulated quantum-kernel experiment**, not
as a claim of finished quantum advantage.

## QML Hyperparameters

Final repeated-split QML setup:

| Hyperparameter | Value |
| --- | --- |
| Features | `formation_energy_per_atom`, `has_o`, `space_group_number`, `theoretical` |
| Qubits | 4 |
| Kernel | `entangled_pi` |
| Angle scale | `pi` |
| Classifier | SVM with precomputed quantum kernel |
| SVM `C` | 5.0 |
| Rows per class | 500 stable + 500 unstable |
| Train/test split | 80/20 |
| Validation | 10 random train/test splits |

## How The QML Hyperparameters Were Found

The QML settings were selected by experimentation, not guessed manually.

Initial tuning tested:

- feature counts: `4`, `6`, `8`, `10`
- angle scales: `pi/2`, `pi`, `2pi`
- SVM `C`: `0.1`, `0.5`, `1.0`, `2.0`, `5.0`, `10.0`
- total tuning experiments: `72`
- validation method: 4-fold cross-validation

Then the best improved QML setup was checked across 10 random balanced splits.
This was done so the result would not depend on only one lucky train/test split.

## Final Interpretation

XGBoost is the stronger production-style model for the full tabular DSS.
Final QML is valuable because it gives stronger stable-material recall and F1
on the balanced QML task. The DSS uses this honestly: classical ML supports the
current recommendation, and QML shows the future direction for quantum-assisted
materials discovery.

## How To Run

```bash
python3 -m pip install -r requirements.txt
cd "Battery Materials DSS QML"
python3 scripts/create_main_presentation_notebook.py
```

Full pipeline scripts are inside `Battery Materials DSS QML/scripts/`.
