from datetime import date
from pathlib import Path
import math

import numpy as np
import pandas as pd
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
results_csv_path = processed_folder / "best qml repeated split results.csv"
predictions_csv_path = processed_folder / "best qml repeated split predictions.csv"
summary_markdown_path = (
    metadata_folder / "improved_qml_step_07_repeated_split_validation.md"
)

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
c_value = 5.0


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

    train_states = create_quantum_state_table(train_features)
    test_states = create_quantum_state_table(test_features)

    train_kernel_matrix = create_kernel_matrix(train_states, train_states)
    test_kernel_matrix = create_kernel_matrix(test_states, train_states)

    classifier = SVC(
        kernel="precomputed",
        C=c_value,
        probability=True,
        random_state=split_random_state,
    )
    classifier.fit(train_kernel_matrix, target[train_indices])

    predicted_labels = classifier.predict(test_kernel_matrix)
    predicted_probabilities = classifier.predict_proba(test_kernel_matrix)[:, 1]
    metrics = get_metrics(target[test_indices], predicted_labels)
    confusion = confusion_matrix(target[test_indices], predicted_labels, labels=[0, 1])

    result_row = {
        "split_random_state": split_random_state,
        "train_rows": len(train_indices),
        "test_rows": len(test_indices),
        "stable_train_rows": int(target[train_indices].sum()),
        "unstable_train_rows": int(len(train_indices) - target[train_indices].sum()),
        "stable_test_rows": int(target[test_indices].sum()),
        "unstable_test_rows": int(len(test_indices) - target[test_indices].sum()),
        "accuracy": metrics["accuracy"],
        "stable_precision": metrics["stable_precision"],
        "stable_recall": metrics["stable_recall"],
        "stable_f1": metrics["stable_f1"],
        "true_unstable_predicted_unstable": int(confusion[0][0]),
        "true_unstable_predicted_stable": int(confusion[0][1]),
        "true_stable_predicted_unstable": int(confusion[1][0]),
        "true_stable_predicted_stable": int(confusion[1][1]),
    }

    prediction_dataframe = balanced_dataframe.iloc[test_indices][metadata_columns].copy()
    prediction_dataframe["split_random_state"] = split_random_state
    prediction_dataframe["target_is_stable"] = target[test_indices]
    prediction_dataframe["repeated_qml_predicted_label"] = predicted_labels
    prediction_dataframe["repeated_qml_stable_probability"] = np.round(
        predicted_probabilities,
        6,
    )

    return result_row, prediction_dataframe


def summarize_results(results_dataframe):
    metric_columns = [
        "accuracy",
        "stable_precision",
        "stable_recall",
        "stable_f1",
    ]
    summary_rows = []

    for metric_name in metric_columns:
        summary_rows.append(
            {
                "metric": metric_name,
                "mean": round(results_dataframe[metric_name].mean(), 4),
                "standard_deviation": round(
                    results_dataframe[metric_name].std(ddof=1),
                    4,
                ),
                "minimum": round(results_dataframe[metric_name].min(), 4),
                "maximum": round(results_dataframe[metric_name].max(), 4),
            }
        )

    return pd.DataFrame(summary_rows)


def write_report(
    rows_removed,
    results_dataframe,
    summary_dataframe,
    prediction_rows,
):
    feature_text = ", ".join([f"`{feature_name}`" for feature_name in feature_columns])

    report_text = f"""# Improved QML Step 07: Repeated Split Validation

Generated on: {date.today().isoformat()}

## Purpose

This step checks whether the best QML setup is stable across multiple random
train/test splits. A single 200-row test split can be lucky or unlucky, so this
validation repeats the experiment with different random seeds.

## Best QML Setup Tested

| Parameter | Value |
| --- | --- |
| Features | {feature_text} |
| Qubits | 4 |
| Kernel | `{kernel_name}` |
| Angle scale | `{angle_scale_name}` |
| SVM C | {c_value} |
| Rows per class per split | {rows_per_class} |
| Train/test split | 80/20 |
| Random states | {split_random_states} |

## Data Notes

- Source file: `data/processed/lithium india scored.csv`
- Rows removed for missing required values: {rows_removed}
- Each split uses a fresh balanced sample of 500 stable and 500 unstable rows.
- The scaler is fit only on the training rows for that split.
- The test rows are not used during training.

## Per-Split Results

{dataframe_to_markdown(results_dataframe)}

## Summary Across Splits

{dataframe_to_markdown(summary_dataframe)}

## Main Interpretation

The repeated-split result is the number we should trust more than a single
train/test split. If the mean stable F1 stays close to the single-split result,
then the QML result is stable. If it drops a lot, the earlier result was partly
dependent on the random split.

## Output Files

- `data/processed/best qml repeated split results.csv`
- `data/processed/best qml repeated split predictions.csv`

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
        result_row, prediction_dataframe = run_one_split(
            clean_dataframe,
            split_random_state,
        )
        result_rows.append(result_row)
        prediction_dataframes.append(prediction_dataframe)

    results_dataframe = pd.DataFrame(result_rows)
    predictions_dataframe = pd.concat(prediction_dataframes, ignore_index=True)
    summary_dataframe = summarize_results(results_dataframe)

    results_dataframe.to_csv(results_csv_path, index=False)
    predictions_dataframe.to_csv(predictions_csv_path, index=False)

    write_report(
        rows_removed,
        results_dataframe,
        summary_dataframe,
        len(predictions_dataframe),
    )

    stable_f1_row = summary_dataframe[summary_dataframe["metric"] == "stable_f1"].iloc[
        0
    ]
    accuracy_row = summary_dataframe[summary_dataframe["metric"] == "accuracy"].iloc[0]

    print(f"Created: {results_csv_path}")
    print(f"Created: {predictions_csv_path}")
    print(f"Created: {summary_markdown_path}")
    print(f"Repeated split count: {len(split_random_states)}")
    print(f"Mean accuracy: {accuracy_row['mean']}")
    print(f"Mean stable F1: {stable_f1_row['mean']}")
    print(f"Stable F1 standard deviation: {stable_f1_row['standard_deviation']}")


if __name__ == "__main__":
    main()
