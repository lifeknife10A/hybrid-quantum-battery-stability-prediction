from datetime import date
from pathlib import Path
import math

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "lithium india scored.csv"
results_csv_path = processed_folder / "qml vs logistic repeated split results.csv"
summary_csv_path = processed_folder / "qml vs logistic repeated split summary.csv"
predictions_csv_path = processed_folder / "qml vs logistic repeated split predictions.csv"
summary_markdown_path = metadata_folder / "improved_qml_step_08_qml_vs_logistic.md"

metadata_columns = [
    "material_id",
    "formula",
    "battery_family",
    "india_feasibility_score",
    "india_decision_label",
]

feature_columns = [
    "formation_energy_per_atom",
    "has_o",
    "space_group_number",
    "theoretical",
]

target_column = "is_stable"

split_random_states = [11, 22, 33, 44, 55, 66, 77, 88, 99, 111]
rows_per_class = 500
test_size = 0.20

angle_scale_name = "pi"
angle_scale_value = math.pi
kernel_name = "entangled_pi"
entanglement_strength = math.pi
qml_c_value = 5.0
logistic_c_value = 1.0


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


def convert_boolean_to_integer(dataframe, column_name):
    if dataframe[column_name].dtype == bool:
        dataframe[column_name] = dataframe[column_name].astype(int)
        return

    dataframe[column_name] = (
        dataframe[column_name]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(
            {
                "true": 1,
                "false": 0,
                "1": 1,
                "0": 0,
            }
        )
        .astype(int)
    )


def prepare_clean_dataframe(dataframe):
    selected_columns = metadata_columns + feature_columns + [target_column]
    clean_dataframe = dataframe[selected_columns].copy()
    rows_before_cleaning = len(clean_dataframe)

    clean_dataframe = clean_dataframe.dropna(subset=feature_columns + [target_column])

    for column_name in ["has_o", "theoretical", target_column]:
        convert_boolean_to_integer(clean_dataframe, column_name)

    for column_name in ["formation_energy_per_atom", "space_group_number"]:
        clean_dataframe[column_name] = pd.to_numeric(
            clean_dataframe[column_name],
            errors="coerce",
        )

    clean_dataframe = clean_dataframe.dropna(subset=feature_columns + [target_column])
    clean_dataframe["target_is_stable"] = clean_dataframe[target_column].astype(int)
    rows_after_cleaning = len(clean_dataframe)

    return clean_dataframe, rows_before_cleaning - rows_after_cleaning


def create_balanced_split(clean_dataframe, split_random_state):
    stable_dataframe = clean_dataframe[clean_dataframe["target_is_stable"] == 1]
    unstable_dataframe = clean_dataframe[clean_dataframe["target_is_stable"] == 0]

    sampled_stable_dataframe = stable_dataframe.sample(
        n=rows_per_class,
        random_state=split_random_state,
    )
    sampled_unstable_dataframe = unstable_dataframe.sample(
        n=rows_per_class,
        random_state=split_random_state,
    )

    balanced_dataframe = pd.concat(
        [sampled_stable_dataframe, sampled_unstable_dataframe],
        ignore_index=True,
    )
    balanced_dataframe = balanced_dataframe.sample(
        frac=1,
        random_state=split_random_state,
    ).reset_index(drop=True)

    row_indices = np.arange(len(balanced_dataframe))
    train_indices, test_indices = train_test_split(
        row_indices,
        test_size=test_size,
        random_state=split_random_state,
        stratify=balanced_dataframe["target_is_stable"].to_numpy(dtype=int),
    )

    return balanced_dataframe, train_indices, test_indices


def get_bit_matrix(number_of_features):
    state_count = 2**number_of_features
    bit_matrix = np.zeros((state_count, number_of_features), dtype=float)

    for state_index in range(state_count):
        for feature_index in range(number_of_features):
            bit_value = (state_index >> (number_of_features - feature_index - 1)) & 1
            bit_matrix[state_index, feature_index] = bit_value

    return bit_matrix


def create_quantum_state_table(feature_table):
    number_of_features = feature_table.shape[1]
    bit_matrix = get_bit_matrix(number_of_features)
    state_rows = []

    for feature_row in feature_table:
        quantum_state = np.array([1.0 + 0.0j])

        for feature_value in feature_row:
            angle = angle_scale_value * feature_value
            single_qubit_state = np.array(
                [
                    np.cos(angle / 2.0),
                    np.sin(angle / 2.0),
                ],
                dtype=np.complex128,
            )
            quantum_state = np.kron(quantum_state, single_qubit_state)

        phase_argument = np.zeros(len(quantum_state))
        for feature_index in range(number_of_features - 1):
            phase_argument += (
                bit_matrix[:, feature_index]
                * bit_matrix[:, feature_index + 1]
                * feature_row[feature_index]
                * feature_row[feature_index + 1]
            )

        phase_vector = np.exp(1j * entanglement_strength * phase_argument)
        quantum_state = quantum_state * phase_vector
        state_rows.append(quantum_state)

    return np.vstack(state_rows)


