import numpy as np
import math

# create and return a dictionary which has the record of "Node Name" <---> "Node value array"(np.array)


def format(analysis):
    sim_res_dict = {}  # Create a dict

    for node in analysis.nodes.values():
        data_label = "%s" % str(node)
        sim_res_dict[data_label] = np.array(node)

    return sim_res_dict


# organize node outputs in the form of frame
# chronological organized --> spatial organized
def getFrame(analysis_dict, nodetype, row, column, sequence=0):
    res_arr = np.empty([row, column], dtype=np.float32)
    for i in range(0, row, 1):
        for j in range(0, column, 1):
            nodename = nodetype + '_%d_%d' % (i+1, j+1)
            res_arr[i][j] = analysis_dict[nodename][sequence]

    return res_arr


# package getFrame func to get all frames at once.
def frameAll(analysis_dict, nodetype, row, column, size):
    if nodetype == 'output':
        result = np.empty([size, row, column], dtype=np.float32)
        for i in range(0, size, 1):
            vin = getFrame(analysis_dict, 'vin', row, column, i)
            net = getFrame(analysis_dict, 'net', row, column, i)
            result[i] = vin-net
            # print("Got: frame %d" % i)
    else:
        result = np.empty([size, row, column], dtype=np.float32)
        for i in range(0, size, 1):
            result = getFrame(analysis_dict, nodetype, row, column, i)
            # print("Got: frame %d" % i)
    return result


def std_8b(data):
    dmax = data.max()
    dmin = data.min()
    data = data - dmin
    data = (data * 255) / (dmax-dmin)
    return data


def logProc(data):
    data = data + np.ones(data.shape)
    data = np.log(data)
    data = data * 255 / math.log(256)
    return data
