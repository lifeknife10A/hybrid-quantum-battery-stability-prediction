from pathlib import Path
import base64
import io
import json
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"
notebook_path = project_folder / "Main.ipynb"

lithium_scored_path = processed_folder / "lithium india scored.csv"
final_shortlist_path = processed_folder / "final india battery shortlist.csv"
dss_family_ranking_path = (
    processed_folder / "dss battery family recommendation ranking.csv"
)
dss_material_ranking_path = processed_folder / "dss material recommendation ranking.csv"
dss_compound_ranking_path = processed_folder / "dss compound recommendation ranking.csv"
qml_ready_path = processed_folder / "qml_ready_lithium_india.csv"
qml_predictions_path = processed_folder / "qml baseline predictions.csv"
tuned_qml_predictions_path = processed_folder / "qml tuned best predictions.csv"
qml_exhaustive_results_path = (
    processed_folder / "qml exhaustive feature combination results.csv"
)
qml_exhaustive_top_results_path = (
    processed_folder / "qml exhaustive feature combination top results.csv"
)
improved_qml_dataset_path = processed_folder / "improved qml feature pca.csv"
improved_qml_tuning_results_path = processed_folder / "improved qml tuning results.csv"
improved_qml_predictions_path = processed_folder / "improved qml best predictions.csv"
improved_qml_threshold_results_path = (
    processed_folder / "improved qml threshold results.csv"
)
improved_qml_threshold_predictions_path = (
    processed_folder / "improved qml threshold predictions.csv"
)
improved_qml_alignment_scores_path = (
    processed_folder / "improved qml alignment scores.csv"
)
improved_qml_alignment_results_path = (
    processed_folder / "improved qml alignment results.csv"
)
improved_qml_alignment_predictions_path = (
    processed_folder / "improved qml alignment predictions.csv"
)
best_qml_repeated_split_results_path = (
    processed_folder / "best qml repeated split results.csv"
)
best_qml_repeated_split_predictions_path = (
    processed_folder / "best qml repeated split predictions.csv"
)
qml_vs_logistic_results_path = (
    processed_folder / "qml vs logistic repeated split results.csv"
)
qml_vs_logistic_summary_path = (
    processed_folder / "qml vs logistic repeated split summary.csv"
)
qml_vs_logistic_predictions_path = (
    processed_folder / "qml vs logistic repeated split predictions.csv"
)


def make_table_output(dataframe):
    return {
        "output_type": "display_data",
        "data": {
            "text/plain": dataframe.to_string(index=False),
            "text/html": dataframe.to_html(index=False),
        },
        "metadata": {},
    }


def make_figure_output(figure):
    image_buffer = io.BytesIO()
    figure.savefig(image_buffer, format="png", dpi=150, bbox_inches="tight")
    image_text = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    plt.close(figure)

    return {
        "output_type": "display_data",
        "data": {
            "image/png": image_text,
            "text/plain": "<matplotlib figure>",
        },
        "metadata": {},
    }


def make_stream_output(text):
    return {
        "output_type": "stream",
        "name": "stdout",
        "text": text,
    }


def make_code_cell(source_text, outputs, execution_count):
    return {
        "id": f"cell-{execution_count:02d}",
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs,
        "source": source_text.splitlines(keepends=True),
    }


def make_markdown_cell(markdown_text, cell_id):
    return {
        "id": cell_id,
        "cell_type": "markdown",
        "metadata": {},
        "source": markdown_text.splitlines(keepends=True),
    }


def create_bar_figure(dataframe, x_column, y_column, title, x_label, y_label, color):
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(dataframe[x_column], dataframe[y_column], color=color)
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.tick_params(axis="x", rotation=35)
    axis.grid(axis="y", alpha=0.25)

    for index, value in enumerate(dataframe[y_column]):
        axis.text(index, value, f"{int(value):,}", ha="center", va="bottom", fontsize=8)

    return figure


def add_gate(axis, x_position, y_position, label, width=0.9, height=0.42):
    rectangle = patches.FancyBboxPatch(
        (x_position - width / 2, y_position - height / 2),
        width,
        height,
        boxstyle="round,pad=0.03,rounding_size=0.04",
        linewidth=1.4,
        edgecolor="#233142",
        facecolor="#edf4fb",
        zorder=3,
    )
    axis.add_patch(rectangle)
    axis.text(
        x_position,
        y_position,
        label,
        ha="center",
        va="center",
        fontsize=8,
        color="#111111",
        zorder=4,
    )


def add_controlled_phase(axis, x_position, upper_y_position, lower_y_position, label):
    axis.plot(
        [x_position, x_position],
        [upper_y_position, lower_y_position],
        color="#233142",
        linewidth=1.5,
        zorder=3,
    )
    for y_position in [upper_y_position, lower_y_position]:
        circle = patches.Circle(
            (x_position, y_position),
            radius=0.08,
            facecolor="#233142",
            edgecolor="#233142",
            zorder=4,
        )
        axis.add_patch(circle)
    axis.text(
        x_position,
        (upper_y_position + lower_y_position) / 2,
        label,
        ha="left",
        va="center",
        fontsize=7,
        color="#233142",
        bbox={"boxstyle": "round,pad=0.15", "facecolor": "#ffffff", "edgecolor": "none"},
        zorder=5,
    )


def create_qml_circuit_figure():
    feature_names = [
        "formation_energy_per_atom",
        "has_o",
        "space_group_number",
        "theoretical",
    ]
    y_positions = [3.5, 2.5, 1.5, 0.5]

    figure, axis = plt.subplots(figsize=(12, 5.2))
    axis.set_xlim(-0.2, 10.4)
    axis.set_ylim(-0.8, 4.6)
    axis.axis("off")

    axis.text(
        5.1,
        4.35,
        "Best QML Feature Map: 4-Qubit Entangled Quantum Kernel",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#111111",
    )

    for row_index, y_position in enumerate(y_positions):
        axis.plot(
            [1.2, 9.6],
            [y_position, y_position],
            color="#233142",
            linewidth=1.4,
            zorder=1,
        )
        axis.text(
            0.0,
            y_position,
            f"q{row_index}: |0>",
            ha="left",
            va="center",
            fontsize=9,
            color="#111111",
        )
        axis.text(
            0.95,
            y_position + 0.28,
            feature_names[row_index],
            ha="right",
            va="center",
            fontsize=7,
            color="#444444",
        )
        add_gate(axis, 2.2, y_position, f"RY(theta_{row_index})")

    add_controlled_phase(axis, 4.0, y_positions[0], y_positions[1], "CP(phi_01)")
    add_controlled_phase(axis, 5.3, y_positions[1], y_positions[2], "CP(phi_12)")
    add_controlled_phase(axis, 6.6, y_positions[2], y_positions[3], "CP(phi_23)")

    kernel_box = patches.FancyBboxPatch(
        (7.55, 0.0),
        1.75,
        4.0,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        linewidth=1.5,
        edgecolor="#315f8c",
        facecolor="#f2f7fc",
    )
    axis.add_patch(kernel_box)
    axis.text(
        8.425,
        2.25,
        "Kernel overlap",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="#111111",
    )
    axis.text(
        8.425,
        1.75,
        "K(x, y) =\n|<phi(x)|phi(y)>|^2",
        ha="center",
        va="center",
        fontsize=8,
        color="#111111",
    )

    add_gate(axis, 9.95, 2.0, "SVC", width=0.65, height=0.5)

    axis.text(
        5.1,
        -0.25,
        "theta_i = pi * scaled_feature_i      phi_ij = pi * scaled_feature_i * scaled_feature_j",
        ha="center",
        va="center",
        fontsize=9,
        color="#111111",
    )
    axis.text(
        5.1,
        -0.58,
        "This diagram represents our simulated quantum-kernel feature map, not a real quantum-hardware run.",
        ha="center",
        va="center",
        fontsize=8,
        color="#555555",
    )

    return figure


def create_metric_figure(metric_dataframe):
    figure, axis = plt.subplots(figsize=(9, 5))
    bar_width = 0.12
    metric_names = ["accuracy", "stable_precision", "stable_recall", "stable_f1"]
    model_names = metric_dataframe["model"].tolist()
    x_positions = list(range(len(metric_names)))

    colors = [
        "#315f8c",
        "#4f86c6",
        "#d88c2d",
        "#5f8f45",
        "#7b5ea7",
        "#8c4f4f",
        "#2f766d",
    ]
    center_offset = (len(model_names) - 1) / 2

    for model_index, model_name in enumerate(model_names):
        values = metric_dataframe.loc[
            metric_dataframe["model"] == model_name,
            metric_names,
        ].iloc[0]
        shifted_positions = [
            position + (model_index - center_offset) * bar_width
            for position in x_positions
        ]
        axis.bar(
            shifted_positions,
            values,
            width=bar_width,
            label=model_name,
            color=colors[model_index],
        )

    axis.set_title("Model Performance Comparison")
    axis.set_ylabel("Score")
    axis.set_ylim(0, 1.05)
    axis.set_xticks(x_positions)
    axis.set_xticklabels(
        ["Accuracy", "Stable Precision", "Stable Recall", "Stable F1"],
        rotation=15,
    )
    axis.grid(axis="y", alpha=0.25)
    axis.legend(loc="lower right", fontsize=8)

    return figure


