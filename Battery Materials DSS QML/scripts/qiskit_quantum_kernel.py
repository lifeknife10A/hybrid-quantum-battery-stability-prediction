import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def create_qiskit_feature_map_circuit(
    feature_row,
    angle_scale_value,
    entanglement_strength=0.0,
):
    number_of_qubits = len(feature_row)
    circuit = QuantumCircuit(number_of_qubits)

    for feature_index in range(number_of_qubits):
        feature_value = float(feature_row[feature_index])
        angle = angle_scale_value * feature_value
        circuit.ry(angle, feature_index)

    if entanglement_strength != 0.0:
        for feature_index in range(number_of_qubits - 1):
            first_feature_value = float(feature_row[feature_index])
            second_feature_value = float(feature_row[feature_index + 1])
            phase_angle = (
                entanglement_strength
                * first_feature_value
                * second_feature_value
            )
            circuit.cp(phase_angle, feature_index, feature_index + 1)

    return circuit


def create_qiskit_state_table(
    feature_table,
    angle_scale_value,
    entanglement_strength=0.0,
):
    state_rows = []

    for feature_row in feature_table:
        circuit = create_qiskit_feature_map_circuit(
            feature_row,
            angle_scale_value,
            entanglement_strength,
        )
        statevector = Statevector.from_instruction(circuit)
        quantum_state = np.asarray(statevector.data, dtype=np.complex128)
        state_rows.append(quantum_state)

    state_table = np.vstack(state_rows)
    return state_table


def create_qiskit_kernel_matrix(left_states, right_states):
    inner_product_matrix = left_states @ np.conjugate(right_states.T)
    kernel_matrix = np.abs(inner_product_matrix) ** 2
    return kernel_matrix
