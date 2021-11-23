from PySpice.Unit import *
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
import PySpice
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import module.circuitGen as cg
import module.data as data

# --------------- circuit parameter -------------------
row = 11
column = 11
r_net = 620@u_Ohm
r_out = 1200@u_Ohm
c = 240@u_uF
c_init = 0@u_V
v_ambient = 0@u_V
# ------------------------------------------------------

# -------------- Analysis Parameter --------------------
# Transient Analysis
steptime = 40@u_ms
finaltime = 40000@u_ms
# ------------------------------------------------------

# -------------- Result settings -----------------------
ResultNodeType = 'output'  # output for final result, alternative: vin, net
# ------------------------------------------------------

# -------------- Program Settings ----------------------
echo = False
# ------------------------------------------------------


logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass


circuit = Circuit('early visual processing')

simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# circuit specification
cg.staticInput(circuit, row, column, r_net, r_out,
               v_input, c, mode='square')

analysis = simulator.transient(step_time=steptime, end_time=finaltime)

out_dict = data.format(analysis)

sim_result = data.getFrame()
