from datetime import date
from pathlib import Path
import math

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "qml_ready_lithium_india.csv"
tuning_results_csv_path = processed_folder / "qml tuning results.csv"
best_predictions_csv_path = processed_folder / "qml tuned best predictions.csv"

search_space_markdown_path = metadata_folder / "qml_tuning_step_01_search_space.md"
validation_markdown_path = metadata_folder / "qml_tuning_step_02_validation_results.md"
best_model_markdown_path = metadata_folder / "qml_tuning_step_03_best_model_test.md"
tuning_results_markdown_path = metadata_folder / "qml_tuning_results.md"
best_summary_markdown_path = metadata_folder / "qml_best_model_summary.md"

random_state = 42
test_size = 0.20
cross_validation_splits = 4

feature_count_options = [4, 6, 8, 10]
angle_scale_options = [
    {
        "angle_scale_name": "pi_over_2",
        "angle_scale_value": math.pi / 2,
    },
    {
        "angle_scale_name": "pi",
        "angle_scale_value": math.pi,
    },
    {
        "angle_scale_name": "two_pi",
        "angle_scale_value": 2 * math.pi,
    },
]
c_value_options = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

all_scaled_feature_columns = [
    "scaled_space_group_number",
    "scaled_band_gap",
    "scaled_formation_energy_per_atom",
    "scaled_number_of_elements",
    "scaled_has_fe",
    "scaled_has_p",
    "scaled_has_mn",
    "scaled_has_c",
    "scaled_has_si",
    "scaled_has_s",
]


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


def check_required_columns(dataframe):
    required_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_feasibility_score",
        "india_decision_label",
        "target_is_stable",
    ] + all_scaled_feature_columns

    missing_columns = []

    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")


def create_quantum_state_table(feature_table, angle_scale_value):
    state_rows = []

    for feature_row in feature_table:
        quantum_state = np.array([1.0])

        for feature_value in feature_row:
            angle = angle_scale_value * feature_value
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


def run_one_cross_validation_group(
    feature_count,
    selected_feature_columns,
    angle_scale_name,
    angle_scale_value,
    full_kernel_matrix,
    target,
    cross_validator,
):
    result_rows = []

    for c_value in c_value_options:
        fold_metric_rows = []

        for train_positions, validation_positions in cross_validator.split(
            full_kernel_matrix,
            target,
        ):
            train_kernel_matrix = full_kernel_matrix[
                np.ix_(train_positions, train_positions)
            ]
            validation_kernel_matrix = full_kernel_matrix[
                np.ix_(validation_positions, train_positions)
            ]

            qml_classifier = SVC(
                kernel="precomputed",
                C=c_value,
                probability=False,
                random_state=random_state,
            )
            qml_classifier.fit(train_kernel_matrix, target[train_positions])
            predicted_labels = qml_classifier.predict(validation_kernel_matrix)
            metric_values = get_metrics(target[validation_positions], predicted_labels)
            fold_metric_rows.append(metric_values)

        fold_metrics_dataframe = pd.DataFrame(fold_metric_rows)

        result_rows.append(
            {
                "feature_count": feature_count,
                "feature_names": "; ".join(selected_feature_columns),
                "angle_scale": angle_scale_name,
                "angle_scale_value": round(angle_scale_value, 6),
                "c_value": c_value,
                "quantum_state_size": 2**feature_count,
                "train_validation_rows": len(target),
                "cross_validation_splits": cross_validation_splits,
                "cv_accuracy": round(fold_metrics_dataframe["accuracy"].mean(), 4),
                "cv_stable_precision": round(
                    fold_metrics_dataframe["stable_precision"].mean(),
                    4,
                ),
                "cv_stable_recall": round(
                    fold_metrics_dataframe["stable_recall"].mean(),
                    4,
                ),
                "cv_stable_f1": round(fold_metrics_dataframe["stable_f1"].mean(), 4),
            }
        )

    return result_rows


