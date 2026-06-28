from pathlib import Path
import base64
import io
import json
import sys

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
notebook_path = project_folder / "Summer Vacation Main Presentation.ipynb"

lithium_scored_path = processed_folder / "lithium india scored.csv"
final_shortlist_path = processed_folder / "final india battery shortlist.csv"
qml_ready_path = processed_folder / "qml_ready_lithium_india.csv"
qml_predictions_path = processed_folder / "qml baseline predictions.csv"
tuned_qml_predictions_path = processed_folder / "qml tuned best predictions.csv"


def make_markdown_output(markdown_text):
    return {
        "output_type": "display_data",
        "data": {
            "text/markdown": markdown_text,
            "text/plain": markdown_text,
        },
        "metadata": {},
    }


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
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs,
        "source": source_text.splitlines(keepends=True),
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


def create_metric_figure(metric_dataframe):
    figure, axis = plt.subplots(figsize=(9, 5))
    bar_width = 0.18
    metric_names = ["accuracy", "stable_precision", "stable_recall", "stable_f1"]
    model_names = metric_dataframe["model"].tolist()
    x_positions = list(range(len(metric_names)))

    colors = ["#315f8c", "#4f86c6", "#d88c2d", "#5f8f45"]
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


def create_confusion_matrix_figure(confusion_table):
    figure, axis = plt.subplots(figsize=(5.8, 4.8))
    image = axis.imshow(confusion_table, cmap="Blues")
    axis.set_title("Tuned QML Confusion Matrix")
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
    qml_ready_dataframe = pd.read_csv(qml_ready_path)
    qml_predictions_dataframe = pd.read_csv(qml_predictions_path)
    tuned_qml_predictions_dataframe = pd.read_csv(tuned_qml_predictions_path)

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
            {"parameter": "Train/test split", "value": "80/20"},
            {"parameter": "Random state", "value": "42"},
        ]
    )

    true_labels = qml_predictions_dataframe["target_is_stable"]
    qml_predicted_labels = qml_predictions_dataframe["qml_predicted_label"]
    xgboost_predicted_labels = qml_predictions_dataframe[
        "xgboost_same_data_predicted_label"
    ]
    tuned_true_labels = tuned_qml_predictions_dataframe["target_is_stable"]
    tuned_qml_predicted_labels = tuned_qml_predictions_dataframe[
        "tuned_qml_predicted_label"
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

    sample_predictions_dataframe = tuned_qml_predictions_dataframe[
        [
            "material_id",
            "formula",
            "target_is_stable",
            "tuned_qml_predicted_label",
            "tuned_qml_stable_probability",
        ]
    ].head(10)

    cells = []
    execution_count = 1

    title_markdown = """# Quantum Machine Learning for Lithium-Ion Battery Materials Discovery

**Presentation notebook**

Goal: identify lithium-ion battery material candidates using Materials Project
data, XGBoost, India-focused screening, and a first QML baseline.
"""
    cells.append(
        make_code_cell(
            """from IPython.display import Markdown, display
display(Markdown(\"\"\"# Quantum Machine Learning for Lithium-Ion Battery Materials Discovery

**Presentation notebook**

Goal: identify lithium-ion battery material candidates using Materials Project
data, XGBoost, India-focused screening, and a first QML baseline.
\"\"\"))""",
            [make_markdown_output(title_markdown)],
            execution_count,
        )
    )
    execution_count += 1

    data_loading_source = """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

project_folder = Path.cwd()
processed_folder = project_folder / "data" / "processed"

lithium_scored_dataframe = pd.read_csv(processed_folder / "lithium india scored.csv")
final_shortlist_dataframe = pd.read_csv(processed_folder / "final india battery shortlist.csv")
qml_ready_dataframe = pd.read_csv(processed_folder / "qml_ready_lithium_india.csv")
qml_predictions_dataframe = pd.read_csv(processed_folder / "qml baseline predictions.csv")
tuned_qml_predictions_dataframe = pd.read_csv(processed_folder / "qml tuned best predictions.csv")

dataset_summary = pd.DataFrame([
    {"dataset": "Lithium India scored", "rows": len(lithium_scored_dataframe), "columns": len(lithium_scored_dataframe.columns)},
    {"dataset": "Final India shortlist", "rows": len(final_shortlist_dataframe), "columns": len(final_shortlist_dataframe.columns)},
    {"dataset": "QML-ready dataset", "rows": len(qml_ready_dataframe), "columns": len(qml_ready_dataframe.columns)},
    {"dataset": "QML test predictions", "rows": len(qml_predictions_dataframe), "columns": len(qml_predictions_dataframe.columns)},
    {"dataset": "Tuned QML test predictions", "rows": len(tuned_qml_predictions_dataframe), "columns": len(tuned_qml_predictions_dataframe.columns)},
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

    quantum_parameters_source = """quantum_parameters_dataframe = pd.DataFrame([
    {"parameter": "QML model type", "value": "Simulated quantum kernel classifier"},
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

    metric_figure = create_metric_figure(metric_dataframe)
    metric_source = """true_labels = qml_predictions_dataframe["target_is_stable"]
qml_predicted_labels = qml_predictions_dataframe["qml_predicted_label"]
xgboost_predicted_labels = qml_predictions_dataframe["xgboost_same_data_predicted_label"]
tuned_true_labels = tuned_qml_predictions_dataframe["target_is_stable"]
tuned_qml_predicted_labels = tuned_qml_predictions_dataframe["tuned_qml_predicted_label"]

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

    confusion_figure = create_confusion_matrix_figure(qml_confusion_matrix)
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

    conclusion_markdown = """# Presentation Conclusion

**What we achieved**

- Built a complete lithium battery material pipeline.
- Created India-focused material scoring and final shortlist.
- Trained XGBoost as the classical baseline.
- Prepared a balanced QML-ready dataset.
- Trained a first simulated quantum-kernel classifier.
- Tuned QML hyperparameters using 4-fold cross-validation.

**Main model result**

- QML accuracy on QML-ready test split: **0.8100**
- Tuned QML accuracy on QML-ready test split: **0.8200**
- Tuned QML stable F1 on QML-ready test split: **0.8269**
- Same-data XGBoost accuracy: **0.8300**

**Next step**

Create final report visuals and try entangled QML feature maps or
hardware-oriented circuits.
"""
    cells.append(
        make_code_cell(
            """display(Markdown(\"\"\"# Presentation Conclusion

**What we achieved**

- Built a complete lithium battery material pipeline.
- Created India-focused material scoring and final shortlist.
- Trained XGBoost as the classical baseline.
- Prepared a balanced QML-ready dataset.
- Trained a first simulated quantum-kernel classifier.
- Tuned QML hyperparameters using 4-fold cross-validation.

**Main model result**

- QML accuracy on QML-ready test split: **0.8100**
- Tuned QML accuracy on QML-ready test split: **0.8200**
- Tuned QML stable F1 on QML-ready test split: **0.8269**
- Same-data XGBoost accuracy: **0.8300**

**Next step**

Create final report visuals and try entangled QML feature maps or
hardware-oriented circuits.
\"\"\"))""",
            [make_markdown_output(conclusion_markdown)],
            execution_count,
        )
    )

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
