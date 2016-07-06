import numpy as np


def reformat_time(time_vector, delay):

    return time_vector-delay


def center_segmentation(time_array, y_arrays, center_time, window=150):

    event_time_index = np.where(np.array(time_array) > center_time)[0][0]

    output = [np.array(time_array)[event_time_index-window:event_time_index+window]]

    for i in range(0, len(y_arrays)):
        output.append(np.array(y_arrays[i])[event_time_index - window:event_time_index + window])

    return output, range(event_time_index-window, event_time_index+window)


def read_config(file_path):
    data = open(file_path + '/config.txt')
    lines = data.readlines()

    peak_delta = int(lines[0].split('; ')[1])
    test_1 = [int(lines[2].split('; ')[1]), int(lines[2].split('; ')[2])]
    test_2 = [int(lines[3].split('; ')[1]), int(lines[3].split('; ')[2])]
    test_3 = [int(lines[4].split('; ')[1]), int(lines[4].split('; ')[2])]
    test_4 = [int(lines[5].split('; ')[1]), int(lines[5].split('; ')[2])]

    return peak_delta, [test_1, test_2, test_3, test_4]


def window_segmentation(time_arrays, intervals):
    wii_time = time_arrays[0]
    open_time = time_arrays[1]
    wii_range = []
    open_range = []
    for i in range(0, len(intervals)):
        wii_range.append(range(np.where(np.array(wii_time) > intervals[i][0])[0][0], np.where(np.array(wii_time) > intervals[i][1])[0][0]))
        open_range.append(range(np.where(np.array(open_time) > intervals[i][0])[0][0], np.where(np.array(open_time) > intervals[i][1])[0][0]))
    return wii_range, open_range


def segmentator_interval(indexes, wii_arrays, opensignal_arrays, labels):

    # test_1 -> wii     -> time (test_1[0][0])
    #                   -> tl   (test_1[0][1])
    #                   -> tr   (test_1[0][2])
    #                   -> bl   (test_1[0][3])
    #                   -> br   (test_1[0][4])
    #                   -> tw   (test_1[0][5])
    #
    #        -> open    -> time (test_1[1][0])
    #                   -> EMG  (test_1[1][1], test_1[1][2], test_1[1][3], , test_1[1][4])
    #                   -> ACC  (test_1[1][5], test_1[1][6], test_1[1][7])
    #                   -> ECG  (test_1[1][8])
    #
    #        -> labels  -> Wii  (test_1[2][0])
    #                   -> Open (test_1[2][1])

    temp = []
    for i in range(0, 4):
        temp_ = []
        wii_index = indexes[0][i]
        open_index = indexes[1][i]
        temp__ = []
        for j in range(0, len(wii_arrays)):
            temp__.append(list(np.array(wii_arrays[j])[wii_index]))
        temp_.append(temp__)
        temp__ = []
        for j in range(0, len(opensignal_arrays)):
            temp__.append(list(np.array(opensignal_arrays[j])[open_index]))
        temp_.append(temp__)
        temp_.append(labels)
        temp.append(temp_)

    return [temp[0], temp[1], temp[2], temp[3]]






