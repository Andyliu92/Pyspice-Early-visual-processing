from PySpice.Unit import *
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
import PySpice
import sys
import numpy as np
import module.circuitGen as cg
import module.data as data
import module.media as media
import cv2 as cv

# -------------- Input parameter ----------------------
Image_path = "D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\img\\test.jpg"
img = cv.imread(Image_path)
# -----------------------------------------------------

# --------------- circuit parameter -------------------
row = img.shape[0]
column = img.shape[1]
r_net = 620@u_Ohm
r_out = 1200@u_Ohm
c = 240@u_uF
c_init = 0@u_V
v_ambient = 0@u_V
# ------------------------------------------------------

# -------------- Analysis Parameter --------------------
# Transient Analysis
steptime = 0@u_ms
finaltime = 40000@u_ms
# ------------------------------------------------------

# -------------- Result settings -----------------------
ResultNodeType = 'output'  # output for final result, alternative: vin, net
Frame_quantity = 100
# ------------------------------------------------------


logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass

v_input = media.img2Voltage(Image_path)

# -------------- simulation ----------------------
circuitR = Circuit('channel R')
circuitG = Circuit('channel G')
circuitB = Circuit('channel B')

circuit = [circuitB, circuitG, circuitR]
analysis = []
out = []
sim_result = np.empty((Frame_quantity, row, column), dtype=np.float32)

for i in range(0, 3, 1):
    simulator = circuit[i].simulator(temperature=25, nominal_temperature=25)

    # circuit specification
    cg.staticInput(circuit[i], row, column, r_net, r_out,
                   v_input[:, i], c, mode='square')

    analysis.append(simulator.transient(
        step_time=steptime, end_time=finaltime))

    out.append(data.format(analysis[i]))

    sim_result[:, i] = data.frameAll(out[i], ResultNodeType,
                                     row, column, Frame_quantity)
