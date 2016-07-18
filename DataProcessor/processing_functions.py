import numpy as np
from novainstrumentation import *
from frequency_functions import *
from NOVAOpenSignals.EMG_stats import *


def reformat_time(time_vector, delay):

    return time_vector-delay


def center_segmentation(time_array, y_arrays, center_time, window=150):

    event_time_index = np.where(np.array(time_array) > center_time)[0][0]

    output = [np.array(time_array)[event_time_index-window:event_time_index+window]]

    for i in range(0, len(y_arrays)):
        output.append(np.array(y_arrays[i])[event_time_index - window:event_time_index + window])

    return output, range(event_time_index-window, event_time_index+window)


def read_config(file_path):
    data = open(file_path + '.txt')
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


def segmentator_interval(indexes, wii_arrays, opensignal_arrays, labels, number_of_segments=4):

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
    for i in range(0, number_of_segments):
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

    return temp


def remove_duplicates(wii_segment):
    output = wii_segment
    original_size = len(wii_segment[0])
    not_duplicated_indexes = np.where(np.diff(np.array(wii_segment[0])) != 0)[0]

    if not_duplicated_indexes[0] != 0:
        output[0][0] = output[0][1] - 0.01
        output[1][0] = output[1][1]
        output[2][0] = output[2][1]
        output[3][0] = output[3][1]
        output[4][0] = output[4][1]
        output[5][0] = output[5][1]

    for j in range(1, original_size-1):
        if j not in not_duplicated_indexes:
            output[0][j] = output[0][j-1] + 0.01
            output[1][j] = np.interp(output[0][j], [output[0][j-1], output[0][j+1]], [output[1][j-1], output[1][j+1]])
            output[2][j] = np.interp(output[0][j], [output[0][j-1], output[0][j+1]], [output[2][j-1], output[2][j+1]])
            output[3][j] = np.interp(output[0][j], [output[0][j-1], output[0][j+1]], [output[3][j-1], output[3][j+1]])
            output[4][j] = np.interp(output[0][j], [output[0][j-1], output[0][j+1]], [output[4][j-1], output[4][j+1]])
            output[5][j] = np.interp(output[0][j], [output[0][j-1], output[0][j+1]], [output[5][j-1], output[5][j+1]])

    if original_size-1 not in not_duplicated_indexes:
        j = original_size-1
        output[0][j] = output[0][j-1] + 0.01
        output[1][j] = np.interp(output[0][j], [output[0][j-2], output[0][j-1]], [output[1][j-2], output[1][j-1]])
        output[2][j] = np.interp(output[0][j], [output[0][j-2], output[0][j-1]], [output[2][j-2], output[2][j-1]])
        output[3][j] = np.interp(output[0][j], [output[0][j-2], output[0][j-1]], [output[3][j-2], output[3][j-1]])
        output[4][j] = np.interp(output[0][j], [output[0][j-2], output[0][j-1]], [output[4][j-2], output[4][j-1]])
        output[5][j] = np.interp(output[0][j], [output[0][j-2], output[0][j-1]], [output[5][j-2], output[5][j-1]])

    return output


def remove_duplicates_batch(wii_segments):
    output = []
    for i in wii_segments:
        output.append(remove_duplicates(i))
    return [output[0], output[1], output[2], output[3]]


def smooth_intervals(data, window=20):
    output = data
    for i in range(0, len(data)):
        for j in range(0, len(data[i])-1):
            for k in range(1, len(data[i][j])):
                if k != 8:
                    output[i][j][k] = list(smooth(np.array(data[i][j][k]), window_len=window))
    return [output[0], output[1], output[2], output[3]]


def zero_out_EMG(data, zero_out_array):
    output = data
    for i in range(0, len(data)):
        output[i][1][1] = list(np.array(data[i][1][1])-zero_out_array[0])
        output[i][1][2] = list(np.array(data[i][1][2])-zero_out_array[1])
        output[i][1][3] = list(np.array(data[i][1][3])-zero_out_array[2])
        output[i][1][4] = list(np.array(data[i][1][4])-zero_out_array[3])
    return output


def add_COPs(data, COPs):

    # test_1 -> wii     -> time (test_1[0][0])
    #                   -> tl   (test_1[0][1])
    #                   -> tr   (test_1[0][2])
    #                   -> bl   (test_1[0][3])
    #                   -> br   (test_1[0][4])
    #                   -> tw   (test_1[0][5])
    #                   -> COPs (test_1[0][6])
    output = data
    for i in range(0, len(data)):
        output[i][0].append(COPs[i])
    return output



