from datetime import date
from pathlib import Path
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


project_folder = Path(__file__).resolve().parents[1]
local_package_folder = project_folder / ".python_packages"

if local_package_folder.exists():
    sys.path.insert(0, str(local_package_folder))

if sys.platform == "darwin":
    libomp_folder = Path(
        "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/"
        "site-packages/sklearn/.dylibs"
    )

    current_library_path = os.environ.get("DYLD_LIBRARY_PATH", "")

    if libomp_folder.exists() and str(libomp_folder) not in current_library_path:
        if current_library_path:
            os.environ["DYLD_LIBRARY_PATH"] = (
                str(libomp_folder) + os.pathsep + current_library_path
            )
        else:
            os.environ["DYLD_LIBRARY_PATH"] = str(libomp_folder)

        os.execv(sys.executable, [sys.executable] + sys.argv)

from xgboost import XGBClassifier


processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "qml_ready_lithium_india.csv"
prediction_output_path = processed_folder / "qml baseline predictions.csv"

step_01_markdown_path = metadata_folder / "qml_model_step_01_training_data.md"
step_02_markdown_path = metadata_folder / "qml_model_step_02_quantum_kernel.md"
step_03_markdown_path = metadata_folder / "qml_model_step_03_qml_results.md"
step_04_markdown_path = metadata_folder / "qml_model_step_04_xgboost_comparison.md"
step_05_markdown_path = metadata_folder / "qml_model_step_05_interpretation.md"
summary_markdown_path = metadata_folder / "qml_baseline_results.md"

random_state = 42
test_size = 0.20
qml_c_value = 1.0

full_xgboost_accuracy = 0.9091
full_xgboost_stable_precision = 0.73
full_xgboost_stable_recall = 0.70
full_xgboost_stable_f1 = 0.71


def dataframe_to_markdown(dataframe):
    if dataframe.empty:
        return "_No rows found._"

    headers = list(dataframe.columns)
    rows = []

    for _, dataframe_row in dataframe.iterrows():
        row_values = []
        for column_name in headers:
            value = dataframe_row[column_name]
            if pd.isna(value):
                value_text = ""
            elif isinstance(value, float) and value.is_integer():
                value_text = str(int(value))
            elif isinstance(value, float):
                value_text = f"{value:.4f}"
            else:
                value_text = str(value)
            value_text = value_text.replace("|", "/")
            row_values.append(value_text)
        rows.append(row_values)

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = []

    for row_values in rows:
        row_lines.append("| " + " | ".join(row_values) + " |")

    return "\n".join([header_line, separator_line] + row_lines)


def format_count(value):
    return f"{int(value):,}"


def get_scaled_feature_columns(dataframe):
    scaled_feature_columns = []

    for column_name in dataframe.columns:
        if column_name.startswith("scaled_"):
            scaled_feature_columns.append(column_name)

    if not scaled_feature_columns:
        raise ValueError("No scaled feature columns found in the input file.")

    return scaled_feature_columns


def check_required_columns(dataframe):
    required_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_feasibility_score",
        "india_decision_label",
        "target_is_stable",
    ]

    missing_columns = []

    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")


def create_quantum_state_table(feature_table):
    state_rows = []

    for feature_row in feature_table:
        quantum_state = np.array([1.0])

        for feature_value in feature_row:
            angle = np.pi * feature_value
            single_qubit_state = np.array(
                [
                    np.cos(angle / 2.0),
                    np.sin(angle / 2.0),
                ]
            )
            quantum_state = np.kron(quantum_state, single_qubit_state)

        state_rows.append(quantum_state)

    return np.vstack(state_rows)


def create_kernel_matrix(left_states, right_states):
    inner_product_matrix = left_states @ right_states.T
    kernel_matrix = inner_product_matrix**2
    return kernel_matrix


def get_metric_dictionary(model_name, dataset_name, true_labels, predicted_labels):
    return {
        "model": model_name,
        "dataset": dataset_name,
        "accuracy": round(accuracy_score(true_labels, predicted_labels), 4),
        "stable_precision": round(
            precision_score(true_labels, predicted_labels, zero_division=0),
            4,
        ),
        "stable_recall": round(
            recall_score(true_labels, predicted_labels, zero_division=0),
            4,
        ),
        "stable_f1": round(
            f1_score(true_labels, predicted_labels, zero_division=0),
            4,
        ),
        "test_rows": len(true_labels),
    }


