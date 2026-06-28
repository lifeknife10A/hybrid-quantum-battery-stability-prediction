from datetime import date
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd


project_folder = Path(__file__).resolve().parents[1]
processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"

diagram_path = processed_folder / "qml circuit diagram.png"
summary_path = metadata_folder / "qml_circuit_diagram_summary.md"

feature_rows = [
    {
        "qubit": "q0",
        "feature": "formation_energy_per_atom",
        "angle": "theta_0 = pi * scaled formation_energy_per_atom",
    },
    {
        "qubit": "q1",
        "feature": "has_o",
        "angle": "theta_1 = pi * scaled has_o",
    },
    {
        "qubit": "q2",
        "feature": "space_group_number",
        "angle": "theta_2 = pi * scaled space_group_number",
    },
    {
        "qubit": "q3",
        "feature": "theoretical",
        "angle": "theta_3 = pi * scaled theoretical",
    },
]


def dataframe_to_markdown(dataframe):
    if dataframe.empty:
        return "_No rows found._"

    headers = list(dataframe.columns)
    rows = []

    for _, dataframe_row in dataframe.iterrows():
        row_values = []
        for column_name in headers:
            value_text = str(dataframe_row[column_name]).replace("|", "/")
            row_values.append(value_text)
        rows.append(row_values)

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row_values) + " |" for row_values in rows]
    return "\n".join([header_line, separator_line] + row_lines)


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


def create_circuit_figure():
    feature_names = [row["feature"] for row in feature_rows]
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


def write_summary():
    feature_dataframe = pd.DataFrame(feature_rows)
    gate_dataframe = pd.DataFrame(
        [
            {
                "stage": "Initialize",
                "meaning": "Start each qubit at the zero state.",
            },
            {
                "stage": "RY feature encoding",
                "meaning": "Convert each scaled feature value into a rotation angle.",
            },
            {
                "stage": "Controlled phase",
                "meaning": "Add adjacent-qubit entanglement using feature-pair products.",
            },
            {
                "stage": "Quantum kernel",
                "meaning": "Compare two encoded materials using squared state overlap.",
            },
            {
                "stage": "SVC classifier",
                "meaning": "Use the precomputed kernel matrix for stable/unstable prediction.",
            },
        ]
    )

    report_text = f"""# QML Circuit Diagram Summary

Generated on: {date.today().isoformat()}

## Purpose

This step adds a gate-level visual explanation of the best QML setup used in
the project. The diagram is for presentation and report writing.

## Important Clarification

This is a simulated quantum-kernel feature map. It is written like a quantum
circuit so the idea is easier to explain, but the current project still runs on
classical simulation and does not execute on real quantum hardware.

## Best QML Setup Shown

| Item | Value |
| --- | --- |
| Qubits | 4 |
| Kernel | `entangled_pi` |
| Angle scale | `pi` |
| Classifier | SVC with precomputed quantum kernel |
| Main result | Mean stable F1 0.8583 across 10 repeated balanced splits |

## Qubit To Feature Mapping

{dataframe_to_markdown(feature_dataframe)}

## Circuit Stages

{dataframe_to_markdown(gate_dataframe)}

## Diagram Output

- `data/processed/qml circuit diagram.png`

## How To Explain In Presentation

Each lithium material is converted into four scaled numbers. Each number rotates
one qubit using an RY gate. Then adjacent qubits are connected using controlled
phase gates. Finally, two encoded materials are compared using the quantum
kernel formula `K(x, y) = |<phi(x)|phi(y)>|^2`, and the resulting kernel matrix
is used by an SVC classifier.
"""
    summary_path.write_text(report_text)


def main():
    processed_folder.mkdir(parents=True, exist_ok=True)
    metadata_folder.mkdir(parents=True, exist_ok=True)

    figure = create_circuit_figure()
    figure.savefig(diagram_path, dpi=200, bbox_inches="tight")
    plt.close(figure)

    write_summary()

    print(f"Created: {diagram_path}")
    print(f"Created: {summary_path}")


if __name__ == "__main__":
    main()
