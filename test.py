
from PySpice.Unit import *
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
import PySpice
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math


logger = Logging.setup_logging()

if sys.platform == "linux" or sys.platform == "lunix2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'
elif sys.platform == "win32":
    pass

TESTING = False

# Functions
# 18 min of the lec 2 on youtube


def format_output(analysis):
    sim_res_dict = {}  # Create a dict

    for node in analysis.nodes.values():
        data_label = "%s" % str(node)
        sim_res_dict[data_label] = np.array(node)

    return sim_res_dict


def heatmap(res_arr,  filepath='', mapname='', sequence=0, amount=1, data_max=-314, data_min=-314, start_point=1):
    if data_min == -314:
        data_min = res_arr.min()
        if sequence == 0:
            print('Min: ', data_min)

    if data_max == -314:
        data_max = res_arr.max()
        if sequence == 0:
            print('Max: ', data_max)

    seq_bit = int(math.log10(amount-start_point+1))+1
    plt.figure(figsize=(10, 10))

    heatmap = sns.heatmap(res_arr, annot=True, fmt='0.5f', linewidths=.5, vmin=data_min, vmax=data_max, annot_kws={
                          'size': 8, 'weight': 'normal'})
    # a = mapname + '%.*d' % (seq_bit, sequence)
    heatmap.set_title(mapname + '%.*d' % (seq_bit, sequence+2-start_point))

    res_fig = heatmap.get_figure()
    a = filepath + mapname + '%.*d' % (seq_bit, sequence+1) + '.jpg'
    res_fig.savefig(filepath + mapname + '%.*d' %
                    (seq_bit, sequence+2-start_point) + '.jpg')
    plt.close()


def getArray(analysis_dict, nodetype, row, column, sequence=0):
    res_arr = np.empty([row, column], dtype=float)
    for i in range(0, row, 1):
        for j in range(0, column, 1):
            nodename = nodetype + '_%d_%d' % (i+1, j+1)
            res_arr[i][j] = analysis_dict[nodename][sequence]

    del sequence
    return res_arr


# Create a Circuit
circuit = Circuit('voltage divider')

# Create a Simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# add components to the circuit
row = 1
column = 1
r_net = 1.0@u_kOhm
r_out = 5@u_kOhm
v_ambient = 0@u_V
c = 400@u_uF
c_init = 0@u_V


'''
# Quiescent Operating Point
analysis = simulator.operating_point()

out_dict = format_output(analysis)

print(out_dict)

map_arr_vin = getArray(out_dict, 'vin', row, column, 0)
map_arr_net = getArray(out_dict, 'net', row, column, 0)
map_arr_res = map_arr_net - map_arr_vin


print('Arr_net')
print(map_arr_net)
print('Arr_vin')
print(map_arr_vin)
print('Arr_res')
print(map_arr_res)

heatmap(map_arr_res, filepath='./bin/quiescent/',
        mapname='res_quiescent_', data_min=0, sequence=1)
'''
'''
circuit.SinusoidalVoltageSource(
    'sin_signal', 'different_in', circuit.gnd, amplitude=10@u_V, frequency=1)
'''

# Pulse signal response
circuit.PulseVoltageSource('Pulse_sig', 'net_1_1', circuit.gnd, initial_value=0 @
                           u_V, pulsed_value=10@u_V, pulse_width=10@u_ms, period=1@u_s, delay_time=0@u_s, rise_time=0)


# Transient analysis
steptime = 2@u_ms
finaltime = 100@u_ms
analysis = simulator.transient(
    step_time=steptime, end_time=finaltime, use_initial_condition=True)

out_dict = format_output(analysis)

print(out_dict)
# print(len(out_dict['net_1_1']))

node = np.array(analysis.nodes['net_1_1'])
print(node)
print(len(node))
print("The Simulator : \n \n ", simulator)
print(analysis)

'''max_data = -1000000000
min_data = 1000000000
start_point = 1
for i in range(start_point-1, int(finaltime/steptime), 1):
    map_arr_vin = getArray(out_dict, 'vin', row, column, i)
    map_arr_net = getArray(out_dict, 'net', row, column, i)
    map_arr_res = map_arr_vin - map_arr_net
    this_max = map_arr_net.max()
    this_min = map_arr_net.min()

    if this_max > max_data:
        max_data = this_max
    if this_min < min_data:
        min_data = this_min


for i in range(start_point-1, int(finaltime/steptime), 1):
    map_arr_vin = getArray(out_dict, 'vin', row, column, i)
    map_arr_net = getArray(out_dict, 'net', row, column, i)
    map_arr_res = map_arr_vin - map_arr_net

    heatmap(map_arr_net, filepath='./bin/transcent/', mapname='net_trans_',
            sequence=i, amount=finaltime/steptime, start_point=start_point, data_max=max_data, data_min=min_data)

    print('finished fig', i+2-start_point, ' / ',
          int(finaltime/steptime)-start_point+1)
'''
'''
for i in range(start_point-1, int(finaltime/steptime), 1):
    map_arr_vin = getArray(out_dict, 'vin', row, column, i)
    # map_arr_net = getArray(out_dict, 'net', row, column, i)
    # map_arr_res = map_arr_vin - map_arr_net
    this_max = map_arr_vin.max()
    this_min = map_arr_vin.min()

    if this_max > max_data:
        max_data = this_max
    if this_min < min_data:
        min_data = this_min


for i in range(start_point-1, int(finaltime/steptime), 1):
    map_arr_vin = getArray(out_dict, 'vin', row, column, i)
    # map_arr_net = getArray(out_dict, 'net', row, column, i)
    # map_arr_res = map_arr_vin - map_arr_net

    heatmap(map_arr_vin, filepath='./bin/transcent/', mapname='vin_trans_',
            sequence=i, amount=finaltime/steptime, start_point=start_point, data_max=max_data, data_min=min_data)

    print('finished fig', i+2-start_point, ' / ',
          int(finaltime/steptime)-start_point+1)
'''

'''
# Print the Circuits:
print("The circuit/Netlist : \n \n", circuit)
'''
'''
# Print the circuit and simulator settings



# Run Analysis


print(analysis)


# Extract data from node
print(analysis.nodes['in'])
print(str(analysis.nodes['in']))
print(float(analysis.nodes['in']))
print(str(analysis.nodes['out']))
print(float(analysis.nodes['out']))
'''
exit()
