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
    v_array = np.zeros(shape=(row, column), dtype=np.float64)
    for i in range(0, len(v_input)+1, 1):
        v_array[v_input[i, 0], v_input[i, 1]] = v_input[i, 2]
    for i in range(1, row+1, 1):
        for j in range(1, column+1, 1):
            circuit.V('%d_%d' % (i, j), 'vin_%d_%d' %
                      (i, j), circuit.gnd, v_array[i-1, j-1])


def setInit(simulator, c_init):
    # C init condition
    for i in range(1, row+1, 1):
        for j in range(1, column+1, 1):
            simulator.initial_condition('net_%d_%d=' % (i, j)+c_init)
