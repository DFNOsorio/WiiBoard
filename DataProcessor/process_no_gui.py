from DataProcessor import *
import time

folder_name = '../WiiBoard/Trials/'

patient = 'Catia'

## Loading  and syncing
et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

peak_delta, windows = read_config(folder_name+patient)

new_wii_time = reformat_time(np.array(rt), epoch - t0)
new_event_time = et - (epoch - t0)

wii_window, indexes_ = center_segmentation(new_wii_time, [np.array(data[4])*55000], new_event_time)

adjusted_time = new_event_time - open_time[peak_delta]

new_wii_time_ = reformat_time(np.array(new_wii_time), adjusted_time)
new_event_time_ = new_event_time - adjusted_time

open_signals_window, indexes = center_segmentation(open_time, [ACC[0], ACC[1], ACC[2]], new_event_time)
wii_window_, indexes__ = center_segmentation(new_wii_time_, [np.array(data[4])*55000], new_event_time_)


figure, axes = subplot_overlap([[open_time, open_time, open_time, new_wii_time_],
                  [open_signals_window[0], open_signals_window[0], open_signals_window[0], wii_window[0], wii_window_[0]]],
                 [[ACC[0], ACC[1], ACC[2], np.array(data[4])*55000],
                  [open_signals_window[1], open_signals_window[2], open_signals_window[3], wii_window[1], wii_window_[1]]],
                 ["Acc + Events", "Acc + Events"], ["Time (s)", "Time (s)"], ["Raw data", "Raw data"], 1, 2,
                 legend=[np.concatenate([ACC_l, ["Events"]]), np.concatenate([ACC_l, ["Events", "Events A"]])], overlapx=True)


## Data segmentation

wii_range, open_range = window_segmentation([new_wii_time_, open_time], windows)

wii_array = [new_wii_time_, data[0], data[1], data[2], data[3], data[5]]

opensignal_array = [open_time, EMG[0], EMG[1], EMG[2], EMG[3], ACC[0], ACC[1], ACC[2], ECG[0]]

lbs = [["STL", "STR", "SBL", "SBR", "TW"],
       [EMG_l[0], EMG_l[1], EMG_l[2], EMG_l[3], ACC_l[0], ACC_l[1], ACC_l[2], ECG_l[0]]]

[s1, s2, s3, s4] = segmentator_interval([wii_range, open_range], wii_array, opensignal_array, lbs)

print "Patient mean weight: " + str(np.mean(s1[0][5]))

## Processing

[cop1, cop2, cop3, cop4] = interval_COPs([s1, s2, s3, s4])

## Plots
subplot_overlap([s1[0][0], s2[0][0], s3[0][0], s4[0][0]],
                [[s1[0][1], s1[0][2], s1[0][3], s1[0][4]],
                 [s2[0][1], s2[0][2], s2[0][3], s2[0][4]],
                 [s3[0][1], s3[0][2], s3[0][3], s3[0][4]],
                 [s4[0][1], s4[0][2], s4[0][3], s4[0][4]]],
                ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                ["COPx (mm)", "COPx (mm)", "COPx (mm)", "COPx (mm)"],
                ["COPy (mm)", "COPy (mm)", "COPy (mm)", "COPy (mm)"], 2, 2,
                legend=[s1[2][0], s2[2][0], s3[2][0], s4[2][0]])

subplot_overlap([cop1[0], cop2[0], cop3[0], cop4[0]],
                [[cop1[1]], [cop2[1]], [cop3[1]], [cop4[1]]],
                ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                ["COPx (mm)", "COPx (mm)", "COPx (mm)", "COPx (mm)"],
                ["COPy (mm)", "COPy (mm)", "COPy (mm)", "COPy (mm)"], 2, 2, wii=[0, 1, 2, 3])

plot_show_all()
