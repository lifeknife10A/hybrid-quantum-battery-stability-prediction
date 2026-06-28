from datetime import date
from pathlib import Path
import math

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

input_csv_path = processed_folder / "lithium india scored.csv"
improved_dataset_csv_path = processed_folder / "improved qml feature pca.csv"
tuning_results_csv_path = processed_folder / "improved qml tuning results.csv"
best_predictions_csv_path = processed_folder / "improved qml best predictions.csv"
threshold_results_csv_path = processed_folder / "improved qml threshold results.csv"
threshold_predictions_csv_path = (
    processed_folder / "improved qml threshold predictions.csv"
)

section_summary_markdown_path = metadata_folder / "improved_qml_section_summary.md"
step_01_markdown_path = metadata_folder / "improved_qml_step_01_feature_importance.md"
step_02_markdown_path = metadata_folder / "improved_qml_step_02_pca_dataset.md"
step_03_markdown_path = metadata_folder / "improved_qml_step_03_tuning_results.md"
step_04_markdown_path = metadata_folder / "improved_qml_step_04_best_model.md"
step_05_markdown_path = metadata_folder / "improved_qml_step_05_threshold_experiment.md"

random_state = 42
maximum_rows_per_class = 500
test_size = 0.20
cross_validation_splits = 4
top_feature_count_for_pca = 16
maximum_pca_components = 8

pca_component_count_options = [4, 6, 8]
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
threshold_options = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
kernel_options = [
    {
        "kernel_name": "product",
        "entanglement_strength": 0.0,
    },
    {
        "kernel_name": "entangled_pi_over_2",
        "entanglement_strength": math.pi / 2,
    },
    {
        "kernel_name": "entangled_pi",
        "entanglement_strength": math.pi,
    },
]

metadata_columns = [
    "material_id",
    "formula",
    "battery_family",
    "india_feasibility_score",
    "india_decision_label",
]

numeric_feature_columns = [
    "space_group_number",
    "band_gap",
    "formation_energy_per_atom",
    "number_of_elements",
]

boolean_feature_columns = [
    "is_metal",
    "theoretical",
    "deprecated",
    "has_o",
    "has_fe",
    "has_p",
    "has_mn",
    "has_co",
    "has_ni",
    "has_ti",
    "has_c",
    "has_si",
    "has_s",
    "has_al",
    "has_la",
    "has_zr",
    "has_f",
    "has_cu",
    "has_high_caution_element",
]

categorical_feature_columns = [
    "crystal_system",
    "battery_family",
]

target_column = "is_stable"


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


def unique_column_list(column_names):
    unique_names = []

    for column_name in column_names:
        if column_name not in unique_names:
            unique_names.append(column_name)

    return unique_names


def check_required_columns(dataframe):
    required_columns = unique_column_list(
        metadata_columns
        + numeric_feature_columns
        + boolean_feature_columns
        + categorical_feature_columns
        + [target_column]
    )

    missing_columns = []
    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing_text}")


def convert_boolean_to_integer(dataframe, column_name):
    if dataframe[column_name].dtype == bool:
        dataframe[column_name] = dataframe[column_name].astype(int)
        return

    converted_values = (
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
    )
    dataframe[column_name] = converted_values.astype(int)


def prepare_clean_encoded_dataset(dataframe):
    selected_columns = unique_column_list(
        metadata_columns
        + numeric_feature_columns
        + boolean_feature_columns
        + categorical_feature_columns
        + [target_column]
    )
    selected_dataframe = dataframe[selected_columns].copy()
    rows_before_cleaning = len(selected_dataframe)

    selected_dataframe = selected_dataframe.dropna(
        subset=numeric_feature_columns + [target_column]
    ).copy()

    for column_name in boolean_feature_columns:
        convert_boolean_to_integer(selected_dataframe, column_name)

    convert_boolean_to_integer(selected_dataframe, target_column)
    selected_dataframe["target_is_stable"] = selected_dataframe[target_column]

    feature_dataframe = selected_dataframe[
        numeric_feature_columns + boolean_feature_columns + categorical_feature_columns
    ].copy()

    for column_name in numeric_feature_columns + boolean_feature_columns:
        feature_dataframe[column_name] = pd.to_numeric(
            feature_dataframe[column_name],
            errors="coerce",
        )

    feature_dataframe = pd.get_dummies(
        feature_dataframe,
        columns=categorical_feature_columns,
        dtype=int,
    )

    rows_after_cleaning = len(selected_dataframe)
    removed_rows = rows_before_cleaning - rows_after_cleaning

    return selected_dataframe, feature_dataframe, removed_rows


