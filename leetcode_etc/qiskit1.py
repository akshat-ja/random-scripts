import qiskit.quantum_info as qi
from qiskit.circuit.library import FourierChecking
from qiskit.visualization import plot_histogram

f = [1,-1,-1,-1]
g = [1,1,-1,-1]

circ = FourierChecking(f=f, g=g)
circ.draw()

zero = qi.Statevector.from_label(00)
sv = zero.evolve(circ)
probs = sv.probabilities_dict()
plot_histogram(probs)