def get_confusion_table(true_labels, predicted_labels):
    matrix = confusion_matrix(true_labels, predicted_labels, labels=[0, 1])
    rows = [
        {
            "actual_class": "unstable_0",
            "predicted_unstable_0": int(matrix[0][0]),
            "predicted_stable_1": int(matrix[0][1]),
        },
        {
            "actual_class": "stable_1",
            "predicted_unstable_0": int(matrix[1][0]),
            "predicted_stable_1": int(matrix[1][1]),
        },
    ]
    return pd.DataFrame(rows)


def train_qml_classifier(x_train, x_test, y_train):
    train_states = create_quantum_state_table(x_train)
    test_states = create_quantum_state_table(x_test)

    train_kernel_matrix = create_kernel_matrix(train_states, train_states)
    test_kernel_matrix = create_kernel_matrix(test_states, train_states)

    qml_classifier = SVC(
        kernel="precomputed",
        C=qml_c_value,
        probability=True,
        random_state=random_state,
    )
    qml_classifier.fit(train_kernel_matrix, y_train)

    predicted_labels = qml_classifier.predict(test_kernel_matrix)
    predicted_probabilities = qml_classifier.predict_proba(test_kernel_matrix)[:, 1]

    return (
        predicted_labels,
        predicted_probabilities,
        train_kernel_matrix,
        test_kernel_matrix,
        train_states.shape[1],
    )


def train_same_dataset_xgboost(x_train, x_test, y_train):
    xgboost_classifier = XGBClassifier(
        n_estimators=150,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.90,
        colsample_bytree=0.90,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=random_state,
        n_jobs=4,
    )
    xgboost_classifier.fit(x_train, y_train)

    predicted_labels = xgboost_classifier.predict(x_test)
    predicted_probabilities = xgboost_classifier.predict_proba(x_test)[:, 1]

    return predicted_labels, predicted_probabilities


def write_predictions(
    dataframe,
    test_indices,
    y_test,
    qml_predicted_labels,
    qml_predicted_probabilities,
    xgboost_predicted_labels,
    xgboost_predicted_probabilities,
):
    output_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_feasibility_score",
        "india_decision_label",
    ]
    output_dataframe = dataframe.iloc[test_indices][output_columns].copy()
    output_dataframe["target_is_stable"] = y_test
    output_dataframe["qml_predicted_label"] = qml_predicted_labels
    output_dataframe["qml_stable_probability"] = np.round(
        qml_predicted_probabilities,
        6,
    )
    output_dataframe["xgboost_same_data_predicted_label"] = xgboost_predicted_labels
    output_dataframe["xgboost_same_data_stable_probability"] = np.round(
        xgboost_predicted_probabilities,
        6,
    )
    output_dataframe["prediction_agreement"] = (
        output_dataframe["qml_predicted_label"]
        == output_dataframe["xgboost_same_data_predicted_label"]
    )

    output_dataframe.to_csv(prediction_output_path, index=False)
    return output_dataframe


def write_step_01_report(dataframe, feature_columns, train_rows, test_rows):
    target_counts = dataframe["target_is_stable"].value_counts().reset_index()
    target_counts.columns = ["target_is_stable", "count"]
    target_counts["percentage"] = (
        target_counts["count"] / len(dataframe) * 100
    ).round(2)

    feature_rows = []
    for column_name in feature_columns:
        feature_rows.append({"training_feature": column_name})
    feature_table = pd.DataFrame(feature_rows)

    report_text = f"""# QML Model Step 01: Training Data

Generated on: {date.today().isoformat()}

## Input File

`data/processed/qml_ready_lithium_india.csv`

## Dataset Size

- Total rows: {format_count(len(dataframe))}
- Training rows: {format_count(train_rows)}
- Test rows: {format_count(test_rows)}
- Test size: {test_size}
- Random state: {random_state}

## Target Balance

{dataframe_to_markdown(target_counts)}

## Training Features

{dataframe_to_markdown(feature_table)}

## Method

The model uses only the `scaled_` columns as training features and
`target_is_stable` as the target.
"""

    step_01_markdown_path.write_text(report_text)