def run_tuning(dataframe, train_validation_indices):
    target = dataframe["target_is_stable"].to_numpy(dtype=int)
    all_result_rows = []
    cross_validator = StratifiedKFold(
        n_splits=cross_validation_splits,
        shuffle=True,
        random_state=random_state,
    )

    for feature_count in feature_count_options:
        selected_feature_columns = all_scaled_feature_columns[:feature_count]
        selected_features = dataframe[selected_feature_columns].to_numpy(dtype=float)

        train_validation_features = selected_features[train_validation_indices]
        train_validation_target = target[train_validation_indices]

        for angle_option in angle_scale_options:
            train_validation_states = create_quantum_state_table(
                train_validation_features,
                angle_option["angle_scale_value"],
            )
            full_kernel_matrix = create_kernel_matrix(
                train_validation_states,
                train_validation_states,
            )

            group_rows = run_one_cross_validation_group(
                feature_count,
                selected_feature_columns,
                angle_option["angle_scale_name"],
                angle_option["angle_scale_value"],
                full_kernel_matrix,
                train_validation_target,
                cross_validator,
            )
            all_result_rows.extend(group_rows)

    return pd.DataFrame(all_result_rows)


def choose_best_result(tuning_results_dataframe):
    sorted_dataframe = tuning_results_dataframe.sort_values(
        by=[
            "cv_stable_f1",
            "cv_accuracy",
            "cv_stable_recall",
            "feature_count",
            "c_value",
        ],
        ascending=[False, False, False, True, True],
    )
    return sorted_dataframe.iloc[0].to_dict()


def train_best_model(dataframe, train_validation_indices, test_indices, best_result):
    feature_count = int(best_result["feature_count"])
    selected_feature_columns = all_scaled_feature_columns[:feature_count]
    selected_features = dataframe[selected_feature_columns].to_numpy(dtype=float)
    target = dataframe["target_is_stable"].to_numpy(dtype=int)

    x_train_validation = selected_features[train_validation_indices]
    x_test = selected_features[test_indices]
    y_train_validation = target[train_validation_indices]
    y_test = target[test_indices]

    angle_scale_value = float(best_result["angle_scale_value"])
    c_value = float(best_result["c_value"])

    train_validation_states = create_quantum_state_table(
        x_train_validation,
        angle_scale_value,
    )
    test_states = create_quantum_state_table(x_test, angle_scale_value)

    train_validation_kernel_matrix = create_kernel_matrix(
        train_validation_states,
        train_validation_states,
    )
    test_kernel_matrix = create_kernel_matrix(test_states, train_validation_states)

    qml_classifier = SVC(
        kernel="precomputed",
        C=c_value,
        probability=True,
        random_state=random_state,
    )
    qml_classifier.fit(train_validation_kernel_matrix, y_train_validation)

    predicted_labels = qml_classifier.predict(test_kernel_matrix)
    predicted_probabilities = qml_classifier.predict_proba(test_kernel_matrix)[:, 1]
    test_metrics = get_metrics(y_test, predicted_labels)
    report_text = classification_report(
        y_test,
        predicted_labels,
        target_names=["unstable", "stable"],
        zero_division=0,
    )
    confusion_table = get_confusion_table(y_test, predicted_labels)

    return {
        "selected_feature_columns": selected_feature_columns,
        "y_test": y_test,
        "predicted_labels": predicted_labels,
        "predicted_probabilities": predicted_probabilities,
        "test_metrics": test_metrics,
        "report_text": report_text,
        "confusion_table": confusion_table,
        "quantum_state_size": int(train_validation_states.shape[1]),
        "train_validation_kernel_shape": train_validation_kernel_matrix.shape,
        "test_kernel_shape": test_kernel_matrix.shape,
    }


def write_best_predictions(dataframe, test_indices, best_model_result):
    output_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_feasibility_score",
        "india_decision_label",
    ]
    output_dataframe = dataframe.iloc[test_indices][output_columns].copy()
    output_dataframe["target_is_stable"] = best_model_result["y_test"]
    output_dataframe["tuned_qml_predicted_label"] = best_model_result[
        "predicted_labels"
    ]
    output_dataframe["tuned_qml_stable_probability"] = np.round(
        best_model_result["predicted_probabilities"],
        6,
    )
    output_dataframe.to_csv(best_predictions_csv_path, index=False)
    return output_dataframe


