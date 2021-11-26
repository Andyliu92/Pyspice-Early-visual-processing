import numpy as np


def staticInput(circuit, row, column, r_net, r_out, v_input, c, mode='square'):
    # W-E resistors
    for i in range(1, row+1, 1):
        for j in range(1, column, 1):
            circuit.R('%d_%d_%d_%d' % (i, j, i, j+1), 'net_%d_%d' %
                      (i, j), 'net_%d_%d' % (i, j+1), r_net)

    # N-S resistors
    for i in range(1, row, 1):
        for j in range(1, column+1, 1):
            circuit.R('%d_%d_%d_%d' % (i, j, i+1, j), 'net_%d_%d' %
                      (i, j), 'net_%d_%d' % (i+1, j), r_net)

    if(mode == 'hexagonal'):
        # NW-SE resistors
        for i in range(1, row, 1):
            for j in range(1, column, 1):
                circuit.R('%d_%d_%d_%d' % (i, j, i+1, j+1), 'net_%d_%d' %
                          (i, j), 'net_%d_%d' % (i+1, j+1), r_net)

    # capacitors
    for i in range(1, row+1, 1):
        for j in range(1, column+1, 1):
            circuit.C('%d_%d' % (i, j), 'net_%d_%d' % (i, j), circuit.gnd, c)

    # Output Resistor
    for i in range(1, row+1, 1):
        for j in range(1, column+1, 1):
            circuit.R('out_%d_%d' % (i, j), 'net_%d_%d' %
                      (i, j), 'vin_%d_%d' % (i, j), r_out)

    # Sensory Inputs
    for i in range(1, row+1, 1):
        for j in range(1, column+1, 1):
            circuit.V('%d_%d' % (i, j), 'vin_%d_%d' %
                      (i, j), circuit.gnd, v_input[i-1, j-1])


def setInit(simulator, c_init, row, column):
    # C init condition
    for i in range(1, row+1, 1):
        for j in range(1, column+1, 1):
            exec("simulator.initial_condition(net_%d_%d=c_init[%d, %d])" % (
                i, j, i-1, j-1))
