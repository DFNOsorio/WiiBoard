from DataProcessor.Printing import *
from novainstrumentation import *


def motion_report(patient, text, data, emg_data, thresholds, normalazing):

    Wii = data.get_variable("wii_data")
    EMGs = data.get_variable(emg_data)
    labels = data.get_variable("labels")

    text = text + str(round(Wii[0][-1] - Wii[0][0], 2)) + " s)"

    f, gs1_ax, gs2_ax, gs3_ax = grid_report(patient + text)

    cops_ranges = []
    emg_ranges = []

    if normalazing:
        cops_ranges, cop_range_ = normalize_range([Wii[6][0], Wii[6][1]], cop=True)
        emg_ranges, emg_range_ = normalize_range([EMGs[1], EMGs[2], EMGs[3], EMGs[4]])


    axe_populator([Wii[6][0], [Wii[6][1]], "COPx (mm)", "COPy (mm)", "COP", []], gs1_ax[0], wii=True)
    axe_populator([EMGs[0], [EMGs[5], EMGs[6], EMGs[7]], "Time (s)", "Raw data", "Accelerometer data",
                   labels[1][4:7]], gs1_ax[1], n_col=3,
                  ylim=[np.min([EMGs[5], EMGs[6], EMGs[7]])*0.95, np.max([EMGs[5], EMGs[6], EMGs[7]])*1.05])
    axe_populator([EMGs[0], [EMGs[8]], "Time (s)", "Raw data", "ECG data",
                   []], gs1_ax[2])

    axe_populator([Wii[0], [Wii[6][0]], "Time (s)", "COPx (mm)", "COPx", []], gs2_ax[0], ylim=cops_ranges[0])
    axe_populator([Wii[0][0:-1], [Wii[6][2]], "Time (s)", "Vx (m/s)", "Vx", []], gs2_ax[2])
    axe_populator([Wii[0][0:-2], [Wii[6][4]], "Time (s)", "Ax (m2/s)", "Ax", []], gs2_ax[4])

    axe_populator([Wii[0], [Wii[6][1]], "Time (s)", "COPy (mm)", "COPy", []], gs2_ax[1], ylim=cops_ranges[1])
    axe_populator([Wii[0][0:-1], [Wii[6][3]], "Time (s)", "Vy (m/s)", "Vy", []], gs2_ax[3])
    axe_populator([Wii[0][0:-2], [Wii[6][5]], "Time (s)", "Ay (m2/s)", "Ay", []], gs2_ax[5])

    axe_populator([EMGs[0], [EMGs[1]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[0], auto_padding=True, auto_lim=True,
                  ylim=emg_ranges)
    axe_populator([EMGs[0], [EMGs[2]], "Time (s)", "Raw", labels[1][1], []], gs3_ax[1], auto_padding=True, auto_lim=True,
                  ylim=emg_ranges)
    axe_populator([EMGs[0], [EMGs[3]], "Time (s)", "Raw", labels[1][2], []], gs3_ax[2], auto_padding=True, auto_lim=True,
                  ylim=emg_ranges)
    axe_populator([EMGs[0], [EMGs[4]], "Time (s)", "Raw", labels[1][3], []], gs3_ax[3], auto_padding=True, auto_lim=True,
                  ylim=emg_ranges)

    if thresholds:
        for i in range(0, 4):

            gs2_ax[i+2].legend("Raw_Data")

            axe_populator([Wii[7][i][1], [Wii[7][i][0]], "Time (s)", "Vx (m/s)", "Vx", ["Threshold"]], gs2_ax[i+2],
                          overlap=True, color='r', linestyle='dotted')

    return f


def COP_report(patient, text, data, emg_data, rms_data):

    Wii = data.get_variable("wii_data")
    labels = data.get_variable("labels")
    RMS = data.get_variable(rms_data)
    EMGs = data.get_variable(emg_data)

    text = text + str(round(Wii[0][-1] - Wii[0][0], 2)) + " s)"

    f, gs1_ax, gs2_ax = grid_cops(patient + text)

    axe_populator([Wii[0], [Wii[6][0]], "Time (s)", "COPx (mm)", "COPx", []], gs1_ax[0])
    axe_populator([Wii[0][0:-1], [Wii[6][2]], "Time (s)", "Vx (m/s)", "Vx", []], gs1_ax[2])
    axe_populator([Wii[0][0:-2], [Wii[6][4]], "Time (s)", "Ax (m2/s)", "Ax", []], gs1_ax[4])

    axe_populator([Wii[0], [Wii[6][1]], "Time (s)", "COPy (mm)", "COPy", []], gs1_ax[1])
    axe_populator([Wii[0][0:-1], [Wii[6][3]], "Time (s)", "Vy (m/s)", "Vy", []], gs1_ax[3])
    axe_populator([Wii[0][0:-2], [Wii[6][5]], "Time (s)", "Ay (m2/s)", "Ay", []], gs1_ax[5])

    for i in range(0, 4):
        axe_populator([EMGs[0], [RMS[i]], "Time (s)", "RMS", labels[1][i], []], gs2_ax[i])

    return f


def comparing_report(patient, text, data, emg_data, rms_data, normalazing, smoothing, smoothing_indexes=(10, 50)):

    Wii = data.get_variable("wii_data")
    labels = data.get_variable("labels")
    RMS = data.get_variable(rms_data)
    EMGs = data.get_variable(emg_data)

    text = text + str(round(Wii[0][-1] - Wii[0][0], 2)) + " s)"

    f, gs1_ax, gs2_ax = grid_overlay(patient + text)

    if normalazing:
        cops_ranges, cop_range_ = normalize_range([Wii[6][0], Wii[6][1]], cop=True)
        emg_ranges, emg_range_ = normalize_range([EMGs[1], EMGs[2], EMGs[3], EMGs[4]])
        # sfsdfsdf
        # SPEC ENERGIA EM VEZ DE MAX
        # ELECTORO VS EMG
        # A DIFERENCA DIZER PARA ONDE ANDA
        # ACC OVERLAY
        # NOME+FICHEIRO EM TODOS

    if smoothing:
        Wii[6][0] = smooth(np.array(Wii[6][0]), smoothing_indexes[0])
        Wii[6][1] = smooth(np.array(Wii[6][1]), smoothing_indexes[0])
        Wii[6][2] = smooth(np.array(Wii[6][2]), smoothing_indexes[1])
        Wii[6][3] = smooth(np.array(Wii[6][3]), smoothing_indexes[1])
        Wii[6][4] = smooth(np.array(Wii[6][4]), smoothing_indexes[1])
        Wii[6][5] = smooth(np.array(Wii[6][5]), smoothing_indexes[1])



    axe_populator([Wii[0], [Wii[6][0]], "Time (s)", "Norm", "COPx", ["COPx"]],
                  gs1_ax[0], norm=True, offset=True)
    axe_populator([EMGs[0], RMS, "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[0], norm=True, overlap=True,
                  offset=True, offset_index=0, legend_outside=True)

    axe_populator([Wii[0], [Wii[6][1]], "Time (s)", "Norm", "COPy", ["COPy"]],
                  gs1_ax[1], norm=True, offset=True)
    axe_populator([EMGs[0], RMS, "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[1], norm=True, overlap=True,
                  offset=True, offset_index=0, legend_outside=True)

    axe_populator([Wii[0][0:-1], [Wii[6][2]], "Time (s)", "Norm", "Vx", ["Vx"]], gs1_ax[2], norm=True)
    axe_populator([EMGs[0], RMS, "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[2], norm=True, overlap=True,
                  offset=True, legend_outside=True)

    axe_populator([Wii[0][0:-1], [Wii[6][3]], "Time (s)", "Norm", "Vy", ["Vy"]], gs1_ax[3], norm=True)
    axe_populator([EMGs[0], RMS, "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[3], norm=True, overlap=True,
                  offset=True, legend_outside=True)

    axe_populator([Wii[0][0:-2], [Wii[6][4]], "Time (s)", "Norm", "Ax", ["Ax"]], gs1_ax[4], norm=True)
    axe_populator([EMGs[0], RMS, "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[4], norm=True, overlap=True,
                  offset=True, legend_outside=True)

    axe_populator([Wii[0][0:-2], [Wii[6][5]], "Time (s)", "Norm", "Ay", ["Ay"]], gs1_ax[5], norm=True)
    axe_populator([EMGs[0], RMS, "Time (s)", "RMS", "COPx", labels[1][0:4]], gs1_ax[5], norm=True, overlap=True,
                  offset=True, legend_outside=True)

    axe_populator([Wii[0], [Wii[6][0], Wii[6][1]], "Time (s)", "Norm", "COPs", ["COPx", "COPy"]], gs2_ax[0], norm=True,
                  overlap=False, offset=True)
    axe_populator([Wii[0], [Wii[6][0], Wii[6][1]], "Time (s)", "Norm", "COPx", ["COPx", "COPy"]],
                  gs2_ax[0], norm=True, offset=False, overlap=True, offset_index=1.05, legend_outside=True)

    #RMS

    axe_populator([EMGs[0], [RMS[0], RMS[3]], "Time (s)", "RMS", "Right Side", [labels[1][0], labels[1][3]]], gs2_ax[1],
                  norm=True, overlap=False, offset=False)
    axe_populator([EMGs[0], [np.array(RMS[0]) - np.array(RMS[3])], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[1], norm=True, overlap=True, offset=True, offset_index=0.05, ylim=[0, 2.5], n_col=3, leg_font=7)

    axe_populator([EMGs[0], [RMS[1], RMS[2]], "Time (s)", "RMS", "Left Side", [labels[1][1], labels[1][2]]], gs2_ax[2],
                  norm=True, overlap=False, offset=False)
    axe_populator([EMGs[0], [np.array(RMS[1]) - np.array(RMS[2])], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[2], norm=True, overlap=True, offset=True, offset_index=0.05, ylim=[0, 2.5], n_col=3, leg_font=7)

    axe_populator([EMGs[0], [RMS[2], RMS[3]], "Time (s)", "RMS", "Back Side", [labels[1][2], labels[1][3]]], gs2_ax[3],
                  norm=True, overlap=False, offset=False)
    axe_populator([EMGs[0], [np.array(RMS[2]) - np.array(RMS[3])], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[3], norm=True, overlap=True, offset=True, offset_index=0.05, ylim=[0, 2.5], n_col=3, leg_font=7)

    axe_populator([EMGs[0], [RMS[0], RMS[1]], "Time (s)", "RMS", "Front Side", [labels[1][0], labels[1][1]]], gs2_ax[4],
                  norm=True, overlap=False, offset=False)
    axe_populator([EMGs[0], [np.array(RMS[0]) - np.array(RMS[1])], "Time (s)", "RMS", "Right Side", ["Subtraction"]],
                  gs2_ax[4], norm=True, overlap=True, offset=True, offset_index=0.05, ylim=[0, 2.5], n_col=3, leg_font=7)

    return f


def motion_reporting(patient, data, emg_data="open_signals_data", thresholds=False, rms_data=False, smoothing=False,
                   normalazing=(False, False)):
    title_1 = [" - Two Feet Eyes Open (", " - Two Feet Eyes Closed (",
               " - One Feet Eyes Open (", " - One Feet Eyes Closed ("]
    montion_figs = []
    comparing_figs = []
    for i in range(0, len(data)):
        f1 = motion_report(patient, title_1[i], data[i], emg_data, thresholds, normalazing[0])

        f2 = comparing_report(patient, title_1[i], data[i], emg_data, rms_data, normalazing[1], smoothing)

        montion_figs.append(f1)
        comparing_figs.append(f2)

    return montion_figs, comparing_figs


def spectrogram_report(data, integration_flag=False, data_var="spec_data", integrated_data="integrated_spec_psd",
                       seg_norm=True, global_norm=False):

    title = ["Spectrogram - Two Feet Eyes Open (1 s segments)", "Spectrogram - Two Feet Eyes Closed (1 s segments)",
             "Spectrogram - One Feet Eyes Open (1 s segments)", "Spectrogram - One Feet Eyes Closed (1 s segments)"]
    axes = []
    figures = []
    max_ = [0, 0]
    min_ = [100, 10000]
    max_y = []
    for i in range(0, len(data)):
        spec = data[i].get_variable(data_var)
        inte = data[i].get_variable(integrated_data)
        for j in range(0, len(spec)):
            if spec[j][5][0] > max_[0]:
                max_[0] = spec[j][5][0]
            if spec[j][5][1] < min_[0]:
                min_[0] = spec[j][5][1]
        temp_max = 0
        for j in range(0, 4):
            temp_max_ = max(data[i].get_variable(integrated_data)[j][1])
            if temp_max_ > temp_max:
                temp_max = temp_max_
        max_y.append(temp_max)

    for i in range(0, len(data)):
        f = plt.figure()
        plt.figtext(0.08, 0.95, title[i], fontsize=20)
        axes_= []
        y_lim = False

        if seg_norm:
            y_lim = [0, max_y[i]]

        elif global_norm:
            y_lim = [0, max(max_y)]

        for j in range(0, 4):
            spec = data[i].get_variable(data_var)
            ax = f.add_subplot(2, 2, j + 1)
            ax, im = spectogram_plot(ax, spec[j][1], spec[j][2], spec[j][3], title=data[i].get_variable("labels")[1][j],
                                     no_colorbar=True, v=[min_[0], max_[0]])
            if integration_flag:
                integrated = data[i].get_variable(integrated_data)[j][1]
                ax = add_newaxis(ax, spec[j][3], integrated, "Integration", alpha=1, legend=["Integration"],
                                 linecolor='k', previous_leg=False, y_lim=y_lim)
            axes_.append(ax)
        axes.append(axes_)
        plt.subplots_adjust(hspace=0.34, top=0.90, bottom=0.09, left=0.10, right=0.85, wspace=0.27)
        cax = f.add_axes([0.91, 0.1, 0.02, 0.8])
        cbar = f.colorbar(im, cax=cax, ticks=range(int(min_[0]), int(max_[0]), 5))
        im.set_clim(max([-50, int(min_[0])]), int(max_[0]))
        cbar.set_label('Power Spectral Density (dB)')
        figures.append(f)
    return figures, axes


def psd_reports(data, new_var="psd_data"):
    title = ["PSD - Two Feet Eyes Open", "PSD - Two Feet Eyes Closed",
             "PSD - One Feet Eyes Open", "PSD - One Feet Eyes Closed"]
    axes = []
    figures =[]
    for i in range(0, len(data)):
        f = plt.figure()
        plt.figtext(0.08, 0.95, title[i], fontsize=20)
        axes1 = []
        axes2 = []
        PSD = data[i].get_variable(new_var)
        for j in range(0, 4):

            ax1 = f.add_subplot(2, 4, j+1)
            ax1 = axe_populator([PSD[j][2], [PSD[j][1]], "Frequencies (Hz)", "Power Spectral Density (dB)",
                                 data[i].get_variable("labels")[1][j], []], ax1)

            ax2 = f.add_subplot(2, 4, (j+5))
            ax2 = axe_populator([PSD[j][2], [PSD[j][0]], "Frequencies (Hz)", "Power Spectral Density (No dB)",
                                 data[i].get_variable("labels")[1][j], []], ax2)

            axes1.append(ax1)
            axes2.append(ax2)

        axes.append(np.concatenate([axes1, axes2]))
        figures.append(f)
    return figures, axes


def rms_reports(data, rms_data="emg_rms_data", emg_data="open_signals_data"):
    title = ["RMS - Two Feet Eyes Open", "RMS - Two Feet Eyes Closed",
             "RMS - One Feet Eyes Open", "RMS - One Feet Eyes Closed"]
    axes = []
    figures = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.figtext(0.08, 0.95, title[i], fontsize=20)
        axes_ = []
        RMS = data[i].get_variable(rms_data)
        EMGs = data[i].get_variable(emg_data)
        current_time = EMGs[0]
        for j in range(0, 4):
            ax1 = f.add_subplot(2, 2, j+1)
            ax1 = axe_populator([current_time, [EMGs[j+1]], "Time (s)", "Energy",
                                 data[i].get_variable("labels")[1][j], ["Spec Energy"]], ax1, auto_padding=True,
                                auto_lim=True)
            ax1 = add_newaxis(ax1, current_time, RMS[j], "RMS", legend="RMS", auto_padding=True, auto_lim=True,
                              alpha=0.8, n_col=2)

            axes_.append(ax1)
        axes.append(axes_)
        plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.05, right=0.95)
        figures.append(f)
    return figures, axes


def spec_psd_integrated(data, integrated_data="integrated_spec_psd", spec_data = "spec_data" ):
    title = ["EMG Spectrum - Two Feet Eyes Open", "EMG Spectrum - Two Feet Eyes Closed",
             "EMG Spectrum - One Feet Eyes Open", "EMG Spectrum - One Feet Eyes Closed"]

    axes = []
    figures = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.figtext(0.08, 0.95, title[i], fontsize=20)

        psd_integrated_data = data[i].get_variable(integrated_data)
        time = data[i].get_variable(spec_data)[0][3]
        axes_ = []
        for j in range(0, 4):
            ax1 = f.add_subplot(2, 2, j + 1)
            ax1 = axe_populator([time, [psd_integrated_data[j][1]], "Time (s)", "Energy",
                                 data[i].get_variable("labels")[1][j], ["Spec Energy"]], ax1, color='k',
                                legend_outside=True)

            axes_.append(ax1)
        axes.append(axes_)
        figures.append(f)
    return figures, axes


def spec_psd_overlay(data, data_var_psd="psd_data", data_var_spec="spec_data", alpha=0.1, dB="True"):
    title = ["EMG Spectrum Energy - Two Feet Eyes Open", "EMG Spectrum Energy - Two Feet Eyes Closed",
             "EMG Spectrum Energy - One Feet Eyes Open", "EMG Spectrum Energy - One Feet Eyes Closed"]
    mode = 0
    if dB:
        mode = 1

    axes = []
    figures = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.figtext(0.08, 0.95, title[i], fontsize=20)

        psds = data[i].get_variable(data_var_psd)
        spec = data[i].get_variable(data_var_spec)

        axes_ = []
        for j in range(0, 4):
            ax1 = f.add_subplot(2, 2, j + 1)

            frequencies = spec[j][2]

            ax1 = axe_populator([frequencies, [spec[j][mode]], "Frequency (Hz)", "Spec",
                                 data[i].get_variable("labels")[1][j], ["Spec"]], ax1, alpha=alpha)

            frequencies = psds[j][2]

            ax1 = axe_populator([frequencies, [psds[j][mode]], "Frequency (Hz)", "Psd",
                                 data[i].get_variable("labels")[1][j], ["Psd"]], ax1, color='k', overlap=True)

            axes_.append(ax1)
        axes.append(axes_)
        figures.append(f)
    return figures, axes