'''
Content:
    1. DC Sweep (4.1)
    2. Custom DC Sweeps
        using a custom dc source
'''

import numpy as np
import matplotlib.pyplot as plt
import sys

import PySpice
from PySpice.Spice.Netlist import Circuit
import PySpice.Logging.Logging as Logging
from PySpice.Unit import *

logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass

# Functions
# 18 min of the lec 2 on youtube


# Create a Circuit

circuit = Circuit('tutorial 4_1')

# Define the parameter of the component in the circuit (exp.1N4148PH signal diode)
circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458 @
              u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)

# add components to the circuit
circuit.V('input', 'img', circuit.gnd, 0@u_V)  # imaginary!!
circuit.Diode(1, 1, 2, model='MyDiode')
circuit.R(1, 2, circuit.gnd, 1@u_kOhm)

data = [0, 1, 5, -4, 6, -3]

# using the imaginary voltage as voltage value
circuit.B('Bs', 1, circuit.gnd, v=v_seq)  # piecewise like arbitrary input


# Create a Simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Print the Circuits:
print("The circuit/Netlist : \n \n", circuit)

# Print the circuit and simulator settings
print("The Simulator : \n \n ", simulator)


# Run Analysis
analysis = simulator.dc(Vinput=slice(1, 4, 1))

print("Node : ", str(analysis["1"]), "values: ", np.array(analysis['1']))
print("Node : ", str(analysis["2"]), "values: ", np.array(analysis['2']))

# Plot Graph
fig = plt.figure()

plt.plot(np.array(analysis['1']), np.array(analysis['2']))
plt.xlabel('Input Voltage (1)')
plt.ylabel('Output Voltage (2)')

fig.savefig("Sim_outout.png", dpi=300)
plt.close(fig)

exit()