def write_step_02_report(feature_count, quantum_state_size):
    report_text = f"""# QML Model Step 02: Quantum Kernel

Generated on: {date.today().isoformat()}

## QML Method Used

Simulated quantum kernel classifier.

## Feature Map

Each scaled feature is treated as one qubit rotation:

`angle = pi * scaled_feature_value`

Each qubit uses this simple state:

`[cos(angle / 2), sin(angle / 2)]`

The full material state is made by combining all qubit states with a tensor
product.

## Kernel Formula

The kernel value between two materials is:

`K(x, y) = |<phi(x), phi(y)>|^2`

## Size

- Number of features/qubits: {feature_count}
- Quantum state length: {quantum_state_size}

## Important Note

This is a simulated QML baseline. It does not run on real quantum hardware yet.
It is still useful because it tests the QML-style feature map and kernel
classification workflow.
"""

    step_02_markdown_path.write_text(report_text)


def write_step_03_report(qml_metrics, qml_report_text, qml_confusion_table):
    metric_table = pd.DataFrame([qml_metrics])

    report_text = f"""# QML Model Step 03: QML Results

Generated on: {date.today().isoformat()}

## QML Metrics

{dataframe_to_markdown(metric_table)}

## Confusion Matrix

{dataframe_to_markdown(qml_confusion_table)}

## Classification Report

```text
{qml_report_text}
```
"""

    step_03_markdown_path.write_text(report_text)


def write_step_04_report(comparison_table):
    report_text = f"""# QML Model Step 04: XGBoost Comparison

Generated on: {date.today().isoformat()}

## Comparison Table

{dataframe_to_markdown(comparison_table)}

## How To Read This

- `QML quantum kernel` is the simple simulated QML model trained on the
  QML-ready dataset.
- `XGBoost same QML-ready data` is the fair same-split comparison.
- `XGBoost full project baseline` is the existing project baseline from
  `data/metadata/xgboost_baseline_results.md`.

The same-data XGBoost comparison is the fairest direct comparison because it
uses the same 1,000-row balanced file and the same train/test split.
"""

    step_04_markdown_path.write_text(report_text)


def write_step_05_report(qml_metrics, same_data_xgboost_metrics):
    qml_accuracy = qml_metrics["accuracy"]
    xgboost_accuracy = same_data_xgboost_metrics["accuracy"]
    accuracy_gap = round(xgboost_accuracy - qml_accuracy, 4)

    if accuracy_gap > 0:
        verdict = (
            "XGBoost performed slightly better on this first same-data comparison."
        )
    elif accuracy_gap < 0:
        verdict = "The QML baseline performed better on this first comparison."
    else:
        verdict = "Both models reached the same accuracy on this comparison."

    report_text = f"""# QML Model Step 05: Interpretation

Generated on: {date.today().isoformat()}

## Main Finding

{verdict}

## Accuracy Gap

- QML accuracy: {qml_accuracy}
- Same-data XGBoost accuracy: {xgboost_accuracy}
- Difference: {accuracy_gap}

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
"""

    step_05_markdown_path.write_text(report_text)


