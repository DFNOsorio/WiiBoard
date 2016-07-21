from frequency_functions import *
from NOVAOpenSignals.EMG_stats import *
import copy


class data_holder:
    def __init__(self, wii_data, open_signal_data, labels):
        self.__dict__["data"] = ["wii_data", "open_signals_data", "labels"]
        self.__dict__["wii_data"] = wii_data
        self.__dict__["open_signals_data"] = open_signal_data
        self.__dict__["labels"] = labels

    def add_variable(self, var_name, data):
        self.__dict__[var_name] = data
        self.__dict__["data"].append(var_name)

    def get_variable(self, vari_name):
        if vari_name in self.__dict__["data"]:
            return copy.deepcopy(self.__dict__[vari_name])
        else:
            print "No attribute available"
            print "Choose one of the following: ", self.__dict__["data"]

    def set_variable(self, vari_name, data):
        if vari_name in self.__dict__["data"]:
            self.__dict__[vari_name] = data
        else:
            print "No attribute available"
            print "Choose one of the following: ", self.__dict__["data"]


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

    temp = [[] for _ in range(0, number_of_segments)]

    for i in range(0, number_of_segments):

        wii_index = indexes[0][i]
        open_index = indexes[1][i]

        wii_data = [[] for _ in range(0, len(wii_arrays))]
        for j in range(0, len(wii_arrays)):
            wii_data[j] = list(np.array(wii_arrays[j])[wii_index])

        open_data = [[] for _ in range(0, len(opensignal_arrays))]
        for j in range(0, len(opensignal_arrays)):
            open_data[j] = list(np.array(opensignal_arrays[j])[open_index])

        temp[i] = data_holder(wii_data, open_data, labels)

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
    for i in range(0, len(wii_segments)):
        wii_seg = remove_duplicates(wii_segments[i].get_variable("wii_data"))
        wii_segments[i].set_variable("wii_data", wii_seg)
    return wii_segments


# def smooth_intervals(data, window=20):
#     output = data
#     for i in range(0, len(data)):
#         for j in range(0, len(data[i])-1):
#             for k in range(1, len(data[i][j])):
#                 if k != 8:
#                     output[i][j][k] = list(smooth(np.array(data[i][j][k]), window_len=window))
#     return [output[0], output[1], output[2], output[3]]


def zero_out_EMG(data, zero_out_array):

    for i in range(0, len(data)):
        EMGs = data[i].get_variable("open_signals_data")
        EMGs[1] = list(np.array(EMGs[1])-zero_out_array[0])
        EMGs[2] = list(np.array(EMGs[2])-zero_out_array[1])
        EMGs[3] = list(np.array(EMGs[3])-zero_out_array[2])
        EMGs[4] = list(np.array(EMGs[4])-zero_out_array[3])

        data[i].set_variable("open_signals_data", EMGs)

    return data


def add_COPs(data, COPs):

    # test_1 -> wii     -> time (test_1[0][0])
    #                   -> tl   (test_1[0][1])
    #                   -> tr   (test_1[0][2])
    #                   -> bl   (test_1[0][3])
    #                   -> br   (test_1[0][4])
    #                   -> tw   (test_1[0][5])
    #                   -> COPs (test_1[0][6])

    for i in range(0, len(data)):
        wii = data[i].get_variable("wii_data")
        wii.append(COPs[i])
        data[i].set_variable("wii_data", wii)

    return data


def add_spec(data, fs=1000, window_size=1000, data_var="open_signals_data", new_var="spec_data"):
    # test_1  -> psd    -> [Pxx, Pxx_dB, freqs, bins, maxmin Pxx, maxmin Pxxdb] -> EMG1 (test_1[3][0])
    #                   -> [Pxx, Pxx_dB, freqs, bins] -> EMG2 (test_1[3][1])
    #                   -> [Pxx, Pxx_dB, freqs, bins] -> EMG2 (test_1[3][2])
    #                   -> [Pxx, Pxx_dB, freqs, bins] -> EMG2 (test_1[3][3])

    for i in range(0, len(data)):
        spec = []
        EMGs = data[i].get_variable(data_var)

        for j in range(1, 5):
            temp_ = get_spectrogram_no_plot(EMGs[j], fs=fs, window_size=window_size)
            spec.append(temp_)

        data[i].add_variable(new_var, spec)

    return data


def add_psd(data, fs=1000, data_var="open_signals_data", new_var="psd_data"):
    # test_1  -> psd    -> [Pxx, Pxx_dB, freqs] -> EMG1 (test_1[4][0])
    #                   -> [Pxx, Pxx_dB, freqs] -> EMG2 (test_1[4][1])
    #                   -> [Pxx, Pxx_dB, freqs] -> EMG2 (test_1[4][2])
    #                   -> [Pxx, Pxx_dB, freqs] -> EMG2 (test_1[4][3])

    for i in range(0, len(data)):
        psd = []
        EMGs = data[i].get_variable(data_var)

        for j in range(1, 5):
            temp_ = get_psd(EMGs[j], fs=fs)
            psd.append(temp_)

        data[i].add_variable(new_var, psd)

    return data