def create_confusion_matrix_figure(confusion_table, title):
    figure, axis = plt.subplots(figsize=(5.8, 4.8))
    image = axis.imshow(confusion_table, cmap="Blues")
    axis.set_title(title)
    axis.set_xticks([0, 1])
    axis.set_xticklabels(["Predicted unstable", "Predicted stable"])
    axis.set_yticks([0, 1])
    axis.set_yticklabels(["Actual unstable", "Actual stable"])

    for row_index in range(confusion_table.shape[0]):
        for column_index in range(confusion_table.shape[1]):
            axis.text(
                column_index,
                row_index,
                str(confusion_table[row_index, column_index]),
                ha="center",
                va="center",
                color="black",
                fontsize=12,
            )

    figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    return figure


def get_metric_row(model_name, true_labels, predicted_labels):
    return {
        "model": model_name,
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


def main():
    lithium_scored_dataframe = pd.read_csv(lithium_scored_path)
    final_shortlist_dataframe = pd.read_csv(final_shortlist_path)
    dss_family_ranking_dataframe = pd.read_csv(dss_family_ranking_path)
    dss_material_ranking_dataframe = pd.read_csv(dss_material_ranking_path)
    dss_compound_ranking_dataframe = pd.read_csv(dss_compound_ranking_path)
    qml_ready_dataframe = pd.read_csv(qml_ready_path)
    qml_predictions_dataframe = pd.read_csv(qml_predictions_path)
    tuned_qml_predictions_dataframe = pd.read_csv(tuned_qml_predictions_path)
    qml_exhaustive_results_dataframe = pd.read_csv(qml_exhaustive_results_path)
    qml_exhaustive_top_results_dataframe = pd.read_csv(
        qml_exhaustive_top_results_path
    )
    improved_qml_dataset_dataframe = pd.read_csv(improved_qml_dataset_path)
    improved_qml_tuning_results_dataframe = pd.read_csv(improved_qml_tuning_results_path)
    improved_qml_predictions_dataframe = pd.read_csv(improved_qml_predictions_path)
    improved_qml_threshold_results_dataframe = pd.read_csv(
        improved_qml_threshold_results_path
    )
    improved_qml_threshold_predictions_dataframe = pd.read_csv(
        improved_qml_threshold_predictions_path
    )
    improved_qml_alignment_scores_dataframe = pd.read_csv(
        improved_qml_alignment_scores_path
    )
    improved_qml_alignment_results_dataframe = pd.read_csv(
        improved_qml_alignment_results_path
    )
    improved_qml_alignment_predictions_dataframe = pd.read_csv(
        improved_qml_alignment_predictions_path
    )
    best_qml_repeated_split_results_dataframe = pd.read_csv(
        best_qml_repeated_split_results_path
    )
    best_qml_repeated_split_predictions_dataframe = pd.read_csv(
        best_qml_repeated_split_predictions_path
    )
    qml_vs_logistic_results_dataframe = pd.read_csv(qml_vs_logistic_results_path)
    qml_vs_logistic_summary_dataframe = pd.read_csv(qml_vs_logistic_summary_path)
    qml_vs_logistic_predictions_dataframe = pd.read_csv(qml_vs_logistic_predictions_path)

    improved_best_result = improved_qml_tuning_results_dataframe.sort_values(
        by=["cv_stable_f1", "cv_accuracy", "cv_stable_recall"],
        ascending=[False, False, False],
    ).iloc[0]
    improved_best_threshold_result = improved_qml_threshold_results_dataframe.sort_values(
        by=["cv_stable_f1", "cv_accuracy", "cv_stable_recall"],
        ascending=[False, False, False],
    ).iloc[0]
    improved_best_alignment_result = improved_qml_alignment_results_dataframe.sort_values(
        by=["cv_stable_f1", "cv_accuracy", "kernel_target_alignment"],
        ascending=[False, False, False],
    ).iloc[0]
    qml_exhaustive_best_result = qml_exhaustive_top_results_dataframe.iloc[0]

    pipeline_counts_dataframe = pd.DataFrame(
        [
            {"stage": "Raw MP snapshot", "rows": 210579},
            {"stage": "Lithium dataset", "rows": len(lithium_scored_dataframe)},
            {"stage": "QML-ready dataset", "rows": len(qml_ready_dataframe)},
            {"stage": "Final shortlist", "rows": len(final_shortlist_dataframe)},
        ]
    )

    family_counts_dataframe = (
        lithium_scored_dataframe["battery_family"]
        .value_counts()
        .head(8)
        .reset_index()
    )
    family_counts_dataframe.columns = ["battery_family", "rows"]

    final_family_counts_dataframe = (
        final_shortlist_dataframe["battery_family"]
        .value_counts()
        .reset_index()
    )
    final_family_counts_dataframe.columns = ["battery_family", "rows"]

    decision_counts_dataframe = (
        lithium_scored_dataframe["india_decision_label"]
        .value_counts()
        .reset_index()
    )
    decision_counts_dataframe.columns = ["india_decision_label", "rows"]

    top_candidate_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_decision_label",
        "shortlist_rule_type",
        "shortlist_score",
        "predicted_stable_probability",
        "predicted_energy_above_hull_clipped",
        "india_feasibility_score",
    ]
    top_candidates_dataframe = final_shortlist_dataframe[top_candidate_columns].head(10)

    dss_family_display_columns = [
        "dss_rank",
        "battery_family",
        "dss_decision",
        "shortlist_rows",
        "average_hybrid_recommendation_score",
        "average_hybrid_stable_probability",
        "average_qml_stable_probability",
        "average_xgboost_stable_probability",
        "average_india_feasibility_score",
        "median_predicted_energy_above_hull",
        "top_formula",
        "short_reason",
    ]
    dss_family_display_dataframe = dss_family_ranking_dataframe[
        dss_family_display_columns
    ]
    dss_material_display_columns = [
        "dss_rank",
        "material_id",
        "formula",
        "battery_family",
        "dss_decision",
        "hybrid_recommendation_score",
        "hybrid_stable_probability",
        "qml_stable_probability",
        "xgboost_stable_probability",
        "qml_confidence_band",
        "hybrid_decision_role",
        "model_disagreement",
        "shortlist_score",
        "india_feasibility_score",
        "predicted_energy_above_hull_clipped",
        "short_conceptual_reason",
    ]
    dss_material_display_dataframe = dss_material_ranking_dataframe[
        dss_material_display_columns
    ].head(10)

    quantum_parameters_dataframe = pd.DataFrame(
        [
            {
                "parameter": "QML model type",
                "value": "Simulated quantum kernel classifier",
            },
            {"parameter": "Original number of qubits", "value": "10"},
            {"parameter": "Tuned number of qubits", "value": "8"},
            {"parameter": "Tuned quantum state size", "value": "256"},
            {
                "parameter": "Original feature encoding",
                "value": "angle = pi * scaled_feature_value",
            },
            {
                "parameter": "Tuned feature encoding",
                "value": "angle = (pi / 2) * scaled_feature_value",
            },
            {
                "parameter": "Single-qubit state",
                "value": "[cos(angle / 2), sin(angle / 2)]",
            },
            {
                "parameter": "Kernel formula",
                "value": "K(x, y) = |<phi(x), phi(y)>|^2",
            },
            {"parameter": "Classifier", "value": "SVC with precomputed kernel"},
            {"parameter": "Tuned SVM C value", "value": "1.0"},
            {"parameter": "Tuning method", "value": "4-fold cross-validation"},
            {
                "parameter": "Improved separate section",
                "value": "Random Forest feature importance + PCA + kernel tuning",
            },
            {
                "parameter": "Improved best qubits",
                "value": str(int(improved_best_result["pca_component_count"])),
            },
            {
                "parameter": "Improved best kernel",
                "value": str(improved_best_result["kernel_name"]),
            },
            {
                "parameter": "Improved best angle scale",
                "value": str(improved_best_result["angle_scale"]),
            },
            {
                "parameter": "Improved best SVM C value",
                "value": str(improved_best_result["c_value"]),
            },
            {
                "parameter": "Threshold experiment",
                "value": "Stable-probability cutoff tuned by cross-validation",
            },
            {
                "parameter": "Best stable threshold",
                "value": str(improved_best_threshold_result["stable_threshold"]),
            },
            {
                "parameter": "Kernel alignment experiment",
                "value": "Feature set selected by quantum kernel-target alignment",
            },
            {
                "parameter": "Alignment best feature set",
                "value": str(improved_best_alignment_result["feature_set_name"]),
            },
            {
                "parameter": "Alignment best qubits",
                "value": str(int(improved_best_alignment_result["feature_count"])),
            },
            {
                "parameter": "Alignment best kernel",
                "value": str(improved_best_alignment_result["kernel_name"]),
            },
            {
                "parameter": "Alignment best SVM C value",
                "value": str(improved_best_alignment_result["c_value"]),
            },
            {"parameter": "Train/test split", "value": "80/20"},
            {"parameter": "Random state", "value": "42"},
        ]
    )

    qml_circuit_dataframe = pd.DataFrame(
        [
            {
                "qubit": "q0",
                "feature": "formation_energy_per_atom",
                "gate": "RY(theta_0)",
                "angle": "theta_0 = pi * scaled formation_energy_per_atom",
            },
            {
                "qubit": "q1",
                "feature": "has_o",
                "gate": "RY(theta_1)",
                "angle": "theta_1 = pi * scaled has_o",
            },
            {
                "qubit": "q2",
                "feature": "space_group_number",
                "gate": "RY(theta_2)",
                "angle": "theta_2 = pi * scaled space_group_number",
            },
            {
                "qubit": "q3",
                "feature": "theoretical",
                "gate": "RY(theta_3)",
                "angle": "theta_3 = pi * scaled theoretical",
            },
        ]
    )

    qml_exhaustive_summary_dataframe = pd.DataFrame(
        [
            {
                "total_configurations": len(qml_exhaustive_results_dataframe),
                "feature_combinations": 466,
                "feature_count": int(qml_exhaustive_best_result["feature_count"]),
                "angle_scale": qml_exhaustive_best_result["angle_scale"],
                "svm_c": qml_exhaustive_best_result["c_value"],
                "cv_accuracy": qml_exhaustive_best_result["cv_accuracy"],
                "cv_stable_f1": qml_exhaustive_best_result["cv_stable_f1"],
            }
        ]
    )
    qml_exhaustive_top_display_dataframe = qml_exhaustive_top_results_dataframe[
        [
            "feature_count",
            "feature_names",
            "angle_scale",
            "c_value",
            "cv_accuracy",
            "cv_stable_recall",
            "cv_stable_f1",
        ]
    ].head(10)

    true_labels = qml_predictions_dataframe["target_is_stable"]
    qml_predicted_labels = qml_predictions_dataframe["qml_predicted_label"]
    xgboost_predicted_labels = qml_predictions_dataframe[
        "xgboost_same_data_predicted_label"
    ]
    tuned_true_labels = tuned_qml_predictions_dataframe["target_is_stable"]
    tuned_qml_predicted_labels = tuned_qml_predictions_dataframe[
        "tuned_qml_predicted_label"
    ]
    improved_true_labels = improved_qml_predictions_dataframe["target_is_stable"]
    improved_qml_predicted_labels = improved_qml_predictions_dataframe[
        "improved_qml_predicted_label"
    ]
    threshold_true_labels = improved_qml_threshold_predictions_dataframe[
        "target_is_stable"
    ]
    threshold_qml_predicted_labels = improved_qml_threshold_predictions_dataframe[
        "threshold_qml_predicted_label"
    ]
    alignment_true_labels = improved_qml_alignment_predictions_dataframe[
        "target_is_stable"
    ]
    alignment_qml_predicted_labels = improved_qml_alignment_predictions_dataframe[
        "alignment_qml_predicted_label"
    ]

    metric_dataframe = pd.DataFrame(
        [
            get_metric_row("QML quantum kernel", true_labels, qml_predicted_labels),
            get_metric_row(
                "Tuned QML quantum kernel",
                tuned_true_labels,
                tuned_qml_predicted_labels,
            ),
            get_metric_row(
                "Improved QML separate section",
                improved_true_labels,
                improved_qml_predicted_labels,
            ),
            get_metric_row(
                "Improved QML threshold tuning",
                threshold_true_labels,
                threshold_qml_predicted_labels,
            ),
            get_metric_row(
                "Improved QML kernel alignment",
                alignment_true_labels,
                alignment_qml_predicted_labels,
            ),
            get_metric_row(
                "XGBoost same QML data",
                true_labels,
                xgboost_predicted_labels,
            ),
            {
                "model": "XGBoost full project",
                "accuracy": 0.9091,
                "stable_precision": 0.7300,
                "stable_recall": 0.7000,
                "stable_f1": 0.7100,
            },
        ]
    )

    qml_confusion_matrix = confusion_matrix(
        tuned_true_labels,
        tuned_qml_predicted_labels,
        labels=[0, 1],
    )
    improved_qml_confusion_matrix = confusion_matrix(
        improved_true_labels,
        improved_qml_predicted_labels,
        labels=[0, 1],
    )
    threshold_qml_confusion_matrix = confusion_matrix(
        threshold_true_labels,
        threshold_qml_predicted_labels,
        labels=[0, 1],
    )
    alignment_qml_confusion_matrix = confusion_matrix(
        alignment_true_labels,
        alignment_qml_predicted_labels,
        labels=[0, 1],
    )

    sample_predictions_dataframe = tuned_qml_predictions_dataframe[
        [
            "material_id",
            "formula",
            "target_is_stable",
            "tuned_qml_predicted_label",
            "tuned_qml_stable_probability",
        ]
    ].head(10)

    improved_summary_dataframe = pd.DataFrame(
        [
            {
                "section": "Improved QML separate section",
                "feature_preparation": "feature importance + PCA",
                "best_kernel": improved_best_result["kernel_name"],
                "best_qubits": int(improved_best_result["pca_component_count"]),
                "angle_scale": improved_best_result["angle_scale"],
                "svm_c": improved_best_result["c_value"],
                "cv_stable_f1": improved_best_result["cv_stable_f1"],
                "test_accuracy": round(
                    accuracy_score(improved_true_labels, improved_qml_predicted_labels),
                    4,
                ),
                "test_stable_f1": round(
                    f1_score(
                        improved_true_labels,
                        improved_qml_predicted_labels,
                        zero_division=0,
                    ),
                    4,
                ),
            }
        ]
    )

    improved_sample_predictions_dataframe = improved_qml_predictions_dataframe[
        [
            "material_id",
            "formula",
            "target_is_stable",
            "improved_qml_predicted_label",
            "improved_qml_stable_probability",
        ]
    ].head(10)

    threshold_summary_dataframe = pd.DataFrame(
        [
            {
                "section": "Threshold experiment",
                "selected_threshold": improved_best_threshold_result[
                    "stable_threshold"
                ],
                "cv_stable_f1": improved_best_threshold_result["cv_stable_f1"],
                "test_accuracy": round(
                    accuracy_score(
                        threshold_true_labels,
                        threshold_qml_predicted_labels,
                    ),
                    4,
                ),
                "test_stable_precision": round(
                    precision_score(
                        threshold_true_labels,
                        threshold_qml_predicted_labels,
                        zero_division=0,
                    ),
                    4,
                ),
                "test_stable_recall": round(
                    recall_score(
                        threshold_true_labels,
                        threshold_qml_predicted_labels,
                        zero_division=0,
                    ),
                    4,
                ),
                "test_stable_f1": round(
                    f1_score(
                        threshold_true_labels,
                        threshold_qml_predicted_labels,
                        zero_division=0,
                    ),
                    4,
                ),
            }
        ]
    )

    alignment_summary_dataframe = pd.DataFrame(
        [
            {
                "section": "Kernel alignment experiment",
                "feature_set": improved_best_alignment_result["feature_set_name"],
                "feature_count": int(improved_best_alignment_result["feature_count"]),
                "kernel": improved_best_alignment_result["kernel_name"],
                "angle_scale": improved_best_alignment_result["angle_scale"],
                "svm_c": improved_best_alignment_result["c_value"],
                "kernel_target_alignment": improved_best_alignment_result[
                    "kernel_target_alignment"
                ],
                "cv_stable_f1": improved_best_alignment_result["cv_stable_f1"],
                "test_accuracy": round(
                    accuracy_score(
                        alignment_true_labels,
                        alignment_qml_predicted_labels,
                    ),
                    4,
                ),
                "test_stable_f1": round(
                    f1_score(
                        alignment_true_labels,
                        alignment_qml_predicted_labels,
                        zero_division=0,
                    ),
                    4,
                ),
            }
        ]
    )

    alignment_sample_predictions_dataframe = improved_qml_alignment_predictions_dataframe[
        [
            "material_id",
            "formula",
            "target_is_stable",
            "alignment_qml_predicted_label",
            "alignment_qml_stable_probability",
        ]
    ].head(10)

    repeated_split_summary_rows = []
    repeated_split_metric_columns = [
        "accuracy",
        "stable_precision",
        "stable_recall",
        "stable_f1",
    ]
    for metric_name in repeated_split_metric_columns:
        repeated_split_summary_rows.append(
            {
                "metric": metric_name,
                "mean": round(
                    best_qml_repeated_split_results_dataframe[metric_name].mean(),
                    4,
                ),
                "standard_deviation": round(
                    best_qml_repeated_split_results_dataframe[metric_name].std(ddof=1),
                    4,
                ),
                "minimum": round(
                    best_qml_repeated_split_results_dataframe[metric_name].min(),
                    4,
                ),
                "maximum": round(
                    best_qml_repeated_split_results_dataframe[metric_name].max(),
                    4,
                ),
            }
        )
    repeated_split_summary_dataframe = pd.DataFrame(repeated_split_summary_rows)

    qml_vs_logistic_comparison_rows = []
    qml_vs_logistic_metric_names = [
        "accuracy",
        "stable_precision",
        "stable_recall",
        "stable_f1",
    ]
    for metric_name in qml_vs_logistic_metric_names:
        qml_mean = qml_vs_logistic_summary_dataframe[
            (qml_vs_logistic_summary_dataframe["model"] == "QML kernel classifier")
            & (qml_vs_logistic_summary_dataframe["metric"] == metric_name)
        ]["mean"].iloc[0]
        logistic_mean = qml_vs_logistic_summary_dataframe[
            (qml_vs_logistic_summary_dataframe["model"] == "Logistic Regression")
            & (qml_vs_logistic_summary_dataframe["metric"] == metric_name)
        ]["mean"].iloc[0]
        difference = qml_mean - logistic_mean
        if difference > 0:
            winner = "QML"
        elif difference < 0:
            winner = "Logistic Regression"
        else:
            winner = "Tie"
        qml_vs_logistic_comparison_rows.append(
            {
                "metric": metric_name,
                "qml_mean": round(qml_mean, 4),
                "logistic_mean": round(logistic_mean, 4),
                "qml_minus_logistic": round(difference, 4),
                "winner": winner,
            }
        )
    qml_vs_logistic_comparison_dataframe = pd.DataFrame(
        qml_vs_logistic_comparison_rows
    )

    cells = []
    execution_count = 1

    title_markdown = """# Battery Materials DSS QML

**Presentation notebook**

Goal: build a student-level Decision Support System for lithium-ion battery
material recommendation using Materials Project data, India-focused screening,
XGBoost, and simulated QML comparison.
"""
    cells.append(make_markdown_cell(title_markdown, "markdown-title"))

    student_flow_markdown = """## Student-Level Project Flow

This project is presented as a DSS first and a QML exploration second.

1. XGBoost is the strong current classical benchmark for structured materials
   data.
2. Logistic Regression is the simple classical baseline.
3. Simulated QML is the quantum-future experiment.
4. The final recommendation is made through DSS ranking tables, not through an
   unsupported claim of quantum advantage.

**Why quantum is included**

Battery materials are controlled by atomic and electronic behavior. That
behavior is quantum mechanical. Classical ML is useful today, but future
quantum models may represent material interactions more naturally. This project
therefore uses simulated QML as a safe first step toward quantum-assisted
materials discovery.
"""
    cells.append(make_markdown_cell(student_flow_markdown, "markdown-student-flow"))

    data_loading_source = """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

project_folder = Path.cwd()
processed_folder = project_folder / "data" / "processed"

lithium_scored_dataframe = pd.read_csv(processed_folder / "lithium india scored.csv")
final_shortlist_dataframe = pd.read_csv(processed_folder / "final india battery shortlist.csv")
dss_family_ranking_dataframe = pd.read_csv(processed_folder / "dss battery family recommendation ranking.csv")
dss_compound_ranking_dataframe = pd.read_csv(processed_folder / "dss compound recommendation ranking.csv")
dss_material_ranking_dataframe = dss_compound_ranking_dataframe.copy()
qml_ready_dataframe = pd.read_csv(processed_folder / "qml_ready_lithium_india.csv")
qml_predictions_dataframe = pd.read_csv(processed_folder / "qml baseline predictions.csv")
tuned_qml_predictions_dataframe = pd.read_csv(processed_folder / "qml tuned best predictions.csv")
qml_exhaustive_results_dataframe = pd.read_csv(processed_folder / "qml exhaustive feature combination results.csv")
qml_exhaustive_top_results_dataframe = pd.read_csv(processed_folder / "qml exhaustive feature combination top results.csv")
qml_exhaustive_best_result = qml_exhaustive_top_results_dataframe.iloc[0]
improved_qml_dataset_dataframe = pd.read_csv(processed_folder / "improved qml feature pca.csv")
improved_qml_tuning_results_dataframe = pd.read_csv(processed_folder / "improved qml tuning results.csv")
improved_qml_predictions_dataframe = pd.read_csv(processed_folder / "improved qml best predictions.csv")
improved_qml_threshold_results_dataframe = pd.read_csv(processed_folder / "improved qml threshold results.csv")
improved_qml_threshold_predictions_dataframe = pd.read_csv(processed_folder / "improved qml threshold predictions.csv")
improved_qml_alignment_scores_dataframe = pd.read_csv(processed_folder / "improved qml alignment scores.csv")
improved_qml_alignment_results_dataframe = pd.read_csv(processed_folder / "improved qml alignment results.csv")
improved_qml_alignment_predictions_dataframe = pd.read_csv(processed_folder / "improved qml alignment predictions.csv")
best_qml_repeated_split_results_dataframe = pd.read_csv(processed_folder / "best qml repeated split results.csv")
best_qml_repeated_split_predictions_dataframe = pd.read_csv(processed_folder / "best qml repeated split predictions.csv")
qml_vs_logistic_results_dataframe = pd.read_csv(processed_folder / "qml vs logistic repeated split results.csv")
qml_vs_logistic_summary_dataframe = pd.read_csv(processed_folder / "qml vs logistic repeated split summary.csv")
qml_vs_logistic_predictions_dataframe = pd.read_csv(processed_folder / "qml vs logistic repeated split predictions.csv")

dataset_summary = pd.DataFrame([
    {"dataset": "Lithium India scored", "rows": len(lithium_scored_dataframe), "columns": len(lithium_scored_dataframe.columns)},
    {"dataset": "Final India shortlist", "rows": len(final_shortlist_dataframe), "columns": len(final_shortlist_dataframe.columns)},
    {"dataset": "DSS compound ranking", "rows": len(dss_compound_ranking_dataframe), "columns": len(dss_compound_ranking_dataframe.columns)},
    {"dataset": "DSS family context", "rows": len(dss_family_ranking_dataframe), "columns": len(dss_family_ranking_dataframe.columns)},
    {"dataset": "QML-ready dataset", "rows": len(qml_ready_dataframe), "columns": len(qml_ready_dataframe.columns)},
    {"dataset": "QML test predictions", "rows": len(qml_predictions_dataframe), "columns": len(qml_predictions_dataframe.columns)},
    {"dataset": "Tuned QML test predictions", "rows": len(tuned_qml_predictions_dataframe), "columns": len(tuned_qml_predictions_dataframe.columns)},
    {"dataset": "Exhaustive QML tuning results", "rows": len(qml_exhaustive_results_dataframe), "columns": len(qml_exhaustive_results_dataframe.columns)},
    {"dataset": "Exhaustive QML top results", "rows": len(qml_exhaustive_top_results_dataframe), "columns": len(qml_exhaustive_top_results_dataframe.columns)},
    {"dataset": "Improved QML PCA dataset", "rows": len(improved_qml_dataset_dataframe), "columns": len(improved_qml_dataset_dataframe.columns)},
    {"dataset": "Improved QML tuning results", "rows": len(improved_qml_tuning_results_dataframe), "columns": len(improved_qml_tuning_results_dataframe.columns)},
    {"dataset": "Improved QML test predictions", "rows": len(improved_qml_predictions_dataframe), "columns": len(improved_qml_predictions_dataframe.columns)},
    {"dataset": "Improved QML threshold results", "rows": len(improved_qml_threshold_results_dataframe), "columns": len(improved_qml_threshold_results_dataframe.columns)},
    {"dataset": "Improved QML threshold predictions", "rows": len(improved_qml_threshold_predictions_dataframe), "columns": len(improved_qml_threshold_predictions_dataframe.columns)},
    {"dataset": "Improved QML alignment scores", "rows": len(improved_qml_alignment_scores_dataframe), "columns": len(improved_qml_alignment_scores_dataframe.columns)},
    {"dataset": "Improved QML alignment results", "rows": len(improved_qml_alignment_results_dataframe), "columns": len(improved_qml_alignment_results_dataframe.columns)},
    {"dataset": "Improved QML alignment predictions", "rows": len(improved_qml_alignment_predictions_dataframe), "columns": len(improved_qml_alignment_predictions_dataframe.columns)},
    {"dataset": "Best QML repeated split results", "rows": len(best_qml_repeated_split_results_dataframe), "columns": len(best_qml_repeated_split_results_dataframe.columns)},
    {"dataset": "Best QML repeated split predictions", "rows": len(best_qml_repeated_split_predictions_dataframe), "columns": len(best_qml_repeated_split_predictions_dataframe.columns)},
    {"dataset": "QML vs Logistic results", "rows": len(qml_vs_logistic_results_dataframe), "columns": len(qml_vs_logistic_results_dataframe.columns)},
    {"dataset": "QML vs Logistic summary", "rows": len(qml_vs_logistic_summary_dataframe), "columns": len(qml_vs_logistic_summary_dataframe.columns)},
    {"dataset": "QML vs Logistic predictions", "rows": len(qml_vs_logistic_predictions_dataframe), "columns": len(qml_vs_logistic_predictions_dataframe.columns)},
])
display(dataset_summary)"""
    dataset_summary_dataframe = pd.DataFrame(
        [
            {
                "dataset": "Lithium India scored",
                "rows": len(lithium_scored_dataframe),
                "columns": len(lithium_scored_dataframe.columns),
            },
            {
                "dataset": "Final India shortlist",
                "rows": len(final_shortlist_dataframe),
                "columns": len(final_shortlist_dataframe.columns),
            },
            {
                "dataset": "DSS compound ranking",
                "rows": len(dss_compound_ranking_dataframe),
                "columns": len(dss_compound_ranking_dataframe.columns),
            },
            {
                "dataset": "DSS family context",
                "rows": len(dss_family_ranking_dataframe),
                "columns": len(dss_family_ranking_dataframe.columns),
            },
            {
                "dataset": "QML-ready dataset",
                "rows": len(qml_ready_dataframe),
                "columns": len(qml_ready_dataframe.columns),
            },
            {
                "dataset": "QML test predictions",
                "rows": len(qml_predictions_dataframe),
                "columns": len(qml_predictions_dataframe.columns),
            },
            {
                "dataset": "Tuned QML test predictions",
                "rows": len(tuned_qml_predictions_dataframe),
                "columns": len(tuned_qml_predictions_dataframe.columns),
            },
            {
                "dataset": "Exhaustive QML tuning results",
                "rows": len(qml_exhaustive_results_dataframe),
                "columns": len(qml_exhaustive_results_dataframe.columns),
            },
            {
                "dataset": "Exhaustive QML top results",
                "rows": len(qml_exhaustive_top_results_dataframe),
                "columns": len(qml_exhaustive_top_results_dataframe.columns),
            },
            {
                "dataset": "Improved QML PCA dataset",
                "rows": len(improved_qml_dataset_dataframe),
                "columns": len(improved_qml_dataset_dataframe.columns),
            },
            {
                "dataset": "Improved QML tuning results",
                "rows": len(improved_qml_tuning_results_dataframe),
                "columns": len(improved_qml_tuning_results_dataframe.columns),
            },
            {
                "dataset": "Improved QML test predictions",
                "rows": len(improved_qml_predictions_dataframe),
                "columns": len(improved_qml_predictions_dataframe.columns),
            },
            {
                "dataset": "Improved QML threshold results",
                "rows": len(improved_qml_threshold_results_dataframe),
                "columns": len(improved_qml_threshold_results_dataframe.columns),
            },
            {
                "dataset": "Improved QML threshold predictions",
                "rows": len(improved_qml_threshold_predictions_dataframe),
                "columns": len(improved_qml_threshold_predictions_dataframe.columns),
            },
            {
                "dataset": "Improved QML alignment scores",
                "rows": len(improved_qml_alignment_scores_dataframe),
                "columns": len(improved_qml_alignment_scores_dataframe.columns),
            },
            {
                "dataset": "Improved QML alignment results",
                "rows": len(improved_qml_alignment_results_dataframe),
                "columns": len(improved_qml_alignment_results_dataframe.columns),
            },
            {
                "dataset": "Improved QML alignment predictions",
                "rows": len(improved_qml_alignment_predictions_dataframe),
                "columns": len(improved_qml_alignment_predictions_dataframe.columns),
            },
            {
                "dataset": "Best QML repeated split results",
                "rows": len(best_qml_repeated_split_results_dataframe),
                "columns": len(best_qml_repeated_split_results_dataframe.columns),
            },
            {
                "dataset": "Best QML repeated split predictions",
                "rows": len(best_qml_repeated_split_predictions_dataframe),
                "columns": len(best_qml_repeated_split_predictions_dataframe.columns),
            },
            {
                "dataset": "QML vs Logistic results",
                "rows": len(qml_vs_logistic_results_dataframe),
                "columns": len(qml_vs_logistic_results_dataframe.columns),
            },
            {
                "dataset": "QML vs Logistic summary",
                "rows": len(qml_vs_logistic_summary_dataframe),
                "columns": len(qml_vs_logistic_summary_dataframe.columns),
            },
            {
                "dataset": "QML vs Logistic predictions",
                "rows": len(qml_vs_logistic_predictions_dataframe),
                "columns": len(qml_vs_logistic_predictions_dataframe.columns),
            },
        ]
    )
    cells.append(
        make_code_cell(
            data_loading_source,
            [make_table_output(dataset_summary_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    pipeline_figure = create_bar_figure(
        pipeline_counts_dataframe,
        "stage",
        "rows",
        "Dataset Size Through The Pipeline",
        "Pipeline stage",
        "Rows",
        "#315f8c",
    )
    pipeline_source = """pipeline_counts_dataframe = pd.DataFrame([
    {"stage": "Raw MP snapshot", "rows": 210579},
    {"stage": "Lithium dataset", "rows": len(lithium_scored_dataframe)},
    {"stage": "QML-ready dataset", "rows": len(qml_ready_dataframe)},
    {"stage": "Final shortlist", "rows": len(final_shortlist_dataframe)},
])

plt.figure(figsize=(9, 5))
plt.bar(pipeline_counts_dataframe["stage"], pipeline_counts_dataframe["rows"])
plt.title("Dataset Size Through The Pipeline")
plt.xlabel("Pipeline stage")
plt.ylabel("Rows")
plt.xticks(rotation=35)
plt.grid(axis="y", alpha=0.25)
plt.show()"""
    cells.append(
        make_code_cell(
            pipeline_source,
            [make_table_output(pipeline_counts_dataframe), make_figure_output(pipeline_figure)],
            execution_count,
        )
    )
    execution_count += 1

    family_figure = create_bar_figure(
        family_counts_dataframe,
        "battery_family",
        "rows",
        "Top Lithium Battery Families In Full Dataset",
        "Battery family",
        "Rows",
        "#5f8f45",
    )
    family_source = """family_counts_dataframe = (
    lithium_scored_dataframe["battery_family"]
    .value_counts()
    .head(8)
    .reset_index()
)
family_counts_dataframe.columns = ["battery_family", "rows"]

display(family_counts_dataframe)

plt.figure(figsize=(9, 5))
plt.bar(family_counts_dataframe["battery_family"], family_counts_dataframe["rows"])
plt.title("Top Lithium Battery Families In Full Dataset")
plt.xlabel("Battery family")
plt.ylabel("Rows")
plt.xticks(rotation=35)
plt.grid(axis="y", alpha=0.25)
plt.show()"""
    cells.append(
        make_code_cell(
            family_source,
            [make_table_output(family_counts_dataframe), make_figure_output(family_figure)],
            execution_count,
        )
    )
    execution_count += 1

    decision_figure = create_bar_figure(
        decision_counts_dataframe,
        "india_decision_label",
        "rows",
        "India Feasibility Decision Labels",
        "Decision label",
        "Rows",
        "#d88c2d",
    )
    decision_source = """decision_counts_dataframe = (
    lithium_scored_dataframe["india_decision_label"]
    .value_counts()
    .reset_index()
)
decision_counts_dataframe.columns = ["india_decision_label", "rows"]

display(decision_counts_dataframe)

plt.figure(figsize=(9, 5))
plt.bar(decision_counts_dataframe["india_decision_label"], decision_counts_dataframe["rows"])
plt.title("India Feasibility Decision Labels")
plt.xlabel("Decision label")
plt.ylabel("Rows")
plt.xticks(rotation=35)
plt.grid(axis="y", alpha=0.25)
plt.show()"""
    cells.append(
        make_code_cell(
            decision_source,
            [make_table_output(decision_counts_dataframe), make_figure_output(decision_figure)],
            execution_count,
        )
    )
    execution_count += 1

    final_family_figure = create_bar_figure(
        final_family_counts_dataframe,
        "battery_family",
        "rows",
        "Final Shortlist Battery Families",
        "Battery family",
        "Rows",
        "#7b5ea7",
    )
    final_family_source = """final_family_counts_dataframe = (
    final_shortlist_dataframe["battery_family"]
    .value_counts()
    .reset_index()
)
final_family_counts_dataframe.columns = ["battery_family", "rows"]

display(final_family_counts_dataframe)

plt.figure(figsize=(9, 5))
plt.bar(final_family_counts_dataframe["battery_family"], final_family_counts_dataframe["rows"])
plt.title("Final Shortlist Battery Families")
plt.xlabel("Battery family")
plt.ylabel("Rows")
plt.xticks(rotation=35)
plt.grid(axis="y", alpha=0.25)
plt.show()"""
    cells.append(
        make_code_cell(
            final_family_source,
            [
                make_table_output(final_family_counts_dataframe),
                make_figure_output(final_family_figure),
            ],
            execution_count,
        )
    )
    execution_count += 1

    top_candidates_source = """top_candidate_columns = [
    "material_id",
    "formula",
    "battery_family",
    "india_decision_label",
    "shortlist_rule_type",
    "shortlist_score",
    "predicted_stable_probability",
    "predicted_energy_above_hull_clipped",
    "india_feasibility_score",
]
top_candidates_dataframe = final_shortlist_dataframe[top_candidate_columns].head(10)
display(top_candidates_dataframe)"""
    cells.append(
        make_code_cell(
            top_candidates_source,
            [make_table_output(top_candidates_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    dss_markdown = """## DSS Compound Recommendation Ranking

The project is used as a Decision Support System here. The main output is a
ranked list of exact lithium compound formulas. Battery family is shown only as
supporting context.

In this flow, QML gives the first stability signal. XGBoost is used as a
corrective backup when the QML probability is uncertain or when both models
disagree. This keeps the DSS quantum-led without ignoring the stronger
classical benchmark.
"""
    dss_source = """dss_compound_display_columns = [
    "dss_rank",
    "formula",
    "material_id",
    "battery_family",
    "dss_decision",
    "hybrid_recommendation_score",
    "hybrid_stable_probability",
    "qml_stable_probability",
    "xgboost_stable_probability",
    "qml_confidence_band",
    "hybrid_decision_role",
    "model_disagreement",
    "shortlist_score",
    "india_feasibility_score",
    "predicted_energy_above_hull_clipped",
    "band_gap",
    "short_conceptual_reason",
]
dss_compound_display_dataframe = dss_compound_ranking_dataframe[
    dss_compound_display_columns
].head(10)
display(dss_compound_display_dataframe)

dss_family_display_columns = [
    "dss_rank",
    "battery_family",
    "dss_decision",
    "shortlist_rows",
    "average_hybrid_recommendation_score",
    "average_hybrid_stable_probability",
    "average_qml_stable_probability",
    "average_xgboost_stable_probability",
    "average_india_feasibility_score",
    "median_predicted_energy_above_hull",
    "top_formula",
    "short_reason",
]
dss_family_display_dataframe = dss_family_ranking_dataframe[dss_family_display_columns]
display(dss_family_display_dataframe)"""
    cells.append(make_markdown_cell(dss_markdown, "markdown-dss-ranking"))
    cells.append(
        make_code_cell(
            dss_source,
            [
                make_table_output(
                    dss_compound_ranking_dataframe[
                        [
                            "dss_rank",
                            "formula",
                            "material_id",
                            "battery_family",
                            "dss_decision",
                            "hybrid_recommendation_score",
                            "hybrid_stable_probability",
                            "qml_stable_probability",
                            "xgboost_stable_probability",
                            "qml_confidence_band",
                            "hybrid_decision_role",
                            "model_disagreement",
                            "shortlist_score",
                            "india_feasibility_score",
                            "predicted_energy_above_hull_clipped",
                            "band_gap",
                            "short_conceptual_reason",
                        ]
                    ].head(10)
                ),
                make_table_output(dss_family_display_dataframe),
            ],
            execution_count,
        )
    )
    execution_count += 1

    quantum_parameters_source = """quantum_parameters_dataframe = pd.DataFrame([
    {"parameter": "QML model type", "value": "Simulated quantum kernel classifier"},
    {"parameter": "Student-level role", "value": "Quantum-future experiment, not a full replacement for XGBoost"},
    {"parameter": "Why quantum is relevant", "value": "Battery materials are quantum systems at atomic scale"},
    {"parameter": "Original number of qubits", "value": "10"},
    {"parameter": "Tuned number of qubits", "value": "8"},
    {"parameter": "Tuned quantum state size", "value": "256"},
    {"parameter": "Original feature encoding", "value": "angle = pi * scaled_feature_value"},
    {"parameter": "Tuned feature encoding", "value": "angle = (pi / 2) * scaled_feature_value"},
    {"parameter": "Single-qubit state", "value": "[cos(angle / 2), sin(angle / 2)]"},
    {"parameter": "Kernel formula", "value": "K(x, y) = |<phi(x), phi(y)>|^2"},
    {"parameter": "Classifier", "value": "SVC with precomputed kernel"},
    {"parameter": "Tuned SVM C value", "value": "1.0"},
    {"parameter": "Tuning method", "value": "4-fold cross-validation"},
    {"parameter": "Improved separate section", "value": "Random Forest feature importance + PCA + kernel tuning"},
    {"parameter": "Improved best qubits", "value": "6"},
    {"parameter": "Improved best kernel", "value": "entangled_pi"},
    {"parameter": "Improved best angle scale", "value": "pi"},
    {"parameter": "Improved best SVM C value", "value": "2.0"},
    {"parameter": "Threshold experiment", "value": "Stable-probability cutoff tuned by cross-validation"},
    {"parameter": "Best stable threshold", "value": "0.50"},
    {"parameter": "Kernel alignment experiment", "value": "Feature set selected by quantum kernel-target alignment"},
    {"parameter": "Alignment best feature set", "value": "rf_top_4"},
    {"parameter": "Alignment best qubits", "value": "4"},
    {"parameter": "Alignment best kernel", "value": "entangled_pi"},
    {"parameter": "Alignment best SVM C value", "value": "5.0"},
    {"parameter": "Train/test split", "value": "80/20"},
    {"parameter": "Random state", "value": "42"},
])
display(quantum_parameters_dataframe)"""
    cells.append(
        make_code_cell(
            quantum_parameters_source,
            [make_table_output(quantum_parameters_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    qml_circuit_figure = create_qml_circuit_figure()
    qml_circuit_source = """qml_circuit_dataframe = pd.DataFrame([
    {
        "qubit": "q0",
        "feature": "formation_energy_per_atom",
        "gate": "RY(theta_0)",
        "angle": "theta_0 = pi * scaled formation_energy_per_atom",
    },
    {
        "qubit": "q1",
        "feature": "has_o",
        "gate": "RY(theta_1)",
        "angle": "theta_1 = pi * scaled has_o",
    },
    {
        "qubit": "q2",
        "feature": "space_group_number",
        "gate": "RY(theta_2)",
        "angle": "theta_2 = pi * scaled space_group_number",
    },
    {
        "qubit": "q3",
        "feature": "theoretical",
        "gate": "RY(theta_3)",
        "angle": "theta_3 = pi * scaled theoretical",
    },
])
display(qml_circuit_dataframe)

qml_circuit_image = plt.imread(processed_folder / "qml circuit diagram.png")
plt.figure(figsize=(12, 5.2))
plt.imshow(qml_circuit_image)
plt.axis("off")
plt.show()"""
    cells.append(
        make_code_cell(
            qml_circuit_source,
            [
                make_table_output(qml_circuit_dataframe),
                make_figure_output(qml_circuit_figure),
            ],
            execution_count,
        )
    )
    execution_count += 1

    qml_exhaustive_markdown = """## Exhaustive QML Feature-Combination Tuning

This step tests the stronger tuning approach: all selected feature-count
combinations are compared with all angle scales and all SVM `C` values. The
full result table has 8,388 rows.
"""
    qml_exhaustive_source = """qml_exhaustive_summary_dataframe = pd.DataFrame([
    {
        "total_configurations": len(qml_exhaustive_results_dataframe),
        "feature_combinations": 466,
        "feature_count": int(qml_exhaustive_best_result["feature_count"]),
        "angle_scale": qml_exhaustive_best_result["angle_scale"],
        "svm_c": qml_exhaustive_best_result["c_value"],
        "cv_accuracy": qml_exhaustive_best_result["cv_accuracy"],
        "cv_stable_f1": qml_exhaustive_best_result["cv_stable_f1"],
    }
])
display(qml_exhaustive_summary_dataframe)

qml_exhaustive_top_display_dataframe = qml_exhaustive_top_results_dataframe[
    [
        "feature_count",
        "feature_names",
        "angle_scale",
        "c_value",
        "cv_accuracy",
        "cv_stable_recall",
        "cv_stable_f1",
    ]
].head(10)
display(qml_exhaustive_top_display_dataframe)"""
    cells.append(
        make_markdown_cell(qml_exhaustive_markdown, "markdown-exhaustive-tuning")
    )
    cells.append(
        make_code_cell(
            qml_exhaustive_source,
            [
                make_table_output(qml_exhaustive_summary_dataframe),
                make_table_output(qml_exhaustive_top_display_dataframe),
            ],
            execution_count,
        )
    )
    execution_count += 1

    metric_figure = create_metric_figure(metric_dataframe)
    metric_source = """true_labels = qml_predictions_dataframe["target_is_stable"]
qml_predicted_labels = qml_predictions_dataframe["qml_predicted_label"]
xgboost_predicted_labels = qml_predictions_dataframe["xgboost_same_data_predicted_label"]
tuned_true_labels = tuned_qml_predictions_dataframe["target_is_stable"]
tuned_qml_predicted_labels = tuned_qml_predictions_dataframe["tuned_qml_predicted_label"]
improved_true_labels = improved_qml_predictions_dataframe["target_is_stable"]
improved_qml_predicted_labels = improved_qml_predictions_dataframe["improved_qml_predicted_label"]
threshold_true_labels = improved_qml_threshold_predictions_dataframe["target_is_stable"]
threshold_qml_predicted_labels = improved_qml_threshold_predictions_dataframe["threshold_qml_predicted_label"]
alignment_true_labels = improved_qml_alignment_predictions_dataframe["target_is_stable"]
alignment_qml_predicted_labels = improved_qml_alignment_predictions_dataframe["alignment_qml_predicted_label"]

metric_dataframe = pd.DataFrame([
    {
        "model": "QML quantum kernel",
        "accuracy": accuracy_score(true_labels, qml_predicted_labels),
        "stable_precision": precision_score(true_labels, qml_predicted_labels, zero_division=0),
        "stable_recall": recall_score(true_labels, qml_predicted_labels, zero_division=0),
        "stable_f1": f1_score(true_labels, qml_predicted_labels, zero_division=0),
    },
    {
        "model": "Tuned QML quantum kernel",
        "accuracy": accuracy_score(tuned_true_labels, tuned_qml_predicted_labels),
        "stable_precision": precision_score(tuned_true_labels, tuned_qml_predicted_labels, zero_division=0),
        "stable_recall": recall_score(tuned_true_labels, tuned_qml_predicted_labels, zero_division=0),
        "stable_f1": f1_score(tuned_true_labels, tuned_qml_predicted_labels, zero_division=0),
    },
    {
        "model": "Improved QML separate section",
        "accuracy": accuracy_score(improved_true_labels, improved_qml_predicted_labels),
        "stable_precision": precision_score(improved_true_labels, improved_qml_predicted_labels, zero_division=0),
        "stable_recall": recall_score(improved_true_labels, improved_qml_predicted_labels, zero_division=0),
        "stable_f1": f1_score(improved_true_labels, improved_qml_predicted_labels, zero_division=0),
    },
    {
        "model": "Improved QML threshold tuning",
        "accuracy": accuracy_score(threshold_true_labels, threshold_qml_predicted_labels),
        "stable_precision": precision_score(threshold_true_labels, threshold_qml_predicted_labels, zero_division=0),
        "stable_recall": recall_score(threshold_true_labels, threshold_qml_predicted_labels, zero_division=0),
        "stable_f1": f1_score(threshold_true_labels, threshold_qml_predicted_labels, zero_division=0),
    },
    {
        "model": "Improved QML kernel alignment",
        "accuracy": accuracy_score(alignment_true_labels, alignment_qml_predicted_labels),
        "stable_precision": precision_score(alignment_true_labels, alignment_qml_predicted_labels, zero_division=0),
        "stable_recall": recall_score(alignment_true_labels, alignment_qml_predicted_labels, zero_division=0),
        "stable_f1": f1_score(alignment_true_labels, alignment_qml_predicted_labels, zero_division=0),
    },
    {
        "model": "XGBoost same QML data",
        "accuracy": accuracy_score(true_labels, xgboost_predicted_labels),
        "stable_precision": precision_score(true_labels, xgboost_predicted_labels, zero_division=0),
        "stable_recall": recall_score(true_labels, xgboost_predicted_labels, zero_division=0),
        "stable_f1": f1_score(true_labels, xgboost_predicted_labels, zero_division=0),
    },
    {
        "model": "XGBoost full project",
        "accuracy": 0.9091,
        "stable_precision": 0.7300,
        "stable_recall": 0.7000,
        "stable_f1": 0.7100,
    },
]).round(4)

display(metric_dataframe)

metric_dataframe.set_index("model")[["accuracy", "stable_precision", "stable_recall", "stable_f1"]].plot(kind="bar", figsize=(9, 5))
plt.title("Model Performance Comparison")
plt.ylabel("Score")
plt.ylim(0, 1.05)
plt.xticks(rotation=15)
plt.grid(axis="y", alpha=0.25)
plt.show()"""
    cells.append(
        make_code_cell(
            metric_source,
            [make_table_output(metric_dataframe), make_figure_output(metric_figure)],
            execution_count,
        )
    )
    execution_count += 1

    confusion_figure = create_confusion_matrix_figure(
        qml_confusion_matrix,
        "Tuned QML Confusion Matrix",
    )
    confusion_dataframe = pd.DataFrame(
        qml_confusion_matrix,
        index=["actual_unstable", "actual_stable"],
        columns=["predicted_unstable", "predicted_stable"],
    )
    confusion_source = """qml_confusion_matrix = confusion_matrix(tuned_true_labels, tuned_qml_predicted_labels, labels=[0, 1])
confusion_dataframe = pd.DataFrame(
    qml_confusion_matrix,
    index=["actual_unstable", "actual_stable"],
    columns=["predicted_unstable", "predicted_stable"],
)
display(confusion_dataframe)

plt.figure(figsize=(5.8, 4.8))
plt.imshow(qml_confusion_matrix, cmap="Blues")
plt.title("Tuned QML Confusion Matrix")
plt.xticks([0, 1], ["Predicted unstable", "Predicted stable"])
plt.yticks([0, 1], ["Actual unstable", "Actual stable"])
for row_index in range(2):
    for column_index in range(2):
        plt.text(column_index, row_index, qml_confusion_matrix[row_index, column_index], ha="center", va="center")
plt.colorbar()
plt.show()"""
    cells.append(
        make_code_cell(
            confusion_source,
            [make_table_output(confusion_dataframe), make_figure_output(confusion_figure)],
            execution_count,
        )
    )
    execution_count += 1

    predictions_source = """sample_predictions_dataframe = tuned_qml_predictions_dataframe[
    [
        "material_id",
        "formula",
        "target_is_stable",
        "tuned_qml_predicted_label",
        "tuned_qml_stable_probability",
    ]
].head(10)
display(sample_predictions_dataframe)"""
    cells.append(
        make_code_cell(
            predictions_source,
            [make_table_output(sample_predictions_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    improved_summary_source = """improved_best_result = improved_qml_tuning_results_dataframe.sort_values(
    by=["cv_stable_f1", "cv_accuracy", "cv_stable_recall"],
    ascending=[False, False, False],
).iloc[0]

improved_true_labels = improved_qml_predictions_dataframe["target_is_stable"]
improved_qml_predicted_labels = improved_qml_predictions_dataframe["improved_qml_predicted_label"]

improved_summary_dataframe = pd.DataFrame([
    {
        "section": "Improved QML separate section",
        "feature_preparation": "feature importance + PCA",
        "best_kernel": improved_best_result["kernel_name"],
        "best_qubits": int(improved_best_result["pca_component_count"]),
        "angle_scale": improved_best_result["angle_scale"],
        "svm_c": improved_best_result["c_value"],
        "cv_stable_f1": improved_best_result["cv_stable_f1"],
        "test_accuracy": accuracy_score(improved_true_labels, improved_qml_predicted_labels),
        "test_stable_f1": f1_score(improved_true_labels, improved_qml_predicted_labels, zero_division=0),
    }
]).round(4)

display(improved_summary_dataframe)"""
    cells.append(
        make_code_cell(
            improved_summary_source,
            [make_table_output(improved_summary_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    improved_confusion_figure = create_confusion_matrix_figure(
        improved_qml_confusion_matrix,
        "Improved QML Confusion Matrix",
    )
    improved_confusion_dataframe = pd.DataFrame(
        improved_qml_confusion_matrix,
        index=["actual_unstable", "actual_stable"],
        columns=["predicted_unstable", "predicted_stable"],
    )
    improved_confusion_source = """improved_qml_confusion_matrix = confusion_matrix(
    improved_true_labels,
    improved_qml_predicted_labels,
    labels=[0, 1],
)
improved_confusion_dataframe = pd.DataFrame(
    improved_qml_confusion_matrix,
    index=["actual_unstable", "actual_stable"],
    columns=["predicted_unstable", "predicted_stable"],
)
display(improved_confusion_dataframe)

plt.figure(figsize=(5.8, 4.8))
plt.imshow(improved_qml_confusion_matrix, cmap="Blues")
plt.title("Improved QML Confusion Matrix")
plt.xticks([0, 1], ["Predicted unstable", "Predicted stable"])
plt.yticks([0, 1], ["Actual unstable", "Actual stable"])
for row_index in range(2):
    for column_index in range(2):
        plt.text(column_index, row_index, improved_qml_confusion_matrix[row_index, column_index], ha="center", va="center")
plt.colorbar()
plt.show()"""
    cells.append(
        make_code_cell(
            improved_confusion_source,
            [
                make_table_output(improved_confusion_dataframe),
                make_figure_output(improved_confusion_figure),
            ],
            execution_count,
        )
    )
    execution_count += 1

    improved_predictions_source = """improved_sample_predictions_dataframe = improved_qml_predictions_dataframe[
    [
        "material_id",
        "formula",
        "target_is_stable",
        "improved_qml_predicted_label",
        "improved_qml_stable_probability",
    ]
].head(10)
display(improved_sample_predictions_dataframe)"""
    cells.append(
        make_code_cell(
            improved_predictions_source,
            [make_table_output(improved_sample_predictions_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    threshold_summary_source = """improved_best_threshold_result = improved_qml_threshold_results_dataframe.sort_values(
    by=["cv_stable_f1", "cv_accuracy", "cv_stable_recall"],
    ascending=[False, False, False],
).iloc[0]

threshold_true_labels = improved_qml_threshold_predictions_dataframe["target_is_stable"]
threshold_qml_predicted_labels = improved_qml_threshold_predictions_dataframe["threshold_qml_predicted_label"]

threshold_summary_dataframe = pd.DataFrame([
    {
        "section": "Threshold experiment",
        "selected_threshold": improved_best_threshold_result["stable_threshold"],
        "cv_stable_f1": improved_best_threshold_result["cv_stable_f1"],
        "test_accuracy": accuracy_score(threshold_true_labels, threshold_qml_predicted_labels),
        "test_stable_precision": precision_score(threshold_true_labels, threshold_qml_predicted_labels, zero_division=0),
        "test_stable_recall": recall_score(threshold_true_labels, threshold_qml_predicted_labels, zero_division=0),
        "test_stable_f1": f1_score(threshold_true_labels, threshold_qml_predicted_labels, zero_division=0),
    }
]).round(4)

display(threshold_summary_dataframe)"""
    cells.append(
        make_code_cell(
            threshold_summary_source,
            [make_table_output(threshold_summary_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    threshold_confusion_figure = create_confusion_matrix_figure(
        threshold_qml_confusion_matrix,
        "Threshold-Tuned QML Confusion Matrix",
    )
    threshold_confusion_dataframe = pd.DataFrame(
        threshold_qml_confusion_matrix,
        index=["actual_unstable", "actual_stable"],
        columns=["predicted_unstable", "predicted_stable"],
    )
    threshold_confusion_source = """threshold_qml_confusion_matrix = confusion_matrix(
    threshold_true_labels,
    threshold_qml_predicted_labels,
    labels=[0, 1],
)
threshold_confusion_dataframe = pd.DataFrame(
    threshold_qml_confusion_matrix,
    index=["actual_unstable", "actual_stable"],
    columns=["predicted_unstable", "predicted_stable"],
)
display(threshold_confusion_dataframe)

plt.figure(figsize=(5.8, 4.8))
plt.imshow(threshold_qml_confusion_matrix, cmap="Blues")
plt.title("Threshold-Tuned QML Confusion Matrix")
plt.xticks([0, 1], ["Predicted unstable", "Predicted stable"])
plt.yticks([0, 1], ["Actual unstable", "Actual stable"])
for row_index in range(2):
    for column_index in range(2):
        plt.text(column_index, row_index, threshold_qml_confusion_matrix[row_index, column_index], ha="center", va="center")
plt.colorbar()
plt.show()"""
    cells.append(
        make_code_cell(
            threshold_confusion_source,
            [
                make_table_output(threshold_confusion_dataframe),
                make_figure_output(threshold_confusion_figure),
            ],
            execution_count,
        )
    )
    execution_count += 1

    alignment_summary_source = """improved_best_alignment_result = improved_qml_alignment_results_dataframe.sort_values(
    by=["cv_stable_f1", "cv_accuracy", "kernel_target_alignment"],
    ascending=[False, False, False],
).iloc[0]

alignment_true_labels = improved_qml_alignment_predictions_dataframe["target_is_stable"]
alignment_qml_predicted_labels = improved_qml_alignment_predictions_dataframe["alignment_qml_predicted_label"]

alignment_summary_dataframe = pd.DataFrame([
    {
        "section": "Kernel alignment experiment",
        "feature_set": improved_best_alignment_result["feature_set_name"],
        "feature_count": int(improved_best_alignment_result["feature_count"]),
        "kernel": improved_best_alignment_result["kernel_name"],
        "angle_scale": improved_best_alignment_result["angle_scale"],
        "svm_c": improved_best_alignment_result["c_value"],
        "kernel_target_alignment": improved_best_alignment_result["kernel_target_alignment"],
        "cv_stable_f1": improved_best_alignment_result["cv_stable_f1"],
        "test_accuracy": accuracy_score(alignment_true_labels, alignment_qml_predicted_labels),
        "test_stable_f1": f1_score(alignment_true_labels, alignment_qml_predicted_labels, zero_division=0),
    }
]).round(4)

display(alignment_summary_dataframe)"""
    cells.append(
        make_code_cell(
            alignment_summary_source,
            [make_table_output(alignment_summary_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    alignment_confusion_figure = create_confusion_matrix_figure(
        alignment_qml_confusion_matrix,
        "Kernel-Alignment QML Confusion Matrix",
    )
    alignment_confusion_dataframe = pd.DataFrame(
        alignment_qml_confusion_matrix,
        index=["actual_unstable", "actual_stable"],
        columns=["predicted_unstable", "predicted_stable"],
    )
    alignment_confusion_source = """alignment_qml_confusion_matrix = confusion_matrix(
    alignment_true_labels,
    alignment_qml_predicted_labels,
    labels=[0, 1],
)
alignment_confusion_dataframe = pd.DataFrame(
    alignment_qml_confusion_matrix,
    index=["actual_unstable", "actual_stable"],
    columns=["predicted_unstable", "predicted_stable"],
)
display(alignment_confusion_dataframe)

plt.figure(figsize=(5.8, 4.8))
plt.imshow(alignment_qml_confusion_matrix, cmap="Blues")
plt.title("Kernel-Alignment QML Confusion Matrix")
plt.xticks([0, 1], ["Predicted unstable", "Predicted stable"])
plt.yticks([0, 1], ["Actual unstable", "Actual stable"])
for row_index in range(2):
    for column_index in range(2):
        plt.text(column_index, row_index, alignment_qml_confusion_matrix[row_index, column_index], ha="center", va="center")
plt.colorbar()
plt.show()"""
    cells.append(
        make_code_cell(
            alignment_confusion_source,
            [
                make_table_output(alignment_confusion_dataframe),
                make_figure_output(alignment_confusion_figure),
            ],
            execution_count,
        )
    )
    execution_count += 1

    alignment_predictions_source = """alignment_sample_predictions_dataframe = improved_qml_alignment_predictions_dataframe[
    [
        "material_id",
        "formula",
        "target_is_stable",
        "alignment_qml_predicted_label",
        "alignment_qml_stable_probability",
    ]
].head(10)
display(alignment_sample_predictions_dataframe)"""
    cells.append(
        make_code_cell(
            alignment_predictions_source,
            [make_table_output(alignment_sample_predictions_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    repeated_split_source = """repeated_split_summary_rows = []
repeated_split_metric_columns = [
    "accuracy",
    "stable_precision",
    "stable_recall",
    "stable_f1",
]

for metric_name in repeated_split_metric_columns:
    repeated_split_summary_rows.append(
        {
            "metric": metric_name,
            "mean": best_qml_repeated_split_results_dataframe[metric_name].mean(),
            "standard_deviation": best_qml_repeated_split_results_dataframe[metric_name].std(ddof=1),
            "minimum": best_qml_repeated_split_results_dataframe[metric_name].min(),
            "maximum": best_qml_repeated_split_results_dataframe[metric_name].max(),
        }
    )

repeated_split_summary_dataframe = pd.DataFrame(repeated_split_summary_rows).round(4)
display(repeated_split_summary_dataframe)"""
    cells.append(
        make_code_cell(
            repeated_split_source,
            [make_table_output(repeated_split_summary_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    qml_vs_logistic_source = """qml_vs_logistic_comparison_rows = []
metric_names = ["accuracy", "stable_precision", "stable_recall", "stable_f1"]

for metric_name in metric_names:
    qml_mean = qml_vs_logistic_summary_dataframe[
        (qml_vs_logistic_summary_dataframe["model"] == "QML kernel classifier")
        & (qml_vs_logistic_summary_dataframe["metric"] == metric_name)
    ]["mean"].iloc[0]
    logistic_mean = qml_vs_logistic_summary_dataframe[
        (qml_vs_logistic_summary_dataframe["model"] == "Logistic Regression")
        & (qml_vs_logistic_summary_dataframe["metric"] == metric_name)
    ]["mean"].iloc[0]
    difference = qml_mean - logistic_mean
    if difference > 0:
        winner = "QML"
    elif difference < 0:
        winner = "Logistic Regression"
    else:
        winner = "Tie"

    qml_vs_logistic_comparison_rows.append(
        {
            "metric": metric_name,
            "qml_mean": round(qml_mean, 4),
            "logistic_mean": round(logistic_mean, 4),
            "qml_minus_logistic": round(difference, 4),
            "winner": winner,
        }
    )

qml_vs_logistic_comparison_dataframe = pd.DataFrame(qml_vs_logistic_comparison_rows)
display(qml_vs_logistic_comparison_dataframe)"""
    cells.append(
        make_code_cell(
            qml_vs_logistic_source,
            [make_table_output(qml_vs_logistic_comparison_dataframe)],
            execution_count,
        )
    )
    execution_count += 1

    conclusion_markdown = """# Presentation Conclusion

**What we achieved**

- Built a complete lithium battery material pipeline.
- Created India-focused material scoring and final shortlist.
- Added QML-primary DSS recommendation rankings for exact compound formulas.
- Trained XGBoost as the strong present-day classical benchmark.
- Prepared a balanced QML-ready dataset.
- Trained a first simulated quantum-kernel classifier as the quantum-future
  experiment.
- Tuned QML hyperparameters using 4-fold cross-validation.
- Added exhaustive QML feature-combination tuning with 8,388 saved
  configurations.
- Added a separate improved-QML section using feature importance, PCA, and an
  entangled-kernel search.
- Added a threshold experiment for the improved-QML stable probability.
- Added a kernel-alignment experiment for quantum-aware feature selection.
- Validated the best QML setup across 10 random train/test splits.
- Compared best QML with Logistic Regression on the same repeated splits.
- Added a gate-level visual diagram for the best 4-qubit QML feature map.

**Main model result**

- XGBoost full-project accuracy: **0.9091**
- XGBoost regressor MAE: **0.1005**
- QML accuracy on QML-ready test split: **0.8100**
- Tuned QML accuracy on QML-ready test split: **0.8200**
- Tuned QML stable F1 on QML-ready test split: **0.8269**
- Improved QML separate-section accuracy: **0.8150**
- Improved QML separate-section stable F1: **0.8230**
- Improved QML threshold-tuned accuracy: **0.8200**
- Improved QML threshold-tuned stable F1: **0.8269**
- Improved QML kernel-alignment accuracy: **0.8200**
- Improved QML kernel-alignment stable F1: **0.8302**
- Repeated-split mean accuracy: **0.8550**
- Repeated-split mean stable F1: **0.8583**
- QML vs Logistic mean accuracy: **0.8550 vs 0.8410**
- QML vs Logistic mean stable F1: **0.8583 vs 0.8473**
- Same-data XGBoost accuracy: **0.8300**

**Safe interpretation**

XGBoost is stronger on the full tabular benchmark, but the final DSS is
quantum-led. QML gives the first recommendation signal and XGBoost is used as a
corrective backup when QML is uncertain or when the models disagree. The safe
student-level point is that quantum feature spaces are future-facing for
materials discovery, while classical ML can still act as a practical safety
check today.
"""
    cells.append(make_markdown_cell(conclusion_markdown, "markdown-conclusion"))

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": sys.version.split()[0],
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    notebook_path.write_text(json.dumps(notebook, indent=2))
    print(f"Created notebook: {notebook_path}")
    print(f"Cells: {len(cells)}")


if __name__ == "__main__":
    main()
