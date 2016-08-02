from frequency_functions import *
from NOVAOpenSignals.EMG_stats import *
from NOVAWiiBoard.COPStats import *
import copy
# import pynotify
from novainstrumentation import smooth


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
            print "No attribute available, please use add_variable"


# def sendmessage(title, message):
#    pynotify.init("Test")
#    notice = pynotify.Notification(title, message)
#    notice.show()
#    return


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
        for i in range(1, 6):
            output[i][0] = output[i][1]

    for j in range(1, original_size-1):
        if j not in not_duplicated_indexes:
            output[0][j] = output[0][j-1] + 0.01
            for i in range(1, 6):
                output[i][j] = np.interp(output[0][j], [output[0][j-1], output[0][j+1]], [output[i][j-1], output[i][j+1]])

    if original_size-1 not in not_duplicated_indexes:
        j = original_size-1
        output[0][j] = output[0][j-1] + 0.01
        for i in range(1, 6):
            output[i][j] = np.interp(output[0][j], [output[0][j-2], output[0][j-1]], [output[i][j-2], output[i][j-1]])
        
    return output


def remove_duplicates_batch(wii_segments):
    for i in range(0, len(wii_segments)):
        wii_seg = remove_duplicates(wii_segments[i].get_variable("wii_data"))
        wii_segments[i].set_variable("wii_data", wii_seg)
    return wii_segments


def smooth_intervals(data, data_var="open_signals_data", new_var="smoothed_data", window=200):
    for i in range(0, len(data)):

        EMGs = data[i].get_variable(data_var)
        emg_smooth = [EMGs[0]]
        for j in range(1, 5):
            print "segment", i + 1, ", electrode", j
            current_EMG = EMGs[j]
            emg_smooth.append(emg_smoother(current_EMG, window))
        data[i].add_variable(new_var, emg_smooth)
    return data


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
        RMS.append(RMS_EMG(EMG[start:end]))
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


def add_filtered_signal(data, order=2, frequencies=[10, 400], fs=1000, data_var="open_signals_data",
                        new_var="open_signals_data_filtered"):

    for i in range(0, len(data)):
        filtered_emg = []
        EMGs = data[i].get_variable(data_var)
        filtered_emg.append(EMGs[0])
        for j in range(1, 5):
            temp_ = filter_signal_band(EMGs[j], frequencies, order, fs=fs)
            filtered_emg.append(temp_)

        for j in range(5, len(EMGs)):
            filtered_emg.append(EMGs[j])

        data[i].add_variable(new_var, filtered_emg)

    return data


def integrate_spec_psd(data, dB=True, data_var_psd="psd_data", data_var_spec="spec_data", new_var="spec_psd_integrated"):

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

            integration = sum(np.array(psds[j][k])) / (spec[j][2][1] - spec[j][2][0])
            if integration < 0:
                integration = 0
            temp_ = [integration]
            temp__ = []

            for l in range(0, len(spec[j][3])):
                integration = sum(np.array(spec[j][k][:, l])) / (spec[j][2][1] - spec[j][2][0])

                if integration < 0:
                    integration = 0

                temp__.append(integration)

            temp_.append(temp__)
            integrated_spec.append(temp_)

        data[i].add_variable(new_var, integrated_spec)
    return data


def thresholding(vector, time_vector, thresholds):
    
    indexes = np.concatenate([np.where(vector <= thresholds[0])[0], np.where(vector >= thresholds[1])[0]])

    if indexes[-1] == len(vector)-1:
        indexes = indexes[:-2]

    return [list(np.array(vector)[indexes]), list(np.array(time_vector)[indexes])]


def a_v_def_thr():
    a_thr = []
    v_thr = []
    for i in range(0, 4):
        temp_a = []
        temp_v = []
        for j in range(0, 2):
            temp_a.append(['d', 'd'])
            temp_v.append(['d', 'd'])
        a_thr.append(temp_a)
        v_thr.append(temp_v)

    return v_thr, a_thr


