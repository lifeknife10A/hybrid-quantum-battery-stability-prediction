# QML Circuit Diagram Summary

Generated on: 2026-06-29

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

| qubit | feature | angle |
| --- | --- | --- |
| q0 | formation_energy_per_atom | theta_0 = pi * scaled formation_energy_per_atom |
| q1 | has_o | theta_1 = pi * scaled has_o |
| q2 | space_group_number | theta_2 = pi * scaled space_group_number |
| q3 | theoretical | theta_3 = pi * scaled theoretical |

## Circuit Stages

| stage | meaning |
| --- | --- |
| Initialize | Start each qubit at the zero state. |
| RY feature encoding | Convert each scaled feature value into a rotation angle. |
| Controlled phase | Add adjacent-qubit entanglement using feature-pair products. |
| Quantum kernel | Compare two encoded materials using squared state overlap. |
| SVC classifier | Use the precomputed kernel matrix for stable/unstable prediction. |

## Diagram Output

- `data/processed/qml circuit diagram.png`

## How To Explain In Presentation

Each lithium material is converted into four scaled numbers. Each number rotates
one qubit using an RY gate. Then adjacent qubits are connected using controlled
phase gates. Finally, two encoded materials are compared using the quantum
kernel formula `K(x, y) = |<phi(x)|phi(y)>|^2`, and the resulting kernel matrix
is used by an SVC classifier.
