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
import time

start_time = time.time()
# -------------- Input parameter ----------------------
# set path to "0" is you want it to be 0 state
Input_Image_path = "D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\img\\tiny.jpg"
Init_Image_path = "0"
# -----------------------------------------------------


# --------------- circuit parameter -------------------
r_net = 620@u_Ohm
r_out = 1200@u_Ohm
c = 0.2@u_mF
v_ambient = 0@u_V
# ------------------------------------------------------

# -------------- Analysis Parameter --------------------
# Transient Analysis
startTime = 0@u_ms
stepTime = 10@u_ms
finalTime = 2000@u_ms
# ------------------------------------------------------

# -------------- Result settings -----------------------
ResultNodeType = 'output'  # output for final result, alternative: vin, net
Frame_quantity = 200
videoOutPath = 'D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\out\\out.avi'
imageOutPath = 'D:\\Work\\04 Research Project\\21.08.19 Early Visual Processing\\pyspice\\assets\\out\\out'
# ------------------------------------------------------

# -------------- setting up pyspice ---------------
logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass

# -------------- error checking ------------------
if Init_Image_path == '0' and Input_Image_path == '0':
    print('No input and no init condition. No Response.')
    exit()

# --------------- input reading --------------------
if Init_Image_path == '0':
    v_input = media.img2npArray(Input_Image_path)
    c_init = np.zeros(v_input.shape, dtype=np.float32)
elif Input_Image_path == '0':
    c_init = media.img2npArray(Init_Image_path)
    v_input = np.zeros(c_init.shape, dtype=np.float32)
else:
    c_init = media.img2npArray(Init_Image_path)
    v_input = media.img2npArray(Input_Image_path)

row = v_input.shape[0]
column = v_input.shape[1]

# -------------- simulation ----------------------
circuitR = Circuit('channel R')
circuitG = Circuit('channel G')
circuitB = Circuit('channel B')

circuit = [circuitB, circuitG, circuitR]
analysis = []
out = []
sim_result = np.empty((3, Frame_quantity, row, column), dtype=np.float32)

# v_input = data.logProc(v_input)  # log for the first stage of visual processing. No need for 8-bit image.

for i in range(0, 3, 1):
    print('\n---------------- channel %d -----------------\n' % (i+1))

    simulator = circuit[i].simulator(temperature=25, nominal_temperature=25)
    print('Simulator created')

    # circuit specification
    cg.staticInput(circuit[i], row, column, r_net, r_out,
                   v_input[:, :, i], c, mode='square')
    cg.setInit(simulator, c_init[:, :, i], row, column)
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


media.res2img(sim_result, imageOutPath)
media.res2Video(sim_result, videoOutPath)
print("Output media resources generated")

end_time = time.time()
print('Time elapsed:', round(end_time - start_time, 3), 'secs')
