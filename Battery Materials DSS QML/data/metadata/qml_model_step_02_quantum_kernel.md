# QML Model Step 02: Quantum Kernel

Generated on: 2026-06-28

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

- Number of features/qubits: 10
- Quantum state length: 1024

## Important Note

This is a simulated QML baseline. It does not run on real quantum hardware yet.
It is still useful because it tests the QML-style feature map and kernel
classification workflow.
