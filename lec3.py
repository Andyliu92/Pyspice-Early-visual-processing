'''
Content:
1. Create a model
2. Raw Spice
    take the def of the original parameter and changet it when using.
    use the SPICE syntax
3. SubCircuit
    2 ways to implement subcircuits:
        a. SubCircuitFactory
        b. class subcircuit (yes)
'''

import numpy as np
import matplotlib.pyplot as ply
import sys

import PySpice
from PySpice.Spice.Netlist import Circuit, SubCircuit, SubCircuitFactory
import PySpice.Logging.Logging as Logging
from PySpice.Unit import *

logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass

# Functions
# 18 min of the lec 2 on youtube
# Get dictionary containing SPICE sim data
# The dictionary is created by pairing each of the nodes to its corresponding output voltage value array
# This Provides a more managable format


def format_output(analysis):
    sim_res_dict = {}  # Create a dict

    for node in analysis.nodes.values():
        data_label = "%s" % str(node)
        sim_res_dict[data_label] = np.array(node)

    return sim_res_dict

# Sub Circuit


class MySubCircuit(SubCircuit):

    __nodes__ = ('t_in', 't_out')

    def __init__(self, name, R=1@u_kOhm):
        SubCircuit.__init__(self, name, *self.__nodes__)
        self.R(1, 't_in', 't_out', R)
        self.Diode(1, 't_in', 't_out', model='MyDiode')
        return


# Create a Circuit
circuit = Circuit('lec3_diode')

# Define the parameter of the component in the circuit (exp.1N4148PH signal diode)
circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458 @
              u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)

# add components to the circuit
circuit.V('input', 1, circuit.gnd, 10@u_V)
circuit.R(1, 1, 2, 9@u_kOhm)
circuit.Diode(1, 2, 3, model='MyDiode')

circuit.subcircuit(MySubCircuit("sub1", R=1@u_kOhm))

circuit.X(1, 'sub1', 3, circuit.gnd)

# Print the Circuits:
print("The circuit/Netlist : \n \n", circuit)


# Create a Simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)


# Run Analysis
analysis = simulator.operating_point()

out_dict = format_output(analysis)

print(out_dict)

'''


# Print the circuit and simulator settings
print("The Simulator : \n \n ", simulator)



print(analysis)


# Extract data from node
print(analysis.nodes['in'])
print(str(analysis.nodes['in']))
print(float(analysis.nodes['in']))
print(str(analysis.nodes['out']))
print(float(analysis.nodes['out']))

exit()
'''

exit()