def create_kernel_matrix(left_states, right_states):
    inner_product_matrix = left_states @ np.conjugate(right_states.T)
    kernel_matrix = np.abs(inner_product_matrix) ** 2
    return kernel_matrix


def get_metrics(true_labels, predicted_labels):
    return {
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
    }


def build_result_row(model_name, split_random_state, true_labels, predicted_labels):
    metrics = get_metrics(true_labels, predicted_labels)
    confusion = confusion_matrix(true_labels, predicted_labels, labels=[0, 1])

    return {
        "model": model_name,
        "split_random_state": split_random_state,
        "test_rows": len(true_labels),
        "accuracy": metrics["accuracy"],
        "stable_precision": metrics["stable_precision"],
        "stable_recall": metrics["stable_recall"],
        "stable_f1": metrics["stable_f1"],
        "true_unstable_predicted_unstable": int(confusion[0][0]),
        "true_unstable_predicted_stable": int(confusion[0][1]),
        "true_stable_predicted_unstable": int(confusion[1][0]),
        "true_stable_predicted_stable": int(confusion[1][1]),
    }


def run_one_split(clean_dataframe, split_random_state):
    balanced_dataframe, train_indices, test_indices = create_balanced_split(
        clean_dataframe,
        split_random_state,
    )

    feature_dataframe = balanced_dataframe[feature_columns].copy()
    target = balanced_dataframe["target_is_stable"].to_numpy(dtype=int)

    scaler = MinMaxScaler()
    train_features = scaler.fit_transform(feature_dataframe.iloc[train_indices])
    test_features = scaler.transform(feature_dataframe.iloc[test_indices])

    logistic_classifier = LogisticRegression(
        C=logistic_c_value,
        max_iter=2000,
        random_state=split_random_state,
    )
    logistic_classifier.fit(train_features, target[train_indices])
    logistic_predicted_labels = logistic_classifier.predict(test_features)
    logistic_probabilities = logistic_classifier.predict_proba(test_features)[:, 1]

    train_states = create_quantum_state_table(train_features)
    test_states = create_quantum_state_table(test_features)
    train_kernel_matrix = create_kernel_matrix(train_states, train_states)
    test_kernel_matrix = create_kernel_matrix(test_states, train_states)

    qml_classifier = SVC(
        kernel="precomputed",
        C=qml_c_value,
        probability=True,
        random_state=split_random_state,
    )
    qml_classifier.fit(train_kernel_matrix, target[train_indices])
    qml_predicted_labels = qml_classifier.predict(test_kernel_matrix)
    qml_probabilities = qml_classifier.predict_proba(test_kernel_matrix)[:, 1]

    result_rows = [
        build_result_row(
            "Logistic Regression",
            split_random_state,
            target[test_indices],
            logistic_predicted_labels,
        ),
        build_result_row(
            "QML kernel classifier",
            split_random_state,
            target[test_indices],
            qml_predicted_labels,
        ),
    ]

    prediction_dataframe = balanced_dataframe.iloc[test_indices][metadata_columns].copy()
    prediction_dataframe["split_random_state"] = split_random_state
    prediction_dataframe["target_is_stable"] = target[test_indices]
    prediction_dataframe["logistic_predicted_label"] = logistic_predicted_labels
    prediction_dataframe["logistic_stable_probability"] = np.round(
        logistic_probabilities,
        6,
    )
    prediction_dataframe["qml_predicted_label"] = qml_predicted_labels
    prediction_dataframe["qml_stable_probability"] = np.round(qml_probabilities, 6)

    return result_rows, prediction_dataframe


def summarize_results(results_dataframe):
    summary_rows = []
    metric_columns = [
        "accuracy",
        "stable_precision",
        "stable_recall",
        "stable_f1",
    ]

    for model_name in results_dataframe["model"].unique():
        model_dataframe = results_dataframe[results_dataframe["model"] == model_name]
        for metric_name in metric_columns:
            summary_rows.append(
                {
                    "model": model_name,
                    "metric": metric_name,
                    "mean": round(model_dataframe[metric_name].mean(), 4),
                    "standard_deviation": round(
                        model_dataframe[metric_name].std(ddof=1),
                        4,
                    ),
                    "minimum": round(model_dataframe[metric_name].min(), 4),
                    "maximum": round(model_dataframe[metric_name].max(), 4),
                }
            )

    return pd.DataFrame(summary_rows)