def add_spec(data, fs=1000, window_size=1000):
    # test_1  -> psd    -> [Pxx, Pxx_dB, freqs, bins] -> EMG1 (test_1[3][0])
    #                   -> [Pxx, Pxx_dB, freqs, bins] -> EMG2 (test_1[3][1])
    #                   -> [Pxx, Pxx_dB, freqs, bins] -> EMG2 (test_1[3][2])
    #                   -> [Pxx, Pxx_dB, freqs, bins] -> EMG2 (test_1[3][3])

    output = data

    for i in range(0, len(data)):
        temp = []
        for j in range(1, 5):
            temp_ = get_spectrogram_no_plot(data[i][1][j], fs=fs, window_size=window_size)
            temp.append(temp_)
        output[i].append(temp)
    return output


def add_psd(data, fs=1000):
    # test_1  -> psd    -> [Pxx, Pxx_dB, freqs] -> EMG1 (test_1[4][0])
    #                   -> [Pxx, Pxx_dB, freqs] -> EMG2 (test_1[4][1])
    #                   -> [Pxx, Pxx_dB, freqs] -> EMG2 (test_1[4][2])
    #                   -> [Pxx, Pxx_dB, freqs] -> EMG2 (test_1[4][3])

    output = data

    for i in range(0, len(data)):
        temp = []
        for j in range(1, 5):
            temp_ = get_psd(data[i][1][j], fs=fs)
            temp.append(temp_)
        output[i].append(temp)
    return output


def add_EMG_stat(data, window_size=1000):
    # test_1 -> EMGStat -> [[Positiv, PT], [Negatif, NT], IEMG, MAV, EEMG, Var, RMS] -> EMG1 (test_1[5][0])
    #                   -> [[Positiv, PT], [Negatif, NT], IEMG, MAV, EEMG, Var, RMS] -> EMG2 (test_1[5][1])
    #                   -> [[Positiv, PT], [Negatif, NT], IEMG, MAV, EEMG, Var, RMS] -> EMG2 (test_1[5][2])
    #                   -> [[Positiv, PT], [Negatif, NT], IEEMG, Var, RMS] -> EMG2 (test_1[5][3])

    output = data

    for i in range(0, len(data)):
        temp = []
        current_time = data[i][1][0]
        for j in range(1, 5):
            current_EMG = data[i][1][j]
            positive_indexes = np.where(np.array(current_EMG) > 0)[0]
            temp.append([list(np.array(current_EMG)[positive_indexes]), list(np.array(current_time)[positive_indexes])])
            negative_indexes = np.where(np.array(current_EMG) < 0)[0]
            temp.append([list(np.array(current_EMG)[negative_indexes]), list(np.array(current_time)[negative_indexes])])
            [IEMG, MAV, EEMG, Var, RMS] = moving_window(current_EMG, window_size)

            temp.append(IEMG)
            temp.append(MAV)
            temp.append(EEMG)
            temp.append(Var)
            temp.append(RMS)

        output[i].append(temp)
    return output


def moving_window(EMG, window_size):
    starting_index = window_size/2
    ending_index = len(EMG) - starting_index

    IEMG = []
    MAV = []
    EEMG = []
    Var = []
    RMS = []

    for i in range(0, starting_index):
        start = 0
        end = starting_index+i

        IEMG.append(integrated_EMG(EMG[start:end]))
        MAV.append(mean_absolute_value(EMG[start:end]))
        EEMG.append(energy_EMG(EMG[start:end]))
        Var.append(variance(EMG[start:end]))
        RMS.append(RMS_EMG(EMG[start:end]))

    for i in range(starting_index, ending_index):

        start = i - starting_index
        end = i + starting_index

        IEMG.append(integrated_EMG(EMG[start:end]))
        MAV.append(mean_absolute_value(EMG[start:end]))
        EEMG.append(energy_EMG(EMG[start:end]))
        Var.append(variance(EMG[start:end]))
        RMS.append(RMS_EMG(EMG[start:end]))


    for i in range(ending_index, len(EMG)):

        start = i - starting_index
        end = len(EMG)-1

        IEMG.append(integrated_EMG(EMG[start:end]))
        MAV.append(mean_absolute_value(EMG[start:end]))
        EEMG.append(energy_EMG(EMG[start:end]))
        Var.append(variance(EMG[start:end]))
        RMS.append(RMS_EMG(EMG[start:end]))

    return IEMG, MAV, EEMG, Var, RMS




    #IEMG
    #MAV
    #EEMG
    #Var
    #RMS