def balance_dataset(clean_dataframe, feature_dataframe):
    stable_indices = clean_dataframe[clean_dataframe["target_is_stable"] == 1].index
    unstable_indices = clean_dataframe[clean_dataframe["target_is_stable"] == 0].index
    rows_per_class = min(
        maximum_rows_per_class,
        len(stable_indices),
        len(unstable_indices),
    )

    sampled_stable_indices = pd.Series(stable_indices).sample(
        n=rows_per_class,
        random_state=random_state,
    )
    sampled_unstable_indices = pd.Series(unstable_indices).sample(
        n=rows_per_class,
        random_state=random_state,
    )

    sampled_indices = pd.concat(
        [sampled_stable_indices, sampled_unstable_indices],
        ignore_index=True,
    )
    sampled_indices = sampled_indices.sample(
        frac=1,
        random_state=random_state,
    ).to_list()

    balanced_dataframe = clean_dataframe.loc[sampled_indices].reset_index(drop=True)
    balanced_feature_dataframe = feature_dataframe.loc[sampled_indices].reset_index(
        drop=True
    )

    return balanced_dataframe, balanced_feature_dataframe, rows_per_class


def split_indices(target):
    row_indices = np.arange(len(target))
    train_validation_indices, test_indices = train_test_split(
        row_indices,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )
    return train_validation_indices, test_indices


