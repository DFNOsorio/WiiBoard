from DataProcessor.NOVAOpenSignals import load_open_trial
from DataProcessor.NOVAWiiBoard import load_wii_trial
from DataProcessor.processing_methods import read_config, reformat_time, center_segmentation, window_segmentation,\
    segmentator_interval
from DataProcessor.printing.printing_lib import subplot_overlap
import numpy as np


def sync_files(folder_name, patient, plot=False, high=False):
    et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
    EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

    peak_delta, windows = read_config(folder_name+patient+'/config')

    new_wii_time = reformat_time(np.array(rt), epoch - t0)
    new_event_time = et - (epoch - t0)

    wii_window, indexes_ = center_segmentation(new_wii_time, [np.array(data[4]) * 55000], new_event_time)

    adjusted_time = new_event_time - open_time[peak_delta]

    new_wii_time_ = reformat_time(np.array(new_wii_time), adjusted_time)
    new_event_time_ = new_event_time - adjusted_time
    window = 150
    if high:
        window = 1500
    open_signals_window, indexes = center_segmentation(open_time, [ACC[0], ACC[1], ACC[2]], new_event_time, window=window)
    wii_window_, indexes__ = center_segmentation(new_wii_time_, [np.array(data[4]) * 55000], new_event_time_)

    if plot:
        figure, axes = subplot_overlap([[open_time, open_time, open_time, new_wii_time_],
                                         [open_signals_window[0], open_signals_window[0], open_signals_window[0], wii_window[0],
                                          wii_window_[0]]],
                                        [[ACC[0], ACC[1], ACC[2], np.array (data[4]) * 55000],
                                         [open_signals_window[1], open_signals_window[2], open_signals_window[3], wii_window[1],
                                          wii_window_[1]]],
                                        ["Acc + Events", "Acc + Events"], ["Time (s)", "Time (s)"], ["Raw data", "Raw data"], 1,
                                        2,
                                        legend=[np.concatenate([ACC_l, ["Events"]]),
                                                np.concatenate([ACC_l, ["Events", "Events A"]])], overlapx=True)

    return [new_wii_time_, open_time, windows, data, EMG, ACC, ECG, EMG_l, ACC_l, ECG_l]


def sync_files_multiple(folder_name, patient, file_terminations, segment_info, number_of_files=2, plot=False, high=False):
    output = []
    for i in range(0, number_of_files):
        et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII'+file_terminations[i], patient, False)
        EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test'+file_terminations[i])
        peak_delta, windows = read_config(folder_name+patient+'/config'+file_terminations[i])
        windows = list(np.array(windows)[segment_info[i]])

        new_wii_time = reformat_time(np.array(rt), epoch - t0)
        new_event_time = et - (epoch - t0)

        wii_window, indexes_ = center_segmentation(new_wii_time, [np.array(data[4]) * 55000], new_event_time)

        adjusted_time = new_event_time - open_time[peak_delta]

        new_wii_time_ = reformat_time(np.array(new_wii_time), adjusted_time)
        new_event_time_ = new_event_time - adjusted_time
        window = 150
        if high:
            window = 1500
        open_signals_window, indexes = center_segmentation(open_time, [ACC[0], ACC[1], ACC[2]], new_event_time, window=window)
        wii_window_, indexes__ = center_segmentation(new_wii_time_, [np.array(data[4]) * 55000], new_event_time_)

        if plot:
            figure, axes = subplot_overlap ([[open_time, open_time, open_time, new_wii_time_],
                                             [open_signals_window[0], open_signals_window[0], open_signals_window[0], wii_window[0],
                                              wii_window_[0]]],
                                            [[ACC[0], ACC[1], ACC[2], np.array(data[4]) * 55000],
                                             [open_signals_window[1], open_signals_window[2], open_signals_window[3], wii_window[1],
                                              wii_window_[1]]],
                                            ["Acc + Events", "Acc + Events"], ["Time (s)", "Time (s)"], ["Raw data", "Raw data"], 1,
                                            2,
                                            legend=[np.concatenate ([ACC_l, ["Events"]]),
                                                    np.concatenate ([ACC_l, ["Events", "Events A"]])], overlapx=True)
        output.append([new_wii_time_, open_time, windows, data, EMG, ACC, ECG, EMG_l, ACC_l, ECG_l])
    return output


def segmentation_arrays(wii_time, data, open_time, EMG, ACC, ECG, EMG_l, ACC_l, ECG_l):

    wii_array = [wii_time, data[0], data[1], data[2], data[3], data[5]]

    opensignal_array = [open_time, EMG[0], EMG[1], EMG[2], EMG[3], ACC[0], ACC[1], ACC[2], ECG[0]]

    lbs = [["STL", "STR", "SBL", "SBR", "TW"],
           [EMG_l[0], EMG_l[1], EMG_l[2], EMG_l[3], ACC_l[0], ACC_l[1], ACC_l[2], ECG_l[0]]]

    return wii_array, opensignal_array, lbs


def segmented_signal(input, input_index=0, number_of_segments=4):
    [wii_time, open_time, windows, data, EMG, ACC, ECG, EMG_l, ACC_l, ECG_l] = input[input_index]

    wii_range, open_range = window_segmentation([wii_time, open_time], windows)

    wii_array, opensignal_array, lbs = segmentation_arrays(wii_time, data, open_time, EMG, ACC, ECG, EMG_l, ACC_l,
                                                            ECG_l)

    output = segmentator_interval([wii_range, open_range], wii_array, opensignal_array, lbs, number_of_segments)

    return output