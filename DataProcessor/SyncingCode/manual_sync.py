from DataProcessor import *

folder_name = '/home/danielosorio/PycharmProjects/WiiBoard/Trials/'
patient = 'Joao1000'

et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

new_wii_time = reformat_time(np.array(rt), epoch - t0)
new_event_time = et - (epoch - t0)

adjusted_time = new_event_time - open_time[13206]

new_wii_time_ = reformat_time(np.array(new_wii_time), adjusted_time)
new_event_time_ = new_event_time - adjusted_time

wii_window, indexes_ = center_segmentation(new_wii_time, [np.array(data[4])*55000], new_event_time, window=1000)
open_signals_window, indexes = center_segmentation(open_time, [ACC[0], ACC[1], ACC[2]], new_event_time, window=6000)
wii_window_, indexes__ = center_segmentation(new_wii_time_, [np.array(data[4])*55000], new_event_time_, window=1000)

figure, axes = subplot_overlap([[open_time, open_time, open_time, new_wii_time_, new_wii_time_],
                                 [open_signals_window[0], open_signals_window[0], open_signals_window[0], wii_window[0],
                                  wii_window_[0]]],
                                [[ACC[0], ACC[1], ACC[2], np.array(data[4]) * 55000, np.array(data[5]) * 550 - 20000],
                                 [open_signals_window[1], open_signals_window[2], open_signals_window[3], wii_window[1],
                                  wii_window_[1]]],
                                ["Acc + Events", "Acc + Events"], ["Time (s)", "Time (s)"], ["Raw data", "Raw data"], 1,
                                2,
                                legend=[np.concatenate ([ACC_l, ["Events", "weight"]]),
                                        np.concatenate ([ACC_l, ["Events", "Events A"]])], overlapx=True)

plot_show_all()
figure, axes = subplot_overlap([new_wii_time_], [[data[5]]], ["f"], ["f"], ["f"], 1, 1)
plot_show_all()
