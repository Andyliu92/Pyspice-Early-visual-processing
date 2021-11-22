import numpy as np
import matplotlib.pyplot as ply
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

circuit = Circuit('voltage divider')

# add components to the circuit
circuit.V('input', 'in', circuit.gnd, 10@u_V)
circuit.R(1, 'in', 'out', 9@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 1@u_kOhm)

# Create a Simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Print the Circuits:
print("The circuit/Netlist : \n \n", circuit)

# Print the circuit and simulator settings
print("The Simulator : \n \n ", simulator)


# Run Analysis
analysis = simulator.operating_point()

print(analysis)


# Extract data from node
print(analysis.nodes['in'])
print(str(analysis.nodes['in']))
print(float(analysis.nodes['in']))
print(str(analysis.nodes['out']))
print(float(analysis.nodes['out']))

exit()
