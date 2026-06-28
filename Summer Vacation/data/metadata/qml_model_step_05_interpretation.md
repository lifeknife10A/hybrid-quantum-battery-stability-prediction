# QML Model Step 05: Interpretation

Generated on: 2026-06-28

## Main Finding

XGBoost performed slightly better on this first same-data comparison.

## Accuracy Gap

- QML accuracy: 0.81
- Same-data XGBoost accuracy: 0.83
- Difference: 0.02

## Academic Interpretation

This is a successful first QML baseline because it trains on the prepared
QML-ready dataset and gives measurable classification results. XGBoost is still
stronger in this first comparison, which is expected because XGBoost is a very
strong classical method for tabular data.

## Next Improvement Ideas

- Try fewer qubits using only the strongest features.
- Try different quantum feature maps.
- Tune the SVM `C` value.
- Compare against more classical baselines.
- Later, test a Qiskit or PennyLane circuit if the environment supports it.
