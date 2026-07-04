# Qiskit Implementation Summary

Generated on: 2026-07-04

## What Changed

The QML part now uses Qiskit directly.

The shared implementation is in:

`scripts/qiskit_quantum_kernel.py`

## Qiskit Objects Used

| Object | Purpose |
| --- | --- |
| `QuantumCircuit` | Builds the material feature-map circuit. |
| `ry` gate | Encodes each scaled material feature as a qubit rotation. |
| `cp` gate | Adds adjacent-qubit phase interaction for the entangled kernel. |
| `Statevector.from_instruction` | Simulates the circuit and extracts the quantum state. |

## Circuit Idea

Each material row becomes a small quantum circuit.

For each selected feature:

`angle = angle_scale * feature_value`

Then Qiskit applies:

`RY(angle)`

For the entangled kernel, adjacent feature pairs also receive:

`CP(entanglement_strength * feature_i * feature_j)`

## Kernel Idea

After Qiskit gives the statevector, the kernel between two materials is:

`K(x, y) = |<phi(x), phi(y)>|^2`

This kernel matrix is passed into `SVC(kernel="precomputed")`.

## Honest Limitation

This is Qiskit Statevector simulation on a local machine.

It is not yet an IBM quantum hardware run.
