from DataProcessor import *
import time

folder_name = '../WiiBoard/Trials/'

patient = 'Filipe'

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

plot = False

if plot:
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

## Processing

print "Patient mean weight: " + str(np.mean(s1[0][5]))

[cop1, cop2, cop3, cop4] = interval_COPs([s1, s2, s3, s4])

## Plots
plot = False

if plot:
    figure, axes = subplot_overlap([s1[0][0], s2[0][0], s3[0][0], s4[0][0]],
                    [[s1[0][1], s1[0][2], s1[0][3], s1[0][4]],
                     [s2[0][1], s2[0][2], s2[0][3], s2[0][4]],
                     [s3[0][1], s3[0][2], s3[0][3], s3[0][4]],
                     [s4[0][1], s4[0][2], s4[0][3], s4[0][4]]],
                    ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                    ["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
                    ["Weight (kg)", "Weight (kg)", "Weight (kg)", "Weight (kg)"], 2, 2,
                    legend=[s1[2][0], s2[2][0], s3[2][0], s4[2][0]])

    add_sup_title(figure, "Wii sensor data")

    figure, axes = subplot_overlap([cop1[0], cop2[0], cop3[0], cop4[0]],
                    [[cop1[1]], [cop2[1]], [cop3[1]], [cop4[1]]],
                    ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                    ["COPx (mm)", "COPx (mm)", "COPx (mm)", "COPx (mm)"],
                    ["COPy (mm)", "COPy (mm)", "COPy (mm)", "COPy (mm)"], 2, 2, wii=[0, 1, 2, 3])

    add_sup_title(figure, "COP")

    figure, axes = subplot_overlap([s1[1][0], s2[1][0], s3[1][0], s4[1][0]],
                    [[s1[1][1], s1[1][2], s1[1][3], s1[1][4]],
                     [s2[1][1], s2[1][2], s2[1][3], s2[1][4]],
                     [s3[1][1], s3[1][2], s3[1][3], s3[1][4]],
                     [s4[1][1], s4[1][2], s4[1][3], s4[1][4]]],
                    ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                    ["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
                    ["Raw", "Raw", "Raw", "Raw"], 2, 2,
                    legend=[s1[2][1], s2[2][1], s3[2][1], s4[2][1]])

    add_sup_title(figure, "EMG data")

    figure, axes = subplot_overlap([s1[1][0], s2[1][0], s3[1][0], s4[1][0]],
                    [[s1[1][5], s1[1][6], s1[1][7]],
                     [s2[1][5], s2[1][6], s2[1][7]],
                     [s3[1][5], s3[1][6], s3[1][7]],
                     [s4[1][5], s4[1][6], s4[1][7]]],
                    ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                    ["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
                    ["Raw", "Raw", "Raw", "Raw"], 2, 2,
                    legend=[s1[2][1][4:7], s2[2][1][4:7], s3[2][1][4:7], s4[2][1][4:7]])

    add_sup_title(figure, "Accelerometer data")

    figure, axes = subplot_overlap([s1[1][0], s2[1][0], s3[1][0], s4[1][0]],
                    [[s1[1][8]], [s2[1][8]], [s3[1][8]], [s4[1][8]]],
                    ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open", "1 Feet - Eyes Closed"],
                    ["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
                    ["Raw", "Raw", "Raw", "Raw"], 2, 2,
                    legend=[[s1[2][1][-1]], [s2[2][1][-1]], [s3[2][1][-1]], [s4[2][1][-1]]])

    add_sup_title(figure, "ECG data")

## Removing duplicates

[s1[0], s2[0], s3[0], s4[0]] = remove_duplicates_batch([s1[0], s2[0], s3[0], s4[0]])

[cop1, cop2, cop3, cop4] = interval_COPs([s1, s2, s3, s4])

plot = False
if plot:

    figure, axes = subplot_overlap([s1[0][0], s2[0][0], s3[0][0], s4[0][0]],
                                   [[s1[0][1], s1[0][2], s1[0][3], s1[0][4]],
                                    [s2[0][1], s2[0][2], s2[0][3], s2[0][4]],
                                    [s3[0][1], s3[0][2], s3[0][3], s3[0][4]],
                                    [s4[0][1], s4[0][2], s4[0][3], s4[0][4]]],
                                   ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open",
                                    "1 Feet - Eyes Closed"],
                                   ["Time (s)", "Time (s)", "Time (s)", "Time (s)"],
                                   ["Weight (kg)", "Weight (kg)", "Weight (kg)", "Weight (kg)"], 2, 2,
                                   legend=[s1[2][0], s2[2][0], s3[2][0], s4[2][0]])

    add_sup_title(figure, "Wii sensor data - Clean")

    figure, axes = subplot_overlap([cop1[0], cop2[0], cop3[0], cop4[0]],
                                   [[cop1[1]], [cop2[1]], [cop3[1]], [cop4[1]]],
                                   ["2 Feet - Eyes Open", "2 Feet - Eyes Closed", "1 Feet - Eyes Open",
                                    "1 Feet - Eyes Closed"],
                                   ["COPx (mm)", "COPx (mm)", "COPx (mm)", "COPx (mm)"],
                                   ["COPy (mm)", "COPy (mm)", "COPy (mm)", "COPy (mm)"], 2, 2, wii=[0, 1, 2, 3])

    add_sup_title(figure, "COP - Clean")

    figure, axes = subplot_overlap([s1[0][0], s2[0][0], s3[0][0], s4[0][0],
                                    s1[0][0], s2[0][0], s3[0][0], s4[0][0],
                                    s1[0][0][0:-1], s2[0][0][0:-1], s3[0][0][0:-1], s4[0][0][0:-1],
                                    s1[0][0][0:-2], s2[0][0][0:-2], s3[0][0][0:-2], s4[0][0][0:-2]],
                                   [[cop1[0]], [cop2[0]], [cop3[0]], [cop4[0]],
                                    [cop1[1]], [cop2[1]], [cop3[1]], [cop4[1]],
                                    [cop1[2], cop1[3]], [cop2[2], cop2[3]],
                                    [cop3[2], cop3[3]], [cop4[2], cop4[3]],
                                    [cop1[4], cop1[5]], [cop2[4], cop2[5]],
                                    [cop3[4], cop3[5]], [cop4[4], cop4[5]]
                                    ],
                                   ["2 Feet - Eyes Open COPx", "2 Feet - Eyes Closed COPx",
                                    "1 Feet - Eyes Open COPx", "1 Feet - Eyes Closed COPx",
                                    "COPy", "COPy", "COPy", "COPy", "Velocity", "Velocity", "Velocity", "Velocity",
                                    "Acceleration", "Acceleration", "Acceleration", "Acceleration"],
                                   ["Time (s)", "Time (s)", "Time (s)", "Time (s)",
                                    "Time (s)", "Time (s)", "Time (s)", "Time (s)",
                                    "Time (s)", "Time (s)", "Time (s)", "Time (s)",
                                    "Time (s)", "Time (s)", "Time (s)", "Time (s)"],
                                   ["COPx (mm)", "COPx (mm)", "COPx (mm)", "COPx (mm)",
                                    "COPy (mm)", "COPy (mm)", "COPy (mm)", "COPy (mm)",
                                    "V (m/s)", "V (m/s)", "V (m/s)", "V (m/s)",
                                    "A (m2/s)", "A (m2/s)", "A (m2/s)", "A (m2/s)"]
                                   , 4, 4,
                                   legend=[[], [], [], [], [], [], [], [],
                                           ["Vx", "Vy"], ["Vx", "Vy"], ["Vx", "Vy"], ["Vx", "Vy"],
                                           ["Ax", "Ay"], ["Ax", "Ay"], ["Ax", "Ay"], ["Ax", "Ay"]], tight=True)
    add_sup_title(figure, "Motion Report")
plot = False
if plot:
    #motion_report(patient, " - Two Feet Eyes Open (" + str(round(s1[0][0][-1] - s1[0][0][0], 2)) + " s)", cop1, s1)
    #motion_report(patient, " - Two Feet Eyes Closed (" + str(round(s2[0][0][-1] - s2[0][0][0], 2)) + " s)", cop2, s2)
    #motion_report(patient, " - One Feet Eyes Open " + str(round(s3[0][0][-1] - s3[0][0][0], 2)) + " s)", cop3, s3)
    motion_report(patient, " - One Feet Eyes Closed " + str(round(s4[0][0][-1] - s4[0][0][0], 2)) + " s)", cop4, s4)

window = 20

[s1_, s2_, s3_, s4_] = smooth_intervals([s1, s2, s3, s4], window)
[cop1_, cop2_, cop3_, cop4_] = interval_COPs([s1_, s2_, s3_, s4_])

plot = False

if plot:
    #motion_report(patient, " - Two Feet Eyes Open (Smoothed " + str(window) + " points)(" + str(round(s1[0][0][-1] - s1[0][0][0], 2)) + " s)", cop1_, s1_)
    #motion_report(patient, " - Two Feet Eyes Closed (Smoothed " + str(window) + " points)(" + str(round(s2[0][0][-1] - s2[0][0][0], 2)) + " s)", cop2_, s2_)
    #motion_report(patient, " - One Feet Eyes Open (Smoothed " + str(window) + " points)(" + str(round(s3[0][0][-1] - s3[0][0][0], 2)) + " s)", cop3_, s3_)
    motion_report(patient, " - One Feet Eyes Closed (Smoothed " + str(window) + " points)(" + str(round(s4[0][0][-1] - s4[0][0][0], 2)) + " s)", cop4_, s4_)

# Zero out data

EMG_zero, EMG_l_zero, EMG_means_zero = load_emg_rest(folder_name+patient+'/Base')

plot = False
if plot:
    figure, axes = subplot_overlap([range(0, len(EMG_zero[0])), range(0, len(EMG_zero[0])),
                                    range(0, len(EMG_zero[0])), range(0, len(EMG_zero[0]))],
                                   [[EMG_zero[0]], [EMG_zero[1]], [EMG_zero[2]], [EMG_zero[3]]], EMG_l_zero,
                                   ["Index", "Index", "Index", "Index"], ["Raw", "Raw", "Raw", "Raw"], 4, 1, tight=True,
                                   legend=[[EMG_l_zero[0]], [EMG_l_zero[1]], [EMG_l_zero[2]], [EMG_l_zero[3]]])
    add_hlines(axes[0], [0, len(EMG_zero[0])], EMG_means_zero[0], "Mean")
    add_hlines(axes[1], [0, len(EMG_zero[0])], EMG_means_zero[1], "Mean")
    add_hlines(axes[2], [0, len(EMG_zero[0])], EMG_means_zero[2], "Mean")
    add_hlines(axes[3], [0, len(EMG_zero[0])], EMG_means_zero[3], "Mean")

[s1_z, s2_z, s3_z, s4_z] = zero_out_EMG([s1_, s2_, s3_, s4_], EMG_means_zero)

plot = True

if plot:
    motion_report(patient, " - Two Feet Eyes Open (Smoothed " + str(window) + " points)(" + str(round(s1[0][0][-1] - s1[0][0][0], 2)) + " s)", cop1_, s1_z)
    motion_report(patient, " - Two Feet Eyes Closed (Smoothed " + str(window) + " points)(" + str(round(s2[0][0][-1] - s2[0][0][0], 2)) + " s)", cop2_, s2_z)
    motion_report(patient, " - One Feet Eyes Open (Smoothed " + str(window) + " points)(" + str(round(s3[0][0][-1] - s3[0][0][0], 2)) + " s)", cop3_, s3_z)
    motion_report(patient, " - One Feet Eyes Closed (Smoothed " + str(window) + " points)(" + str(round(s4[0][0][-1] - s4[0][0][0], 2)) + " s)", cop4_, s4_z)


plot_show_all()