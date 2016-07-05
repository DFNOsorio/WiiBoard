from DataProcessor import *
import time

folder_name = '../WiiBoard/Trials/'

patient = 'Paulo'

COPx_s, COPy_s, area, contour_array, et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

peak_delta = read_config(folder_name+patient)

new_wii_time = reformat_time(np.array(rt), epoch - t0)
new_event_time = et - (epoch - t0)

open_signals_window, indexes = window_segmentation(open_time, [ACC[0], ACC[1], ACC[2]], new_event_time)
wii_window, indexes_ = window_segmentation(new_wii_time, [np.array(data[4])*55000], new_event_time)

#figure, axes = subplot_overlap([[open_time, open_time, open_time, new_wii_time],
#                 [open_signals_window[0], open_signals_window[0], open_signals_window[0], wii_window[0]]],
#                [[ACC[0], ACC[1], ACC[2], np.array(data[4])*55000],
#                 [open_signals_window[1], open_signals_window[2], open_signals_window[3], wii_window[1]]],
#                ["Acc + Events", "Acc + Events"], ["Time (s)", "Time (s)"], ["Raw data", "Raw data"], 1, 2,
#                legend=[np.concatenate([ACC_l, ["Events"]]), np.concatenate([ACC_l, ["Events"]])], overlapx=True)
#add_indexes(axes[1], open_signals_window[0], open_signals_window[3], indexes)


adjusted_time = new_event_time - open_time[peak_delta]

new_wii_time_ = reformat_time(np.array(new_wii_time), adjusted_time)
new_event_time_ = new_event_time - adjusted_time

open_signals_window, indexes = window_segmentation(open_time, [ACC[0], ACC[1], ACC[2]], new_event_time)
wii_window_, indexes__ = window_segmentation(new_wii_time_, [np.array(data[4])*55000], new_event_time_)

figure, axes = subplot_overlap([[open_time, open_time, open_time, new_wii_time],
                 [open_signals_window[0], open_signals_window[0], open_signals_window[0], wii_window[0], wii_window_[0]]],
                [[ACC[0], ACC[1], ACC[2], np.array(data[4])*55000],
                 [open_signals_window[1], open_signals_window[2], open_signals_window[3], wii_window[1], wii_window_[1]]],
                ["Acc + Events", "Acc + Events"], ["Time (s)", "Time (s)"], ["Raw data", "Raw data"], 1, 2,
                legend=[np.concatenate([ACC_l, ["Events"]]), np.concatenate([ACC_l, ["Events", "Events A"]])], overlapx=True)

plot_show_all()