def a_v_threshold(data, v_th, a_th):
    Wii = data.get_variable("wii_data")

    time_v = Wii[0][0:-1]
    time_a = Wii[0][0:-2]

    v = [Wii[6][2], Wii[6][3]]
    a = [Wii[6][4], Wii[6][5]]

    [v_means, a_means, v_stds, a_stds] = v_and_a_stats(v, a)

    temp_v_th = [v_means[0] - v_stds[0], v_means[0] + v_stds[0], v_means[1] - v_stds[1], v_means[1] + v_stds[1]]
    temp_a_th = [a_means[0] - a_stds[0], a_means[0] + a_stds[0], a_means[1] - a_stds[1], a_means[1] + a_stds[1]]

    counter = 0

    for i in range(0, 2):
        for j in range(0, 2):
            if a_th[i][j] == 'd':
                a_th[i][j] = temp_a_th[counter]
            if v_th[i][j] == 'd':
                v_th[i][j] = temp_v_th[counter]

            counter += 1

    threshold = [thresholding(v[0], time_v, v_th[0]), thresholding(v[1], time_v, v_th[1]),
                 thresholding(a[0], time_a, a_th[0]), thresholding(a[1], time_a, a_th[1])]

    Wii.append(threshold)

    return Wii


def add_threshold(data, default=True, v_th=[], a_th=[]):
    #   data_holder -> wii_data -> 7 -> [ [THvx, Thvx_time], [THvy, Thvy_time], [THax, Thax_time], [THay, Thay_time] ]
    if default:
        v_th, a_th = a_v_def_thr()

    for i in range(0, len(data)):
        data[i].set_variable('wii_data', a_v_threshold(data[i], v_th[i], a_th[i]))
    return data


def wii_smoother(wii_data, indexes):
    temp_1 = 0
    temp_2 = 0
    for i in range(0, len(wii_data)):
        wii_data[i] = smooth(np.array(wii_data[i]), indexes[temp_1])
        temp_2 += 1
        if temp_2 == 2:
            temp_1 += 1
            temp_2 = 0
    return wii_data


def maximum_range(data):
    range_ = 0
    min_ = 0
    for i in range(0, len(data)):
        range__ = np.max(data[i]) - np.min(data[i])
        if range__ >= range_:
            range_ = range__
    return range_


def get_range_var(data, var_name, indexes, subindex=()):
    output=[]
    for i in range(0, len(data)):
        datas = data[i].get_variable(var_name)
        segment = []
        for j in indexes:
            if len(subindex) != 0:
                for k in subindex:
                    segment.append(datas[k][j])
            else:
                segment.append(datas[j])
        output.append(maximum_range(segment))
    return output


def centering(data, range_, cop_data=False, smooth_data=False, scaling_factor=1.25):

    if isinstance(range_, list):
        range_ = range_[0]

    current_range = np.max(np.array(data)) - np.min(np.array(data))

    if cop_data:
        if abs(current_range - range_) / current_range > 1.15:
            return [np.mean(np.array(data)) - range_/2.0*scaling_factor,
                    np.mean(np.array(data)) + range_/2.0*scaling_factor]
        else:
            return [np.min(np.array(data))*scaling_factor, np.min(np.array(data)) + range_*scaling_factor]
    elif smooth_data:
        return [0, range_*scaling_factor]
    else:
        return [-(range_/2.0)*scaling_factor, (range_/2.0)*scaling_factor]


def multiple_vals(data, range_, cop_data=False, smooth_data=False):
    output = []
    for i in data:
        output.append(centering(i, range_=range_, cop_data=cop_data, smooth_data=smooth_data))
    return output


def normalization(data, y_lims, new_limit=(0, 1)):
    output = copy.deepcopy(data)
    for i in range(0, len(data)):
        y_lim = y_lims[i]
        temp_ = (((np.array(data[i]) - y_lim[0]) * (new_limit[1] - new_limit[0])) / (y_lim[1] - y_lim[0])) + y_lim[0]
        output[i] = temp_ - min(temp_)
    return output

########