def write_search_space_report(train_validation_rows, test_rows):
    feature_rows = []
    for feature_count in feature_count_options:
        feature_rows.append(
            {
                "feature_count": feature_count,
                "features_used": "; ".join(all_scaled_feature_columns[:feature_count]),
            }
        )
    feature_table = pd.DataFrame(feature_rows)

    angle_table = pd.DataFrame(angle_scale_options)
    c_value_table = pd.DataFrame({"c_value": c_value_options})

    total_experiments = (
        len(feature_count_options) * len(angle_scale_options) * len(c_value_options)
    )

    report_text = f"""# QML Tuning Step 01: Search Space

Generated on: {date.today().isoformat()}

## Goal

Test multiple QML hyperparameter combinations and find the best combination
inside this search space.

## Data Split

- Train-validation rows used for tuning: {format_count(train_validation_rows)}
- Cross-validation folds: {cross_validation_splits}
- Untouched test rows: {format_count(test_rows)}
- Random state: {random_state}

## Total Experiments

{format_count(total_experiments)}

## Feature Count Options

{dataframe_to_markdown(feature_table)}

## Angle Scale Options

{dataframe_to_markdown(angle_table)}

## SVM C Values

{dataframe_to_markdown(c_value_table)}

## Selection Rule

The best model is selected by highest cross-validation `stable_f1`. If there is
a tie, cross-validation accuracy and stable recall are used next.
"""

    search_space_markdown_path.write_text(report_text)


def write_validation_report(tuning_results_dataframe, best_result):
    top_results = tuning_results_dataframe.sort_values(
        by=[
            "cv_stable_f1",
            "cv_accuracy",
            "cv_stable_recall",
        ],
        ascending=[False, False, False],
    ).head(15)

    best_table = pd.DataFrame([best_result])

    report_text = f"""# QML Tuning Step 02: Cross-Validation Results

Generated on: {date.today().isoformat()}

## Tuning Output

`data/processed/qml tuning results.csv`

## Number Of Experiments

{format_count(len(tuning_results_dataframe))}

## Best Cross-Validation Combination

{dataframe_to_markdown(best_table)}

## Top 15 Cross-Validation Results

{dataframe_to_markdown(top_results)}

## Important Note

These are cross-validation results from the train-validation split only. The
test set is not used to choose the best combination.
"""

    validation_markdown_path.write_text(report_text)


def write_best_model_report(best_result, best_model_result, prediction_rows):
    best_test_table = pd.DataFrame(
        [
            {
                "feature_count": int(best_result["feature_count"]),
                "angle_scale": best_result["angle_scale"],
                "angle_scale_value": best_result["angle_scale_value"],
                "c_value": best_result["c_value"],
                "quantum_state_size": best_model_result["quantum_state_size"],
                "cv_accuracy": best_result["cv_accuracy"],
                "cv_stable_f1": best_result["cv_stable_f1"],
                "test_accuracy": best_model_result["test_metrics"]["accuracy"],
                "test_stable_precision": best_model_result["test_metrics"][
                    "stable_precision"
                ],
                "test_stable_recall": best_model_result["test_metrics"][
                    "stable_recall"
                ],
                "test_stable_f1": best_model_result["test_metrics"]["stable_f1"],
            }
        ]
    )

    feature_table = pd.DataFrame(
        {
            "selected_feature": best_model_result["selected_feature_columns"],
        }
    )

    report_text = f"""# QML Tuning Step 03: Best Model Test

Generated on: {date.today().isoformat()}

## Best Tuned QML Test Result

{dataframe_to_markdown(best_test_table)}

## Selected Features

{dataframe_to_markdown(feature_table)}

## Confusion Matrix

{dataframe_to_markdown(best_model_result["confusion_table"])}

## Classification Report

```text
{best_model_result["report_text"]}
```

## Prediction Output

`data/processed/qml tuned best predictions.csv`

Rows saved: {format_count(prediction_rows)}

## Kernel Matrix Shapes

- Train-validation kernel: {best_model_result["train_validation_kernel_shape"]}
- Test kernel: {best_model_result["test_kernel_shape"]}
"""

    best_model_markdown_path.write_text(report_text)


