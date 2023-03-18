from qiskit import *
from qiskit.visualization import plot_histogram
import numpy as np


def NOT(inp):
    """An NOT gate.

    Parameters:
        inp (str): Input, encoded in qubit 0.

    Returns:
        QuantumCircuit: Output NOT circuit.
        str: Output value measured from qubit 0.
    """

    # A quantum circuit with a single qubit and a single classical bit
    qc = QuantumCircuit(1, 1)
    qc.reset(0)
    qc.initialize(inp)

    # We encode '0' as the qubit state |0⟩, and '1' as |1⟩
    # Since the qubit is initially |0⟩, we don't need to do anything for an input of '0'
    # For an input of '1', we do an x to rotate the |0⟩ to |1⟩

    # barrier between input state and gate operation
    qc.barrier()

    # Now we've encoded the input, we can do a NOT on it using x
    qc.x(0)

    # barrier between gate operation and measurement
    qc.barrier()

    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc.measure(0, 0)
    qc.draw('mpl')

    # We'll run the program on a simulator
    backend = Aer.get_backend('aer_simulator')
    # Since the output will be deterministic, we can use just a single shot to get it
    job = backend.run(qc, shots=1, memory=True)
    output = job.result().get_memory()[0]

    return qc, output


def AND(inp1, inp2):
    """An AND gate.

    Parameters:
        inpt1 (str): Input 1, encoded in qubit 0.
        inpt2 (str): Input 2, encoded in qubit 1.

    Returns:
        QuantumCircuit: Output XOR circuit.
        str: Output value measured from qubit 2.
    """
    qc = QuantumCircuit(3, 1)
    qc.reset(range(2))

    qc.initialize('0' + inp2 + inp1)  # 000

    qc.barrier()

    # this is where your program for quantum AND gate goes
    qc.ccx(0, 1, 2)  # 011 -> 111, 0

    qc.barrier()
    qc.measure(2, 0)  # output from qubit 2 is measured

    # We'll run the program on a simulator
    backend = Aer.get_backend('aer_simulator')
    # Since the output will be deterministic, we can use just a single shot to get it
    job = backend.run(qc, shots=1, memory=True)
    output = job.result().get_memory()[0]

    return qc, output


def XOR(inp1, inp2):
    """An XOR gate.

    Parameters:
        inpt1 (str): Input 1, encoded in qubit 0.
        inpt2 (str): Input 2, encoded in qubit 1.

    Returns:
        QuantumCircuit: Output XOR circuit.
        str: Output value measured from qubit 1.
    """

    qc = QuantumCircuit(2, 1)
    qc.reset(range(2))
    qc.initialize(inp2 + inp1)

    # barrier between input state and gate operation
    qc.barrier()

    # this is where your program for quantum XOR gate goes
    qc.cx(0, 1)  # 01-> 01, 00 -> 00, 10 -> 11, 11 -> 10
    # barrier between input state and gate operation
    qc.barrier()

    qc.measure(1, 0)  # output from qubit 1 is measured

    # We'll run the program on a simulator
    backend = Aer.get_backend('aer_simulator')
    # Since the output will be deterministic, we can use just a single shot to get it
    job = backend.run(qc, shots=1, memory=True)
    output = job.result().get_memory()[0]

    return qc, output


def full_adder(a, b, c_in):
    out1, a_XOR_b = XOR(a, b)

    out2, S = XOR(c_in, a_XOR_b)

    out3, a_AND_b = AND(a, b)
    out4, a_NAND_b = NOT(a_AND_b)

    out5, ab_AND_c = AND(a_XOR_b, c_in)
    out6, ab_NAND_c = NOT(ab_AND_c)

    out7, cout_temp = AND(ab_NAND_c, a_NAND_b)
    out8, C_out = NOT(cout_temp)

    return S, C_out


# Full Adder Truth Table
print("A\tB\tCin\t(Sum, Cout)")
for a in ['0', '1']:
    for b in ['0', '1']:
        for c_in in ['0', '1']:
            print(f"{a}\t{b}\t{c_in}", end="\t")
            print(full_adder(a, b, c_in))
