from grids import *
from DataProcessor.processing_methods import wii_smoother, center_axis, normalization, multiple_vals
from printing_lib import *

# RAW DATA PLOTTING


def raw_reporting(data, patient, ranges_, open_signal_var = "open_signals_data", wii_smoothing=False,
                  smoothing_indexes=(10, 10, 10), cop_ynormalization="global", emg_ynormalization="global",
                  emg_smoothing=False, smoothed_var="smoothed_data", smoothed_ynormalization="global"):
    
    segments = [" - Two Feet Eyes Open (", " - Two Feet Eyes Closed (", " - One Feet Eyes Open (",
                " - One Feet Eyes Closed ("]
    
    raw_figures = []

    ranges = [[], [], [], []]

    for i in range(0, len(data)):
        title = patient + segments[i]
        if cop_ynormalization == 'segment':
            ranges[0] = [ranges_[0][i]]
            ranges[2] = [ranges_[3][i]]
            ranges[3] = [ranges_[4][i]]
        elif cop_ynormalization == 'global':
            ranges[0] = [max(ranges_[0])]
            ranges[2] = [max(ranges_[3])]
            ranges[3] = [max(ranges_[4])]
        if emg_smoothing:
            if smoothed_ynormalization == 'segment':
                ranges[1] = [ranges_[2][i]]
            elif smoothed_ynormalization == 'global':
                ranges[1] = [max(ranges_[2])]
        else:
            if emg_ynormalization == 'segment':
                ranges[1] = [ranges_[1][i]]
            elif emg_ynormalization == 'global':
                ranges[1] = [max(ranges_[1])]

        raw_figures.append(single_raw_report(title, data[i], open_signal_var, wii_smoothing, smoothing_indexes,
                  emg_smoothing, smoothed_var, ranges))
    
    return raw_figures


