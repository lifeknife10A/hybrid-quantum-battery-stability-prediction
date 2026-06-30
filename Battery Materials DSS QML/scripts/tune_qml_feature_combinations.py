from datetime import date
from itertools import combinations
from pathlib import Path
import math

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
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
results_csv_path = processed_folder / "qml exhaustive feature combination results.csv"
top_results_csv_path = (
    processed_folder / "qml exhaustive feature combination top results.csv"
)
summary_markdown_path = metadata_folder / "qml_exhaustive_feature_tuning_summary.md"

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
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for _, dataframe_row in dataframe.iterrows():
        row_values = []
        for column_name in headers:
            value = dataframe_row[column_name]
            if pd.isna(value):
                value_text = ""
            elif isinstance(value, float):
                value_text = f"{value:.4f}"
            else:
                value_text = str(value)
            row_values.append(value_text.replace("|", "/"))
        lines.append("| " + " | ".join(row_values) + " |")

    return "\n".join(lines)


def format_count(value):
    return f"{int(value):,}"


def check_required_columns(dataframe):
    required_columns = ["target_is_stable"] + all_scaled_feature_columns
    missing_columns = []

    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")


def get_metrics(true_labels, predicted_labels):
    return {
        "accuracy": accuracy_score(true_labels, predicted_labels),
        "stable_precision": precision_score(
            true_labels,
            predicted_labels,
            zero_division=0,
        ),
        "stable_recall": recall_score(
            true_labels,
            predicted_labels,
            zero_division=0,
        ),
        "stable_f1": f1_score(
            true_labels,
            predicted_labels,
            zero_division=0,
        ),
    }


def create_single_feature_kernel(feature_values, angle_scale_value):
    feature_column = feature_values.reshape(-1, 1)
    angle_difference = angle_scale_value * (feature_column - feature_column.T)
    return np.cos(angle_difference / 2.0) ** 2


def create_feature_kernel_dictionary(feature_dataframe):
    kernel_dictionary = {}

    for angle_option in angle_scale_options:
        angle_scale_name = angle_option["angle_scale_name"]
        angle_scale_value = angle_option["angle_scale_value"]

        for feature_name in all_scaled_feature_columns:
            feature_values = feature_dataframe[feature_name].to_numpy(dtype=float)
            kernel_dictionary[(angle_scale_name, feature_name)] = (
                create_single_feature_kernel(feature_values, angle_scale_value)
            )

    return kernel_dictionary


def create_combination_kernel(kernel_dictionary, angle_scale_name, feature_names):
    full_kernel_matrix = None

    for feature_name in feature_names:
        single_feature_kernel = kernel_dictionary[(angle_scale_name, feature_name)]
        if full_kernel_matrix is None:
            full_kernel_matrix = single_feature_kernel.copy()
        else:
            full_kernel_matrix = full_kernel_matrix * single_feature_kernel

    return full_kernel_matrix


def create_feature_combinations():
    feature_combination_rows = []

    for feature_count in feature_count_options:
        for feature_names in combinations(all_scaled_feature_columns, feature_count):
            feature_combination_rows.append(
                {
                    "feature_count": feature_count,
                    "feature_names": list(feature_names),
                }
            )

    return feature_combination_rows


