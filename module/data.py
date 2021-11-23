import numpy as np

# create and return a dictionary which has the record of "Node Name" <---> "Node value array"(np.array)


def format(analysis):
    sim_res_dict = {}  # Create a dict

    for node in analysis.nodes.values():
        data_label = "%s" % str(node)
        sim_res_dict[data_label] = np.array(node)

    return sim_res_dict


# organize node outputs in the form of frame
def getFrame(analysis_dict, nodetype, row, column, sequence=0):
    res_arr = np.empty([row, column], dtype=float)
    for i in range(0, row, 1):
        for j in range(0, column, 1):
            nodename = nodetype + '_%d_%d' % (i+1, j+1)
            res_arr[i][j] = analysis_dict[nodename][sequence]

    return res_arr


def frameAll(analysis_dict, nodetype, row, column, size):
    if nodetype == 'output':
        result = np.empty([size, row, column], dtype=np.float32)
        for i in range(0, size, 1):