def single_raw_report(title, data_segment, open_signal_var, wii_smoothing, smoothing_indexes,
                  emg_smoothing, smoothed_var, ranges=([], [], [], [])):
    
    wii = data_segment.get_variable("wii_data")
    open_signal_data = data_segment.get_variable(open_signal_var)
    labels = data_segment.get_variable("labels")

    title = title + str(round(wii[0][-1] - wii[0][0], 2)) + " s)"

    f, gs1_ax, gs2_ax, gs3_ax = grid_report(title)
    if wii_smoothing:
        wii[6] = wii_smoother(wii[6], smoothing_indexes)

    axe_populator([wii[6][0], [wii[6][1]], "COPx (mm)", "COPy (mm)", "COP", []], gs1_ax[0], wii=True)

    axe_populator([open_signal_data[0], [open_signal_data[5], open_signal_data[6], open_signal_data[7]],
                   "Time (s)", "Raw data", "Accelerometer data", labels[1][4:7]], gs1_ax[1], n_col=3,
                  ylim=[np.min([open_signal_data[5], open_signal_data[6], open_signal_data[7]]) * 0.95,
                        np.max([open_signal_data[5], open_signal_data[6], open_signal_data[7]]) * 1.05])

    axe_populator([open_signal_data[0], [open_signal_data[8]], "Time (s)", "Raw data", "ECG data",
                   []], gs1_ax[2])

    if len(ranges[0]) != 0:
        axe_populator([wii[0], [wii[6][0]], "Time (s)", "COPx (mm)", "COPx", []], gs2_ax[0],
                      ylim=center_axis(wii[6][0], ranges[0], cop=True))
        axe_populator([wii[0], [wii[6][1]], "Time (s)", "COPy (mm)", "COPy", []], gs2_ax[1],
                      ylim=center_axis(wii[6][1], ranges[0], cop=True))
        axe_populator([wii[0][0:-1], [wii[6][2]], "Time (s)", "Vx (m/s)", "Vx", []], gs2_ax[2],
                      ylim=center_axis(wii[6][2], ranges[2], cop=True))
        axe_populator([wii[0][0:-2], [wii[6][4]], "Time (s)", "Ax (m2/s)", "Ax", []], gs2_ax[4],
                      ylim=center_axis(wii[6][4], ranges[3]))
        axe_populator([wii[0][0:-1], [wii[6][3]], "Time (s)", "Vy (m/s)", "Vy", []], gs2_ax[3],
                      ylim=center_axis(wii[6][3], ranges[2]))
        axe_populator([wii[0][0:-2], [wii[6][5]], "Time (s)", "Ay (m2/s)", "Ay", []], gs2_ax[5],
                      ylim=center_axis(wii[6][5], ranges[3]))

    else:
        axe_populator([wii[0], [wii[6][0]], "Time (s)", "COPx (mm)", "COPx", []], gs2_ax[0])
        axe_populator([wii[0], [wii[6][1]], "Time (s)", "COPy (mm)", "COPy", []], gs2_ax[1])
        axe_populator([wii[0][0:-1], [wii[6][2]], "Time (s)", "Vx (m/s)", "Vx", []], gs2_ax[2])
        axe_populator([wii[0][0:-2], [wii[6][4]], "Time (s)", "Ax (m2/s)", "Ax", []], gs2_ax[4])
        axe_populator([wii[0][0:-1], [wii[6][3]], "Time (s)", "Vy (m/s)", "Vy", []], gs2_ax[3])
        axe_populator([wii[0][0:-2], [wii[6][5]], "Time (s)", "Ay (m2/s)", "Ay", []], gs2_ax[5])

    padding = True

    if emg_smoothing:
        open_signal_data = data_segment.get_variable(smoothed_var)
        padding = False

    if len(ranges[0]) != 0:
        axe_populator([open_signal_data[0], [open_signal_data[1]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[0],
                      auto_padding=padding, ylim=center_axis(open_signal_data[1], ranges[1], smooth=emg_smoothing))
        axe_populator([open_signal_data[0], [open_signal_data[2]], "Time (s)", "Raw", labels[1][1], []], gs3_ax[1],
                      auto_padding=padding, ylim=center_axis(open_signal_data[2], ranges[1], smooth=emg_smoothing))
        axe_populator([open_signal_data[0], [open_signal_data[3]], "Time (s)", "Raw", labels[1][2], []], gs3_ax[2],
                      auto_padding=padding, ylim=center_axis(open_signal_data[3], ranges[1], smooth=emg_smoothing))
        axe_populator([open_signal_data[0], [open_signal_data[4]], "Time (s)", "Raw", labels[1][3], []], gs3_ax[3],
                      auto_padding=padding, ylim=center_axis(open_signal_data[4], ranges[1], smooth=emg_smoothing))
    else:
        axe_populator([open_signal_data[0], [open_signal_data[1]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[0],
                      auto_padding=padding)
        axe_populator([open_signal_data[0], [open_signal_data[2]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[1],
                      auto_padding=padding)
        axe_populator([open_signal_data[0], [open_signal_data[3]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[2],
                      auto_padding=padding)
        axe_populator([open_signal_data[0], [open_signal_data[4]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[3],
                      auto_padding=padding)

    return f
        

# COMPARING PLOTS


def single_comparing_report(text, data, smoothed_var, wii_smoothing, smoothing_indexes,
                     ranges=([], [], [], []), cop_norm=False, smooth_norm=False):

    wii = data.get_variable("wii_data")
    labels = data.get_variable("labels")
    RMS = data.get_variable(smoothed_var)

    text = text + str(round(wii[0][-1] - wii[0][0], 2)) + " s)"

    f, gs1_ax, gs2_ax = grid_overlay(text)
    if wii_smoothing:
        wii[6] = wii_smoother(wii[6], smoothing_indexes)

    if cop_norm:
        cops = [wii[6][0], wii[6][1]]
        vel = [wii[6][2], wii[6][3]]
        acc = [wii[6][4], wii[6][5]]

        [wii[6][0], wii[6][1]] = normalization(cops, multiple_vals(cops, ranges[0], cop=True))
        [wii[6][2], wii[6][3]] = normalization(vel, multiple_vals(vel, ranges[2]))
        [wii[6][4], wii[6][5]] = normalization(acc, multiple_vals(acc, ranges[3]))

    if smooth_norm:
        RMS[1:5] = normalization(RMS[1:5], multiple_vals(RMS[1:5], ranges[1], smooth=True))

    axe_populator([wii[0], [wii[6][0]], "Time (s)", "Norm", "COPx", ["COPx"]], gs1_ax[0], offset=False)
    axe_populator([RMS[0], RMS[1:5], "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[0], overlap=True,
                  offset=True, offset_index=0, legend_outside=True, ylim=[-0.5, 4.5])

    axe_populator([wii[0], [wii[6][1]], "Time (s)", "Norm", "COPy", ["COPy"]], gs1_ax[1], offset=False)
    axe_populator([RMS[0], RMS[1:5], "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[1], overlap=True,
                  offset=True, offset_index=0, legend_outside=True, ylim=[-0.5, 4.5])

    axe_populator([wii[0][0:-1], [wii[6][2]], "Time (s)", "Norm", "Vx", ["Vx"]], gs1_ax[2], offset=False)
    axe_populator([RMS[0], RMS[1:5], "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[2], overlap=True,
                  offset=True, offset_index=0, legend_outside=True, ylim=[-0.5, 4.5])

    axe_populator([wii[0][0:-1], [wii[6][3]], "Time (s)", "Norm", "Vy", ["Vy"]], gs1_ax[3], offset=False)
    axe_populator([RMS[0], RMS[1:5], "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[3], overlap=True,
                  offset=True, offset_index=0, legend_outside=True, ylim=[-0.5, 4.5])

    axe_populator([wii[0][0:-2], [wii[6][4]], "Time (s)", "Norm", "Ax", ["Ax"]], gs1_ax[4], offset=False)
    axe_populator([RMS[0], RMS[1:5], "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[4], overlap=True,
                  offset=True, offset_index=0, legend_outside=True, ylim=[-0.5, 4.5])

    axe_populator([wii[0][0:-2], [wii[6][5]], "Time (s)", "Norm", "Ay", ["Ay"]], gs1_ax[5], offset=False)
    axe_populator([RMS[0], RMS[1:5], "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[5], overlap=True,
                  offset=True, offset_index=0, legend_outside=True, ylim=[-0.5, 4.5])
    ###
    axe_populator([RMS[0], [RMS[1], RMS[4]], "Time (s)", "RMS", "Right Side", [labels[1][0], labels[1][3]]], gs2_ax[1],
                  overlap=False, offset=False)
    axe_populator([RMS[0], [(np.array(RMS[1]) - np.array(RMS[4]))], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[1], overlap=True, offset=True, offset_index=1, legend_outside=False, plot_over=True, n_col=3,
                  leg_font=7, ylim=[0, 3])

    axe_populator([RMS[0], [RMS[2], RMS[3]], "Time (s)", "RMS", "Left Side", [labels[1][1], labels[1][2]]], gs2_ax[2],
                  overlap=False, offset=False)
    axe_populator([RMS[0], [(np.array(RMS[1]) - np.array(RMS[3]))], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[2], overlap=True, offset=True, offset_index=1, legend_outside=False, plot_over=True, n_col=3,
                  leg_font=7, ylim=[0, 3])

    axe_populator([RMS[0], [RMS[3], RMS[4]], "Time (s)", "RMS", "Back Side", [labels[1][2], labels[1][3]]], gs2_ax[3],
                  overlap=False, offset=False)
    axe_populator([RMS[0], [(np.array(RMS[3]) - np.array(RMS[4]))], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[3], overlap=True, offset=True, offset_index=1, legend_outside=False, plot_over=True, n_col=3,
                  leg_font=7, ylim=[0, 3])

    axe_populator([RMS[0], [RMS[1], RMS[2]], "Time (s)", "RMS", "Right Side", [labels[1][0], labels[1][1]]], gs2_ax[4],
                  overlap=False, offset=False)
    axe_populator([RMS[0], [(np.array(RMS[1]) - np.array(RMS[2]))], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[4], overlap=True, offset=True, offset_index=1, legend_outside=False, plot_over=True, n_col=3,
                  leg_font=7, ylim=[0, 3])

    return f


def comparing_reports(data, patient, ranges_, smoothed_var="smoothed_data", wii_smoothing=False,
                      smoothing_indexes=(10, 10, 10), cop_ynormalization="global",
                      smoothed_ynormalization="global"):

    segments = [" - Two Feet Eyes Open (", " - Two Feet Eyes Closed (", " - One Feet Eyes Open (",
                " - One Feet Eyes Closed ("]

    comparing_figures = []
    ranges = [[], [], [], []]
    cop_norm = False
    smooth_norm = False
    for i in range(0, len(data)):

        if cop_ynormalization == 'segment':
            ranges[0] = [ranges_[0][i]]
            ranges[2] = [ranges_[3][i]]
            ranges[3] = [ranges_[4][i]]
            cop_norm = True
        elif cop_ynormalization == 'global':
            ranges[0] = [max(ranges_[0])]
            ranges[2] = [max(ranges_[3])]
            ranges[3] = [max(ranges_[4])]
            cop_norm = True
        if smoothed_ynormalization == 'segment':
            ranges[1] = [ranges_[2][i]]
            smooth_norm = True
        elif smoothed_ynormalization == 'global':
            ranges[1] = [max(ranges_[2])]
            smooth_norm = True
        title = patient + "(COP_Norm = " + cop_ynormalization + ", Smooth_Norm = " + smoothed_ynormalization + ")" \
                + segments[i]

        comparing_figures.append(single_comparing_report(title, data[i], smoothed_var, wii_smoothing,
                                                         smoothing_indexes, ranges, cop_norm=cop_norm,
                                                         smooth_norm=smooth_norm))
    return comparing_figures


#ADICIONAR REPORT COM SO OS DADOS NORMALIZADOS EM OVERLAY