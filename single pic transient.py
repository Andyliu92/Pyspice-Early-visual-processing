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
Image_path = "D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\img\\tiny.jpg"
img = cv.imread(Image_path)
# -----------------------------------------------------

# --------------- circuit parameter -------------------
row = img.shape[0]
column = img.shape[1]
r_net = 620@u_Ohm
r_out = 1200@u_Ohm
c = 0.2@u_mF
c_init = 0@u_V
v_ambient = 0@u_V
v_input = media.img2Voltage(Image_path)
# ------------------------------------------------------

# -------------- Analysis Parameter --------------------
# Transient Analysis
startTime = 0@u_ms
stepTime = 10@u_ms
finalTime = 1000@u_ms
# ------------------------------------------------------

# -------------- Result settings -----------------------
ResultNodeType = 'output'  # output for final result, alternative: vin, net
Frame_quantity = 100
videoOutPath = 'D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\out\\out.avi'
imageOutPath = 'D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\out\\out'
# ------------------------------------------------------


logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass


# -------------- simulation ----------------------
circuitR = Circuit('channel R')
circuitG = Circuit('channel G')
circuitB = Circuit('channel B')

circuit = [circuitB, circuitG, circuitR]
analysis = []
out = []
sim_result = np.empty((3, Frame_quantity, row, column), dtype=np.float32)

v_input = data.logProc(v_input)
for i in range(0, 3, 1):
    print('\n\n\n----------------%d th iterate-----------------' % i)

    simulator = circuit[i].simulator(temperature=25, nominal_temperature=25)
    print('Simulator created')

    # circuit specification
    cg.staticInput(circuit[i], row, column, r_net, r_out,
                   v_input[:, :, i], c, mode='square')
    cg.setInit(simulator, c_init, row, column)
    print('circuit generated')

    analysis.append(simulator.transient(
        start_time=startTime, step_time=stepTime, end_time=finalTime))
    print('analysis finished')

    out.append(data.format(analysis[i]))
    print('output dictionary transformed')

    sim_result[i] = data.frameAll(out[i], ResultNodeType,
                                  row, column, Frame_quantity)
    print('got sim result')

sim_result = data.std_8b(sim_result)

media.res2img(sim_result, imageOutPath, row, column)
media.res2Video(sim_result, videoOutPath, row, column)
