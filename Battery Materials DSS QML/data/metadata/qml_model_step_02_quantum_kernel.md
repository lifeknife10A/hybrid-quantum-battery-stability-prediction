# QML Model Step 02: Quantum Kernel

Generated on: 2026-07-04

## QML Method Used

Qiskit Statevector quantum kernel classifier.

## Feature Map

Each scaled feature is treated as one Qiskit qubit rotation:

`angle = pi * scaled_feature_value`

In the code, this is built with a Qiskit `QuantumCircuit` using `RY` gates.
Qiskit `Statevector.from_instruction(...)` then gives the simulated quantum
state.

Each qubit follows this simple rotation idea:

`[cos(angle / 2), sin(angle / 2)]`

The full material state is produced by Qiskit from the circuit.

## Kernel Formula

The kernel value between two materials is:

`K(x, y) = |<phi(x), phi(y)>|^2`

## Size

- Number of features/qubits: 10
- Quantum state length: 1024

## Important Note

This is a Qiskit Statevector simulation. It does not run on IBM quantum
hardware yet. It is still useful because it tests the QML-style feature map and
kernel classification workflow with actual Qiskit circuit objects.