def write_summary_reports(tuning_results_dataframe, best_result, best_model_result):
    baseline_accuracy = 0.8100
    baseline_f1 = 0.8173
    same_data_xgboost_accuracy = 0.8300
    same_data_xgboost_f1 = 0.8283

    tuned_accuracy = best_model_result["test_metrics"]["accuracy"]
    tuned_f1 = best_model_result["test_metrics"]["stable_f1"]

    comparison_table = pd.DataFrame(
        [
            {
                "model": "Original QML baseline",
                "test_accuracy": baseline_accuracy,
                "test_stable_f1": baseline_f1,
            },
            {
                "model": "Tuned QML best model",
                "test_accuracy": tuned_accuracy,
                "test_stable_f1": tuned_f1,
            },
            {
                "model": "Same-data XGBoost baseline",
                "test_accuracy": same_data_xgboost_accuracy,
                "test_stable_f1": same_data_xgboost_f1,
            },
        ]
    )

    best_result_table = pd.DataFrame([best_result])
    top_results = tuning_results_dataframe.sort_values(
        by=[
            "cv_stable_f1",
            "cv_accuracy",
            "cv_stable_recall",
        ],
        ascending=[False, False, False],
    ).head(10)

    tuning_report_text = f"""# QML Tuning Results

Generated on: {date.today().isoformat()}

## Goal

Iterate QML hyperparameters and angle scales to find the best combination inside
the tested search space.

## Search Space

- Feature counts tested: {feature_count_options}
- Angle scales tested: pi/2, pi, 2pi
- SVM C values tested: {c_value_options}
- Total experiments: {format_count(len(tuning_results_dataframe))}

## Best Cross-Validation Combination

{dataframe_to_markdown(best_result_table)}

## Top 10 Cross-Validation Results

{dataframe_to_markdown(top_results)}

## Test Comparison

{dataframe_to_markdown(comparison_table)}

## Important Conclusion

This tuning finds the best QML combination inside our tested search space. It is
not a mathematical guarantee of the perfect QML model.
"""

    best_summary_text = f"""# QML Best Model Summary

Generated on: {date.today().isoformat()}

## Best Tuned Model

{dataframe_to_markdown(best_result_table)}

## Final Test Metrics

{dataframe_to_markdown(pd.DataFrame([best_model_result["test_metrics"]]))}

## Confusion Matrix

{dataframe_to_markdown(best_model_result["confusion_table"])}

## Comparison Against Previous Baselines

{dataframe_to_markdown(comparison_table)}

## Files Created

- `scripts/tune_qml_baseline.py`
- `data/processed/qml tuning results.csv`
- `data/processed/qml tuned best predictions.csv`
- `data/metadata/qml_tuning_results.md`
- `data/metadata/qml_best_model_summary.md`
- `data/metadata/qml_tuning_step_01_search_space.md`
- `data/metadata/qml_tuning_step_02_validation_results.md`
- `data/metadata/qml_tuning_step_03_best_model_test.md`
"""

    tuning_results_markdown_path.write_text(tuning_report_text)
    best_summary_markdown_path.write_text(best_summary_text)


def main():
    metadata_folder.mkdir(parents=True, exist_ok=True)
    processed_folder.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(input_csv_path)
    check_required_columns(dataframe)

    target = dataframe["target_is_stable"].to_numpy(dtype=int)
    row_indices = np.arange(len(dataframe))

    train_validation_indices, test_indices = train_test_split(
        row_indices,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )

    write_search_space_report(
        len(train_validation_indices),
        len(test_indices),
    )

    tuning_results_dataframe = run_tuning(
        dataframe,
        train_validation_indices,
    )
    tuning_results_dataframe.to_csv(tuning_results_csv_path, index=False)

    best_result = choose_best_result(tuning_results_dataframe)
    best_model_result = train_best_model(
        dataframe,
        train_validation_indices,
        test_indices,
        best_result,
    )
    prediction_dataframe = write_best_predictions(
        dataframe,
        test_indices,
        best_model_result,
    )

    write_validation_report(tuning_results_dataframe, best_result)
    write_best_model_report(best_result, best_model_result, len(prediction_dataframe))
    write_summary_reports(tuning_results_dataframe, best_result, best_model_result)

    print(f"Created: {tuning_results_csv_path}")
    print(f"Created: {best_predictions_csv_path}")
    print(f"Best CV stable F1: {best_result['cv_stable_f1']}")
    print(f"Best feature count: {int(best_result['feature_count'])}")
    print(f"Best angle scale: {best_result['angle_scale']}")
    print(f"Best C value: {best_result['c_value']}")
    print(f"Best test accuracy: {best_model_result['test_metrics']['accuracy']}")
    print(f"Best test stable F1: {best_model_result['test_metrics']['stable_f1']}")


if __name__ == "__main__":
    main()