def add_EMG_RMS(data, window_size=1000, data_var="open_signals_data", new_var="emg_rms_data"):

    for i in range(0, len(data)):
        emg_rms = []
        EMGs = data[i].get_variable(data_var)
        for j in range(1, 5):
            print "segment", i+1, ", electrode", j
            current_EMG = EMGs[j]
            RMS = RMS_moving_window(current_EMG, window_size)
            emg_rms.append(RMS)

        data[i].add_variable(new_var, emg_rms)

    return data


def add_EMG_stat(data, window_size=1000, data_var = "open_signals_data", new_var="emg_stat_data"):
    # test_1 -> EMGStat -> [[Positiv, PT], [Negatif, NT], IEMG, MAV, EEMG, Var, RMS] -> EMG1 (test_1[5][0])
    #                   -> [[Positiv, PT], [Negatif, NT], IEMG, MAV, EEMG, Var, RMS] -> EMG2 (test_1[5][1])
    #                   -> [[Positiv, PT], [Negatif, NT], IEMG, MAV, EEMG, Var, RMS] -> EMG2 (test_1[5][2])
    #                   -> [[Positiv, PT], [Negatif, NT], IEEMG, Var, RMS] -> EMG2 (test_1[5][3])

    for i in range(0, len(data)):
        emg_rms = []
        EMGs = data[i].get_variable(data_var)
        current_time = EMGs[0]
        for j in range(1, 5):

            print "segment", i + 1, ", electrode", j
            current_EMG = EMGs[j]
            positive_indexes = np.where(np.array(current_EMG) > 0)[0]
            emg_rms.append([list(np.array(current_EMG)[positive_indexes]), list(np.array(current_time)[positive_indexes])])
            negative_indexes = np.where(np.array(current_EMG) < 0)[0]
            emg_rms.append([list(np.array(current_EMG)[negative_indexes]), list(np.array(current_time)[negative_indexes])])
            [IEMG, MAV, EEMG, Var, RMS] = moving_window(current_EMG, window_size)

            emg_rms.append(IEMG)
            emg_rms.append(MAV)
            emg_rms.append(EEMG)
            emg_rms.append(Var)
            emg_rms.append(RMS)

        data[i].add_variable(new_var, emg_rms)

    return data


def RMS_moving_window(EMG, window_size):
    starting_index = window_size / 2
    ending_index = len(EMG) - starting_index
    RMS = []
    for i in range(0, starting_index):
        start = 0
        end = starting_index + i
        RMS.append(RMS_EMG(EMG[start:end]))

    for i in range(starting_index, ending_index):
        start = i - starting_index
        end = i + starting_index
        RMS.append(RMS_EMG (EMG[start:end]))
    for i in range(ending_index, len (EMG)):
        start = i - starting_index
        end = len(EMG) - 1
        RMS.append(RMS_EMG(EMG[start:end]))

    return RMS


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


def add_filtered_signal(data, frequencies=[10, 400], fs=1000, data_var="open_signals_data", new_var="filter_EMG_data"):

    for i in range(0, len(data)):
        filtered_emg = []
        EMGs = data[i].get_variable(data_var)
        filtered_emg.append(EMGs[0])
        for j in range(1, 5):
            temp_ = filter_signal_band(EMGs[j], frequencies, fs=fs)
            filtered_emg.append(temp_)

        data[i].add_variable(new_var, filtered_emg)

    return data


def integrate_spec_psd(data, dB=True, data_var_psd="psd_data", data_var_spec="spec_data", new_var="integrated_spec_psd"):

    # For each data_holder (data[i]), the variable integrated_spec has the following format
    #   data_holder -> integrated_spec -> FR -> [ PSD_integral, [Spec_Integrals] ]
    #                                     FL
    #                                     BL
    #                                     BR

    k = 0
    if dB:
        k = 1

    for i in range(0, len(data)):
        integrated_spec = []
        psds = data[i].get_variable(data_var_psd)
        spec = data[i].get_variable(data_var_spec)

        for j in range(0, 4):
            temp_ = [sum(np.array(psds[j][k])) / (spec[j][2][1] - spec[j][2][0])]
            temp__ = []

            for l in range(0, len(spec[j][3])):
                temp__.append(sum(np.array(spec[j][k][:, 1])) / (spec[j][2][1] - spec[j][2][0]))

            temp_.append(temp__)
            integrated_spec.append(temp_)

        data[i].add_variable(new_var, integrated_spec)
    return data

########