def rank_features(feature_dataframe, target, train_validation_indices):
    ranking_model = RandomForestClassifier(
        n_estimators=300,
        max_depth=6,
        random_state=random_state,
        n_jobs=4,
        class_weight="balanced",
    )
    ranking_model.fit(
        feature_dataframe.iloc[train_validation_indices],
        target[train_validation_indices],
    )

    importance_dataframe = pd.DataFrame(
        {
            "feature": feature_dataframe.columns,
            "importance": ranking_model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    importance_dataframe["rank"] = range(1, len(importance_dataframe) + 1)
    selected_feature_names = (
        importance_dataframe.head(top_feature_count_for_pca)["feature"].tolist()
    )

    return importance_dataframe, selected_feature_names


def create_pca_dataset(
    balanced_dataframe,
    feature_dataframe,
    selected_feature_names,
    train_validation_indices,
):
    selected_feature_dataframe = feature_dataframe[selected_feature_names].copy()

    scaler = MinMaxScaler()
    train_validation_scaled = scaler.fit_transform(
        selected_feature_dataframe.iloc[train_validation_indices]
    )
    all_scaled = scaler.transform(selected_feature_dataframe)

    pca_model = PCA(
        n_components=maximum_pca_components,
        random_state=random_state,
    )
    train_validation_pca = pca_model.fit_transform(train_validation_scaled)
    all_pca = pca_model.transform(all_scaled)

    pca_scaler = MinMaxScaler()
    pca_scaler.fit(train_validation_pca)
    all_pca_scaled = pca_scaler.transform(all_pca)

    pca_column_names = []
    output_dataframe = balanced_dataframe[metadata_columns].copy()
    output_dataframe["target_is_stable"] = balanced_dataframe["target_is_stable"]

    for component_index in range(maximum_pca_components):
        column_name = f"improved_pca_{component_index + 1}"
        pca_column_names.append(column_name)
        output_dataframe[column_name] = np.round(all_pca_scaled[:, component_index], 6)

    explained_variance_dataframe = pd.DataFrame(
        {
            "component": pca_column_names,
            "explained_variance_ratio": np.round(
                pca_model.explained_variance_ratio_,
                6,
            ),
        }
    )
    explained_variance_dataframe["cumulative_explained_variance"] = np.round(
        explained_variance_dataframe["explained_variance_ratio"].cumsum(),
        6,
    )

    return output_dataframe, pca_column_names, explained_variance_dataframe


def get_bit_matrix(number_of_features):
    state_count = 2**number_of_features
    bit_matrix = np.zeros((state_count, number_of_features), dtype=float)

    for state_index in range(state_count):
        for feature_index in range(number_of_features):
            bit_value = (state_index >> (number_of_features - feature_index - 1)) & 1
            bit_matrix[state_index, feature_index] = bit_value

    return bit_matrix


def create_quantum_state_table(
    feature_table,
    angle_scale_value,
    entanglement_strength,
):
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

        if entanglement_strength != 0.0:
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


def apply_probability_threshold(probabilities, stable_threshold):
    return (probabilities >= stable_threshold).astype(int)


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


def run_cross_validation_group(
    pca_component_count,
    kernel_name,
    entanglement_strength,
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

            classifier = SVC(
                kernel="precomputed",
                C=c_value,
                probability=False,
                random_state=random_state,
            )
            classifier.fit(train_kernel_matrix, target[train_positions])
            predicted_labels = classifier.predict(validation_kernel_matrix)
            fold_metric_rows.append(
                get_metrics(target[validation_positions], predicted_labels)
            )

        fold_metrics_dataframe = pd.DataFrame(fold_metric_rows)

        result_rows.append(
            {
                "pca_component_count": pca_component_count,
                "kernel_name": kernel_name,
                "entanglement_strength": round(entanglement_strength, 6),
                "angle_scale": angle_scale_name,
                "angle_scale_value": round(angle_scale_value, 6),
                "c_value": c_value,
                "quantum_state_size": 2**pca_component_count,
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


def run_tuning(output_dataframe, pca_column_names, train_validation_indices):
    target = output_dataframe["target_is_stable"].to_numpy(dtype=int)
    train_validation_target = target[train_validation_indices]
    all_result_rows = []
    cross_validator = StratifiedKFold(
        n_splits=cross_validation_splits,
        shuffle=True,
        random_state=random_state,
    )

    for pca_component_count in pca_component_count_options:
        selected_pca_columns = pca_column_names[:pca_component_count]
        feature_table = output_dataframe[selected_pca_columns].to_numpy(dtype=float)
        train_validation_features = feature_table[train_validation_indices]

        for angle_option in angle_scale_options:
            for kernel_option in kernel_options:
                train_validation_states = create_quantum_state_table(
                    train_validation_features,
                    angle_option["angle_scale_value"],
                    kernel_option["entanglement_strength"],
                )
                full_kernel_matrix = create_kernel_matrix(
                    train_validation_states,
                    train_validation_states,
                )

                result_rows = run_cross_validation_group(
                    pca_component_count,
                    kernel_option["kernel_name"],
                    kernel_option["entanglement_strength"],
                    angle_option["angle_scale_name"],
                    angle_option["angle_scale_value"],
                    full_kernel_matrix,
                    train_validation_target,
                    cross_validator,
                )
                all_result_rows.extend(result_rows)

    return pd.DataFrame(all_result_rows)


def choose_best_result(tuning_results_dataframe):
    sorted_dataframe = tuning_results_dataframe.sort_values(
        by=[
            "cv_stable_f1",
            "cv_accuracy",
            "cv_stable_recall",
            "pca_component_count",
            "c_value",
        ],
        ascending=[False, False, False, True, True],
    )
    return sorted_dataframe.iloc[0].to_dict()


def train_best_model(output_dataframe, pca_column_names, train_validation_indices, test_indices, best_result):
    pca_component_count = int(best_result["pca_component_count"])
    selected_pca_columns = pca_column_names[:pca_component_count]
    feature_table = output_dataframe[selected_pca_columns].to_numpy(dtype=float)
    target = output_dataframe["target_is_stable"].to_numpy(dtype=int)

    x_train_validation = feature_table[train_validation_indices]
    x_test = feature_table[test_indices]
    y_train_validation = target[train_validation_indices]
    y_test = target[test_indices]

    angle_scale_value = float(best_result["angle_scale_value"])
    entanglement_strength = float(best_result["entanglement_strength"])
    c_value = float(best_result["c_value"])

    train_validation_states = create_quantum_state_table(
        x_train_validation,
        angle_scale_value,
        entanglement_strength,
    )
    test_states = create_quantum_state_table(
        x_test,
        angle_scale_value,
        entanglement_strength,
    )

    train_validation_kernel_matrix = create_kernel_matrix(
        train_validation_states,
        train_validation_states,
    )
    test_kernel_matrix = create_kernel_matrix(test_states, train_validation_states)

    classifier = SVC(
        kernel="precomputed",
        C=c_value,
        probability=True,
        random_state=random_state,
    )
    classifier.fit(train_validation_kernel_matrix, y_train_validation)

    predicted_labels = classifier.predict(test_kernel_matrix)
    predicted_probabilities = classifier.predict_proba(test_kernel_matrix)[:, 1]
    test_metrics = get_metrics(y_test, predicted_labels)
    report_text = classification_report(
        y_test,
        predicted_labels,
        target_names=["unstable", "stable"],
        zero_division=0,
    )
    confusion_table = get_confusion_table(y_test, predicted_labels)

    return {
        "selected_pca_columns": selected_pca_columns,
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


def write_best_predictions(output_dataframe, test_indices, best_model_result):
    prediction_dataframe = output_dataframe.iloc[test_indices][metadata_columns].copy()
    prediction_dataframe["target_is_stable"] = best_model_result["y_test"]
    prediction_dataframe["improved_qml_predicted_label"] = best_model_result[
        "predicted_labels"
    ]
    prediction_dataframe["improved_qml_stable_probability"] = np.round(
        best_model_result["predicted_probabilities"],
        6,
    )
    prediction_dataframe.to_csv(best_predictions_csv_path, index=False)
    return prediction_dataframe


def run_threshold_experiment(
    output_dataframe,
    pca_column_names,
    train_validation_indices,
    test_indices,
    best_result,
    best_model_result,
):
    pca_component_count = int(best_result["pca_component_count"])
    selected_pca_columns = pca_column_names[:pca_component_count]
    feature_table = output_dataframe[selected_pca_columns].to_numpy(dtype=float)
    target = output_dataframe["target_is_stable"].to_numpy(dtype=int)

    x_train_validation = feature_table[train_validation_indices]
    y_train_validation = target[train_validation_indices]
    y_test = target[test_indices]

    angle_scale_value = float(best_result["angle_scale_value"])
    entanglement_strength = float(best_result["entanglement_strength"])
    c_value = float(best_result["c_value"])

    threshold_metric_rows = []
    cross_validator = StratifiedKFold(
        n_splits=cross_validation_splits,
        shuffle=True,
        random_state=random_state,
    )

    for stable_threshold in threshold_options:
        fold_metric_rows = []

        for train_positions, validation_positions in cross_validator.split(
            x_train_validation,
            y_train_validation,
        ):
            x_train = x_train_validation[train_positions]
            x_validation = x_train_validation[validation_positions]
            y_train = y_train_validation[train_positions]
            y_validation = y_train_validation[validation_positions]

            train_states = create_quantum_state_table(
                x_train,
                angle_scale_value,
                entanglement_strength,
            )
            validation_states = create_quantum_state_table(
                x_validation,
                angle_scale_value,
                entanglement_strength,
            )
            train_kernel_matrix = create_kernel_matrix(train_states, train_states)
            validation_kernel_matrix = create_kernel_matrix(
                validation_states,
                train_states,
            )

            classifier = SVC(
                kernel="precomputed",
                C=c_value,
                probability=True,
                random_state=random_state,
            )
            classifier.fit(train_kernel_matrix, y_train)
            stable_probabilities = classifier.predict_proba(validation_kernel_matrix)[
                :,
                1,
            ]
            predicted_labels = apply_probability_threshold(
                stable_probabilities,
                stable_threshold,
            )
            fold_metric_rows.append(get_metrics(y_validation, predicted_labels))

        fold_metrics_dataframe = pd.DataFrame(fold_metric_rows)
        threshold_metric_rows.append(
            {
                "stable_threshold": stable_threshold,
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

    threshold_results_dataframe = pd.DataFrame(threshold_metric_rows)
    sorted_threshold_results = threshold_results_dataframe.sort_values(
        by=[
            "cv_stable_f1",
            "cv_accuracy",
            "cv_stable_recall",
            "stable_threshold",
        ],
        ascending=[False, False, False, True],
    )
    best_threshold_result = sorted_threshold_results.iloc[0].to_dict()

    selected_threshold = float(best_threshold_result["stable_threshold"])
    threshold_test_predictions = apply_probability_threshold(
        best_model_result["predicted_probabilities"],
        selected_threshold,
    )
    threshold_test_metrics = get_metrics(y_test, threshold_test_predictions)
    threshold_report_text = classification_report(
        y_test,
        threshold_test_predictions,
        target_names=["unstable", "stable"],
        zero_division=0,
    )
    threshold_confusion_table = get_confusion_table(y_test, threshold_test_predictions)

    threshold_test_result = {
        "selected_threshold": selected_threshold,
        "y_test": y_test,
        "predicted_labels": threshold_test_predictions,
        "predicted_probabilities": best_model_result["predicted_probabilities"],
        "test_metrics": threshold_test_metrics,
        "report_text": threshold_report_text,
        "confusion_table": threshold_confusion_table,
    }

    return threshold_results_dataframe, best_threshold_result, threshold_test_result


def write_threshold_predictions(output_dataframe, test_indices, threshold_test_result):
    prediction_dataframe = output_dataframe.iloc[test_indices][metadata_columns].copy()
    prediction_dataframe["target_is_stable"] = threshold_test_result["y_test"]
    prediction_dataframe["threshold_qml_predicted_label"] = threshold_test_result[
        "predicted_labels"
    ]
    prediction_dataframe["threshold_qml_stable_probability"] = np.round(
        threshold_test_result["predicted_probabilities"],
        6,
    )
    prediction_dataframe["selected_stable_threshold"] = threshold_test_result[
        "selected_threshold"
    ]
    prediction_dataframe.to_csv(threshold_predictions_csv_path, index=False)
    return prediction_dataframe


def write_reports(
    rows_before_cleaning,
    rows_removed,
    rows_per_class,
    importance_dataframe,
    selected_feature_names,
    explained_variance_dataframe,
    output_dataframe,
    tuning_results_dataframe,
    best_result,
    best_model_result,
    prediction_rows,
    threshold_results_dataframe,
    best_threshold_result,
    threshold_test_result,
    threshold_prediction_rows,
):
    top_importance_dataframe = importance_dataframe.head(20).copy()
    selected_feature_dataframe = pd.DataFrame(
        {
            "selected_feature_for_pca": selected_feature_names,
        }
    )
    top_tuning_results = tuning_results_dataframe.sort_values(
        by=["cv_stable_f1", "cv_accuracy", "cv_stable_recall"],
        ascending=[False, False, False],
    ).head(15)
    best_result_table = pd.DataFrame([best_result])
    best_test_table = pd.DataFrame(
        [
            {
                "pca_component_count": int(best_result["pca_component_count"]),
                "kernel_name": best_result["kernel_name"],
                "angle_scale": best_result["angle_scale"],
                "c_value": best_result["c_value"],
                "quantum_state_size": best_model_result["quantum_state_size"],
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
    best_threshold_table = pd.DataFrame([best_threshold_result])
    threshold_test_table = pd.DataFrame(
        [
            {
                "selected_stable_threshold": threshold_test_result[
                    "selected_threshold"
                ],
                "test_accuracy": threshold_test_result["test_metrics"]["accuracy"],
                "test_stable_precision": threshold_test_result["test_metrics"][
                    "stable_precision"
                ],
                "test_stable_recall": threshold_test_result["test_metrics"][
                    "stable_recall"
                ],
                "test_stable_f1": threshold_test_result["test_metrics"]["stable_f1"],
            }
        ]
    )

    comparison_dataframe = pd.DataFrame(
        [
            {
                "model": "Original QML baseline",
                "test_accuracy": 0.8100,
                "test_stable_f1": 0.8173,
            },
            {
                "model": "Tuned QML baseline",
                "test_accuracy": 0.8200,
                "test_stable_f1": 0.8269,
            },
            {
                "model": "Improved QML separate experiment",
                "test_accuracy": best_model_result["test_metrics"]["accuracy"],
                "test_stable_f1": best_model_result["test_metrics"]["stable_f1"],
            },
            {
                "model": "Improved QML with threshold tuning",
                "test_accuracy": threshold_test_result["test_metrics"]["accuracy"],
                "test_stable_f1": threshold_test_result["test_metrics"]["stable_f1"],
            },
            {
                "model": "Same-data XGBoost baseline",
                "test_accuracy": 0.8300,
                "test_stable_f1": 0.8283,
            },
        ]
    )

    step_01_text = f"""# Improved QML Step 01: Feature Importance

Generated on: {date.today().isoformat()}

## Separate Section

This is a separate improved-QML experiment. It does not replace the original QML
baseline or tuned-QML baseline.

## Feature Rules

- Used safe non-leakage material features.
- Did not use `energy_above_hull` as a training feature.
- Did not use `india_feasibility_score` or `india_decision_label` as training
  features.
- Used Random Forest feature importance on the train-validation split only.

## Rows

- Rows before cleaning: {format_count(rows_before_cleaning)}
- Rows removed for missing numeric values: {format_count(rows_removed)}
- Balanced rows per class: {format_count(rows_per_class)}
- Final balanced rows: {format_count(len(output_dataframe))}

## Top Feature Importances

{dataframe_to_markdown(top_importance_dataframe)}

## Features Selected For PCA

{dataframe_to_markdown(selected_feature_dataframe)}
"""

    step_02_text = f"""# Improved QML Step 02: PCA Dataset

Generated on: {date.today().isoformat()}

## Output Dataset

`data/processed/improved qml feature pca.csv`

## Purpose

The original QML dataset used hand-selected features. This improved experiment
uses feature importance first, then PCA to compress the strongest features into
small quantum-ready component sets.

## Dataset Size

- Rows: {format_count(len(output_dataframe))}
- Columns: {format_count(len(output_dataframe.columns))}
- PCA components saved: {maximum_pca_components}

## PCA Explained Variance

{dataframe_to_markdown(explained_variance_dataframe)}
"""

    step_03_text = f"""# Improved QML Step 03: Tuning Results

Generated on: {date.today().isoformat()}

## Output

`data/processed/improved qml tuning results.csv`

## Search Space

- PCA component counts: {pca_component_count_options}
- Angle scales: pi/2, pi, 2pi
- Kernel types: product, entangled_pi_over_2, entangled_pi
- SVM C values: {c_value_options}
- Total experiments: {format_count(len(tuning_results_dataframe))}

## Best Cross-Validation Result

{dataframe_to_markdown(best_result_table)}

## Top 15 Results

{dataframe_to_markdown(top_tuning_results)}
"""

    step_04_text = f"""# Improved QML Step 04: Best Model

Generated on: {date.today().isoformat()}

## Best Improved QML Test Result

{dataframe_to_markdown(best_test_table)}

## Confusion Matrix

{dataframe_to_markdown(best_model_result["confusion_table"])}

## Classification Report

```text
{best_model_result["report_text"]}
```

## Prediction Output

`data/processed/improved qml best predictions.csv`

Rows saved: {format_count(prediction_rows)}

## Comparison

{dataframe_to_markdown(comparison_dataframe)}
"""

    step_05_text = f"""# Improved QML Step 05: Threshold Experiment

Generated on: {date.today().isoformat()}

## Purpose

The QML model gives a stable-class probability. The normal prediction rule uses
`0.50` as the cutoff:

- probability >= 0.50 means stable
- probability < 0.50 means unstable

This experiment checks whether a different cutoff gives better stable-class
F1-score. The threshold is selected using cross-validation on the
train-validation split only. The test set is used only after the threshold is
selected.

## Thresholds Tested

{threshold_options}

## Cross-Validation Results

{dataframe_to_markdown(threshold_results_dataframe)}

## Best Cross-Validation Threshold

{dataframe_to_markdown(best_threshold_table)}

## Test Result With Selected Threshold

{dataframe_to_markdown(threshold_test_table)}

## Confusion Matrix

{dataframe_to_markdown(threshold_test_result["confusion_table"])}

## Classification Report

```text
{threshold_test_result["report_text"]}
```

## Prediction Output

`data/processed/improved qml threshold predictions.csv`

Rows saved: {format_count(threshold_prediction_rows)}
"""

    section_summary_text = f"""# Improved QML Separate Section Summary

Generated on: {date.today().isoformat()}

## Goal

Try a separate improved-QML experiment using feature importance, PCA, and an
optional entangled quantum-kernel simulation.

## Files Created

- `scripts/run_improved_qml_experiments.py`
- `data/processed/improved qml feature pca.csv`
- `data/processed/improved qml tuning results.csv`
- `data/processed/improved qml best predictions.csv`
- `data/processed/improved qml threshold results.csv`
- `data/processed/improved qml threshold predictions.csv`
- `data/metadata/improved_qml_step_01_feature_importance.md`
- `data/metadata/improved_qml_step_02_pca_dataset.md`
- `data/metadata/improved_qml_step_03_tuning_results.md`
- `data/metadata/improved_qml_step_04_best_model.md`
- `data/metadata/improved_qml_step_05_threshold_experiment.md`

## Best Improved QML Result

{dataframe_to_markdown(best_test_table)}

## Threshold Experiment Result

{dataframe_to_markdown(threshold_test_table)}

## Comparison Against Existing Results

{dataframe_to_markdown(comparison_dataframe)}

## Interpretation

This experiment is useful because it tests a more advanced QML preparation
route. The result should be reported as a separate experiment, not as a
replacement for the original baseline.
"""

    step_01_markdown_path.write_text(step_01_text)
    step_02_markdown_path.write_text(step_02_text)
    step_03_markdown_path.write_text(step_03_text)
    step_04_markdown_path.write_text(step_04_text)
    step_05_markdown_path.write_text(step_05_text)
    section_summary_markdown_path.write_text(section_summary_text)


def main():
    metadata_folder.mkdir(parents=True, exist_ok=True)
    processed_folder.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(input_csv_path)
    check_required_columns(dataframe)
    rows_before_cleaning = len(dataframe)

    clean_dataframe, encoded_feature_dataframe, rows_removed = prepare_clean_encoded_dataset(
        dataframe
    )
    balanced_dataframe, balanced_feature_dataframe, rows_per_class = balance_dataset(
        clean_dataframe,
        encoded_feature_dataframe,
    )

    target = balanced_dataframe["target_is_stable"].to_numpy(dtype=int)
    train_validation_indices, test_indices = split_indices(target)

    importance_dataframe, selected_feature_names = rank_features(
        balanced_feature_dataframe,
        target,
        train_validation_indices,
    )
    output_dataframe, pca_column_names, explained_variance_dataframe = create_pca_dataset(
        balanced_dataframe,
        balanced_feature_dataframe,
        selected_feature_names,
        train_validation_indices,
    )
    output_dataframe.to_csv(improved_dataset_csv_path, index=False)

    tuning_results_dataframe = run_tuning(
        output_dataframe,
        pca_column_names,
        train_validation_indices,
    )
    tuning_results_dataframe.to_csv(tuning_results_csv_path, index=False)

    best_result = choose_best_result(tuning_results_dataframe)
    best_model_result = train_best_model(
        output_dataframe,
        pca_column_names,
        train_validation_indices,
        test_indices,
        best_result,
    )
    prediction_dataframe = write_best_predictions(
        output_dataframe,
        test_indices,
        best_model_result,
    )
    (
        threshold_results_dataframe,
        best_threshold_result,
        threshold_test_result,
    ) = run_threshold_experiment(
        output_dataframe,
        pca_column_names,
        train_validation_indices,
        test_indices,
        best_result,
        best_model_result,
    )
    threshold_results_dataframe.to_csv(threshold_results_csv_path, index=False)
    threshold_prediction_dataframe = write_threshold_predictions(
        output_dataframe,
        test_indices,
        threshold_test_result,
    )

    write_reports(
        rows_before_cleaning,
        rows_removed,
        rows_per_class,
        importance_dataframe,
        selected_feature_names,
        explained_variance_dataframe,
        output_dataframe,
        tuning_results_dataframe,
        best_result,
        best_model_result,
        len(prediction_dataframe),
        threshold_results_dataframe,
        best_threshold_result,
        threshold_test_result,
        len(threshold_prediction_dataframe),
    )

    print(f"Created: {improved_dataset_csv_path}")
    print(f"Created: {tuning_results_csv_path}")
    print(f"Created: {best_predictions_csv_path}")
    print(f"Created: {threshold_results_csv_path}")
    print(f"Created: {threshold_predictions_csv_path}")
    print(f"Best CV stable F1: {best_result['cv_stable_f1']}")
    print(f"Best PCA components: {int(best_result['pca_component_count'])}")
    print(f"Best kernel: {best_result['kernel_name']}")
    print(f"Best angle scale: {best_result['angle_scale']}")
    print(f"Best C value: {best_result['c_value']}")
    print(f"Best test accuracy: {best_model_result['test_metrics']['accuracy']}")
    print(f"Best test stable F1: {best_model_result['test_metrics']['stable_f1']}")
    print(f"Best threshold: {best_threshold_result['stable_threshold']}")
    print(
        "Threshold test accuracy: "
        f"{threshold_test_result['test_metrics']['accuracy']}"
    )
    print(
        "Threshold test stable F1: "
        f"{threshold_test_result['test_metrics']['stable_f1']}"
    )


if __name__ == "__main__":
    main()