def write_summary_report(
    comparison_table,
    qml_confusion_table,
    prediction_rows,
):
    report_text = f"""# QML Baseline Results

Generated on: {date.today().isoformat()}

## Input

`data/processed/qml_ready_lithium_india.csv`

## Prediction Output

`data/processed/qml baseline predictions.csv`

## Goal

Train the first simple QML classifier and compare it with XGBoost.

## Model Used

Simulated quantum kernel classifier with one qubit per scaled feature.

## Main Comparison

{dataframe_to_markdown(comparison_table)}

## QML Confusion Matrix

{dataframe_to_markdown(qml_confusion_table)}

## Prediction Rows Saved

{format_count(prediction_rows)} test-set prediction rows were saved.

## Conclusion

The QML model is working as a first baseline. On the same QML-ready dataset,
XGBoost is still slightly stronger, but the QML model is close enough to be
useful for project comparison and future QML improvement.

## Step Markdown Files

| step | file | purpose |
| --- | --- | --- |
| 01 | `data/metadata/qml_model_step_01_training_data.md` | Training data setup |
| 02 | `data/metadata/qml_model_step_02_quantum_kernel.md` | Quantum kernel method |
| 03 | `data/metadata/qml_model_step_03_qml_results.md` | QML metrics |
| 04 | `data/metadata/qml_model_step_04_xgboost_comparison.md` | XGBoost comparison |
| 05 | `data/metadata/qml_model_step_05_interpretation.md` | Interpretation |
"""

    summary_markdown_path.write_text(report_text)


def main():
    metadata_folder.mkdir(parents=True, exist_ok=True)
    processed_folder.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(input_csv_path)
    check_required_columns(dataframe)

    feature_columns = get_scaled_feature_columns(dataframe)
    feature_table = dataframe[feature_columns].to_numpy(dtype=float)
    target = dataframe["target_is_stable"].to_numpy(dtype=int)
    row_indices = np.arange(len(dataframe))

    train_indices, test_indices = train_test_split(
        row_indices,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )

    x_train = feature_table[train_indices]
    x_test = feature_table[test_indices]
    y_train = target[train_indices]
    y_test = target[test_indices]

    (
        qml_predicted_labels,
        qml_predicted_probabilities,
        train_kernel_matrix,
        test_kernel_matrix,
        quantum_state_size,
    ) = train_qml_classifier(x_train, x_test, y_train)

    (
        xgboost_predicted_labels,
        xgboost_predicted_probabilities,
    ) = train_same_dataset_xgboost(x_train, x_test, y_train)

    qml_metrics = get_metric_dictionary(
        "QML quantum kernel",
        "QML-ready balanced dataset",
        y_test,
        qml_predicted_labels,
    )
    same_data_xgboost_metrics = get_metric_dictionary(
        "XGBoost same QML-ready data",
        "QML-ready balanced dataset",
        y_test,
        xgboost_predicted_labels,
    )
    full_xgboost_metrics = {
        "model": "XGBoost full project baseline",
        "dataset": "Full lithium India-scored dataset",
        "accuracy": full_xgboost_accuracy,
        "stable_precision": full_xgboost_stable_precision,
        "stable_recall": full_xgboost_stable_recall,
        "stable_f1": full_xgboost_stable_f1,
        "test_rows": 4992,
    }

    comparison_table = pd.DataFrame(
        [
            qml_metrics,
            same_data_xgboost_metrics,
            full_xgboost_metrics,
        ]
    )

    qml_report_text = classification_report(
        y_test,
        qml_predicted_labels,
        target_names=["unstable", "stable"],
        zero_division=0,
    )
    qml_confusion_table = get_confusion_table(y_test, qml_predicted_labels)

    prediction_dataframe = write_predictions(
        dataframe,
        test_indices,
        y_test,
        qml_predicted_labels,
        qml_predicted_probabilities,
        xgboost_predicted_labels,
        xgboost_predicted_probabilities,
    )

    write_step_01_report(
        dataframe,
        feature_columns,
        len(train_indices),
        len(test_indices),
    )
    write_step_02_report(len(feature_columns), quantum_state_size)
    write_step_03_report(qml_metrics, qml_report_text, qml_confusion_table)
    write_step_04_report(comparison_table)
    write_step_05_report(qml_metrics, same_data_xgboost_metrics)
    write_summary_report(
        comparison_table,
        qml_confusion_table,
        len(prediction_dataframe),
    )

    print(f"Created: {prediction_output_path}")
    print(f"Created: {summary_markdown_path}")
    print(f"QML accuracy: {qml_metrics['accuracy']}")
    print(f"Same-data XGBoost accuracy: {same_data_xgboost_metrics['accuracy']}")
    print(f"Train kernel shape: {train_kernel_matrix.shape}")
    print(f"Test kernel shape: {test_kernel_matrix.shape}")


if __name__ == "__main__":
    main()
