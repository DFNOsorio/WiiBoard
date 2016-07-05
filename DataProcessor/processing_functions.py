import numpy as np


def reformat_time(time_vector, delay):

    return time_vector-delay


def window_segmentation(time_array, y_arrays, center_time, window=150):

    event_time_index = np.where(np.array(time_array) > center_time)[0][0]

    output = [np.array(time_array)[event_time_index-window:event_time_index+window]]

    for i in range(0, len(y_arrays)):
        output.append(np.array(y_arrays[i])[event_time_index - window:event_time_index + window])

    return output, range(event_time_index-window, event_time_index+window)


def read_config(file_path):
    data = open(file_path + '/config.txt')
    lines = data.readlines()

    return int(lines[0].split('; ')[1])