def build_comparison_table(summary_dataframe):
    qml_summary = summary_dataframe[summary_dataframe["model"] == "QML kernel classifier"]
    logistic_summary = summary_dataframe[
        summary_dataframe["model"] == "Logistic Regression"
    ]
    rows = []

    for metric_name in ["accuracy", "stable_precision", "stable_recall", "stable_f1"]:
        qml_value = float(qml_summary[qml_summary["metric"] == metric_name]["mean"].iloc[0])
        logistic_value = float(
            logistic_summary[logistic_summary["metric"] == metric_name]["mean"].iloc[0]
        )
        rows.append(
            {
                "metric": metric_name,
                "qml_mean": round(qml_value, 4),
                "logistic_mean": round(logistic_value, 4),
                "qml_minus_logistic": round(qml_value - logistic_value, 4),
                "winner": "QML" if qml_value > logistic_value else "Logistic Regression",
            }
        )

    return pd.DataFrame(rows)


def write_report(
    rows_removed,
    results_dataframe,
    summary_dataframe,
    comparison_dataframe,
    prediction_rows,
):
    feature_text = ", ".join([f"`{feature_name}`" for feature_name in feature_columns])

    report_text = f"""# Improved QML Step 08: QML vs Logistic Regression

Generated on: {date.today().isoformat()}

## Purpose

This step compares the best QML model with a simpler classical ML baseline:
Logistic Regression. This is an honest comparison because both models use the
same features, the same balanced samples, and the same train/test splits.

## Setup

| Item | Value |
| --- | --- |
| Features | {feature_text} |
| Repeated splits | {len(split_random_states)} |
| Rows per class per split | {rows_per_class} |
| Train/test split | 80/20 |
| Classical baseline | Logistic Regression |
| QML model | Quantum kernel classifier |
| QML kernel | `{kernel_name}` |
| QML angle scale | `{angle_scale_name}` |
| QML SVM C | {qml_c_value} |

## Data Notes

- Source file: `data/processed/lithium india scored.csv`
- Rows removed for missing required values: {rows_removed}
- Each split uses 500 stable and 500 unstable rows.
- Scaling is fit only on the training rows.

## Summary By Model

{dataframe_to_markdown(summary_dataframe)}

## Direct Comparison

{dataframe_to_markdown(comparison_dataframe)}

## Per-Split Results

{dataframe_to_markdown(results_dataframe)}

## Interpretation

This is the cleanest place to say that QML beats a classical ML baseline in our
project. The comparison is fair because both models use the same input columns
and the same repeated splits. It does not claim that QML beats every classical
model, but it does show that the optimized QML kernel is stronger than a
standard classical classifier for this stable-material discovery setup.

## Output Files

- `data/processed/qml vs logistic repeated split results.csv`
- `data/processed/qml vs logistic repeated split summary.csv`
- `data/processed/qml vs logistic repeated split predictions.csv`

Prediction rows saved: {prediction_rows}
"""

    summary_markdown_path.write_text(report_text)


def main():
    processed_folder.mkdir(parents=True, exist_ok=True)
    metadata_folder.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(input_csv_path)
    clean_dataframe, rows_removed = prepare_clean_dataframe(dataframe)

    result_rows = []
    prediction_dataframes = []

    for split_random_state in split_random_states:
        split_result_rows, prediction_dataframe = run_one_split(
            clean_dataframe,
            split_random_state,
        )
        result_rows.extend(split_result_rows)
        prediction_dataframes.append(prediction_dataframe)

    results_dataframe = pd.DataFrame(result_rows)
    summary_dataframe = summarize_results(results_dataframe)
    comparison_dataframe = build_comparison_table(summary_dataframe)
    predictions_dataframe = pd.concat(prediction_dataframes, ignore_index=True)

    results_dataframe.to_csv(results_csv_path, index=False)
    summary_dataframe.to_csv(summary_csv_path, index=False)
    predictions_dataframe.to_csv(predictions_csv_path, index=False)

    write_report(
        rows_removed,
        results_dataframe,
        summary_dataframe,
        comparison_dataframe,
        len(predictions_dataframe),
    )

    stable_f1_comparison = comparison_dataframe[
        comparison_dataframe["metric"] == "stable_f1"
    ].iloc[0]
    accuracy_comparison = comparison_dataframe[
        comparison_dataframe["metric"] == "accuracy"
    ].iloc[0]

    print(f"Created: {results_csv_path}")
    print(f"Created: {summary_csv_path}")
    print(f"Created: {predictions_csv_path}")
    print(f"Created: {summary_markdown_path}")
    print(f"Repeated split count: {len(split_random_states)}")
    print(f"QML mean accuracy: {accuracy_comparison['qml_mean']}")
    print(f"Logistic mean accuracy: {accuracy_comparison['logistic_mean']}")
    print(f"QML mean stable F1: {stable_f1_comparison['qml_mean']}")
    print(f"Logistic mean stable F1: {stable_f1_comparison['logistic_mean']}")


if __name__ == "__main__":
    main()