def evaluate_one_configuration(
    full_kernel_matrix,
    target,
    cross_validator,
    c_value,
):
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
    return {
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


def run_exhaustive_tuning(dataframe, train_validation_indices):
    target = dataframe["target_is_stable"].to_numpy(dtype=int)
    train_validation_target = target[train_validation_indices]
    train_validation_features = dataframe.iloc[train_validation_indices][
        all_scaled_feature_columns
    ].copy()
    kernel_dictionary = create_feature_kernel_dictionary(train_validation_features)
    feature_combination_rows = create_feature_combinations()
    total_configurations = (
        len(feature_combination_rows) * len(angle_scale_options) * len(c_value_options)
    )

    result_rows = []
    completed_configurations = 0
    cross_validator = StratifiedKFold(
        n_splits=cross_validation_splits,
        shuffle=True,
        random_state=random_state,
    )

    for feature_combination_row in feature_combination_rows:
        feature_count = feature_combination_row["feature_count"]
        feature_names = feature_combination_row["feature_names"]

        for angle_option in angle_scale_options:
            angle_scale_name = angle_option["angle_scale_name"]
            angle_scale_value = angle_option["angle_scale_value"]
            full_kernel_matrix = create_combination_kernel(
                kernel_dictionary,
                angle_scale_name,
                feature_names,
            )

            for c_value in c_value_options:
                metric_values = evaluate_one_configuration(
                    full_kernel_matrix,
                    train_validation_target,
                    cross_validator,
                    c_value,
                )
                completed_configurations += 1

                result_rows.append(
                    {
                        "feature_count": feature_count,
                        "feature_names": "; ".join(feature_names),
                        "angle_scale": angle_scale_name,
                        "angle_scale_value": round(angle_scale_value, 6),
                        "c_value": c_value,
                        "quantum_state_size": 2**feature_count,
                        "train_validation_rows": len(train_validation_target),
                        "cross_validation_splits": cross_validation_splits,
                        "cv_accuracy": metric_values["cv_accuracy"],
                        "cv_stable_precision": metric_values[
                            "cv_stable_precision"
                        ],
                        "cv_stable_recall": metric_values["cv_stable_recall"],
                        "cv_stable_f1": metric_values["cv_stable_f1"],
                    }
                )

                if completed_configurations % 250 == 0:
                    print(
                        "Completed "
                        f"{completed_configurations} / {total_configurations}",
                        flush=True,
                    )

    return pd.DataFrame(result_rows)


def sort_results(results_dataframe):
    return results_dataframe.sort_values(
        by=[
            "cv_stable_f1",
            "cv_accuracy",
            "cv_stable_recall",
            "feature_count",
            "c_value",
        ],
        ascending=[False, False, False, True, True],
    ).reset_index(drop=True)


def write_summary(
    results_dataframe,
    top_results_dataframe,
    train_validation_rows,
    test_rows,
):
    best_result = top_results_dataframe.iloc[0]

    feature_combination_count = len(create_feature_combinations())
    total_configurations = len(results_dataframe)

    summary_text = f"""# QML Exhaustive Feature Combination Tuning Summary

Generated on: {date.today().isoformat()}

## Goal

This step tests true feature combinations for QML tuning. The earlier tuning
tested ordered top-N features. This step checks every feature combination for
the selected feature counts.

## Search Space

- Feature counts: {feature_count_options}
- Available scaled features: {format_count(len(all_scaled_feature_columns))}
- Feature combinations tested: {format_count(feature_combination_count)}
- Angle scales: `pi/2`, `pi`, `2pi`
- SVM C values: {c_value_options}
- Total saved configurations: {format_count(total_configurations)}
- Cross-validation folds: {cross_validation_splits}
- Train-validation rows: {format_count(train_validation_rows)}
- Untouched test rows: {format_count(test_rows)}

## Best Cross-Validation Result

{dataframe_to_markdown(pd.DataFrame([best_result]))}

## Top 20 Results

{dataframe_to_markdown(top_results_dataframe)}

## Output Files

- `data/processed/qml exhaustive feature combination results.csv`
- `data/processed/qml exhaustive feature combination top results.csv`
- `data/metadata/qml_exhaustive_feature_tuning_summary.md`

## Simple Explanation

For each feature count, the script tries all possible feature groups. Each
feature group is tested with every angle scale and every SVM C value. The best
row is selected by highest cross-validation stable F1, then accuracy, then
stable recall.
"""

    summary_markdown_path.write_text(summary_text, encoding="utf-8")


def main():
    processed_folder.mkdir(parents=True, exist_ok=True)
    metadata_folder.mkdir(parents=True, exist_ok=True)

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

    results_dataframe = run_exhaustive_tuning(
        dataframe,
        train_validation_indices,
    )
    sorted_results_dataframe = sort_results(results_dataframe)
    top_results_dataframe = sorted_results_dataframe.head(20).copy()

    sorted_results_dataframe.to_csv(results_csv_path, index=False)
    top_results_dataframe.to_csv(top_results_csv_path, index=False)

    write_summary(
        sorted_results_dataframe,
        top_results_dataframe,
        len(train_validation_indices),
        len(test_indices),
    )

    best_result = top_results_dataframe.iloc[0]

    print(f"Created: {results_csv_path}")
    print(f"Created: {top_results_csv_path}")
    print(f"Created: {summary_markdown_path}")
    print(f"Total configurations: {len(sorted_results_dataframe)}")
    print(f"Best feature count: {int(best_result['feature_count'])}")
    print(f"Best features: {best_result['feature_names']}")
    print(f"Best angle scale: {best_result['angle_scale']}")
    print(f"Best C value: {best_result['c_value']}")
    print(f"Best CV stable F1: {best_result['cv_stable_f1']}")
    print(f"Best CV accuracy: {best_result['cv_accuracy']}")


if __name__ == "__main__":
    main()
