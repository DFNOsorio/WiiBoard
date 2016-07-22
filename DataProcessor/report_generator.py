from DataProcessor.Printing import *


def motion_report(patient, text, data, emg_data):

    Wii = data.get_variable("wii_data")
    EMGs = data.get_variable(emg_data)
    labels = data.get_variable("labels")

    text = text + str(round(Wii[0][-1] - Wii[0][0], 2)) + " s)"

    f, gs1_ax, gs2_ax, gs3_ax = grid_report(patient + text)

    axe_populator([Wii[6][0], [Wii[6][1]], "COPx (mm)", "COPy (mm)", "COP", []], gs1_ax[0], wii=True)
    axe_populator([EMGs[0], [EMGs[5], EMGs[6], EMGs[7]], "Time (s)", "Raw data", "Accelerometer data",
                   labels[1][4:7]], gs1_ax[1], xlim=[min(EMGs[0]), max(EMGs[0])+5])
    axe_populator([EMGs[0], [EMGs[8]], "Time (s)", "Raw data", "ECG data",
                   []], gs1_ax[2])

    axe_populator([Wii[0], [Wii[6][0]], "Time (s)", "COPx (mm)", "COPx", []], gs2_ax[0])
    axe_populator([Wii[0][0:-1], [Wii[6][2]], "Time (s)", "Vx (m/s)", "Vx", []], gs2_ax[2])
    axe_populator([Wii[0][0:-2], [Wii[6][4]], "Time (s)", "Ax (m2/s)", "Ax", []], gs2_ax[4])

    axe_populator([Wii[0], [Wii[6][1]], "Time (s)", "COPy (mm)", "COPy", []], gs2_ax[1])
    axe_populator([Wii[0][0:-1], [Wii[6][3]], "Time (s)", "Vy (m/s)", "Vy", []], gs2_ax[3])
    axe_populator([Wii[0][0:-2], [Wii[6][5]], "Time (s)", "Ay (m2/s)", "Ay", []], gs2_ax[5])

    axe_populator([EMGs[0], [EMGs[1]], "Time (s)", "Raw", labels[1][0], []], gs3_ax[0])
    axe_populator([EMGs[0], [EMGs[2]], "Time (s)", "Raw", labels[1][1], []], gs3_ax[1])
    axe_populator([EMGs[0], [EMGs[3]], "Time (s)", "Raw", labels[1][2], []], gs3_ax[2])
    axe_populator([EMGs[0], [EMGs[4]], "Time (s)", "Raw", labels[1][3], []], gs3_ax[3])

    return f


def motion_reports(patient, data, emg_data="open_signals_data"):
    title_1 = [" - Two Feet Eyes Open (", " - Two Feet Eyes Closed (",
               " - One Feet Eyes Open (", " - One Feet Eyes Closed ("]
    for i in range(0, len(data)):
        motion_report(patient, title_1[i], data[i], emg_data)


def spectrogram_report(data, max_flag=False, data_var="spec_data"):

    title = ["Spectrogram - Two Feet Eyes Open (1 s segments)", "Spectrogram - Two Feet Eyes Closed (1 s segments)",
              "Spectrogram - One Feet Eyes Open (1 s segments)", "Spectrogram - One Feet Eyes Closed (1 s segments)"]
    axes = []
    max_ = 0
    min_ = 100
    for i in range(0, len(data)):
        spec = data[i].get_variable(data_var)
        for j in range(0, len(spec)):
            if spec[j][5][0] > max_:
                max_ = spec[j][5][0]
            if spec[j][5][1] < min_:
                min_ = spec[j][5][1]

    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])
        axes_=[]
        for j in range(0, 4):
            spec = data[i].get_variable(data_var)
            ax = f.add_subplot(2, 2, j + 1)
            ax, im = spectogram_plot(ax, spec[j][1], spec[j][2], spec[j][3], title=data[i].get_variable("labels")[1][j],
                                     no_colorbar=True, v=[min_, max_])
            if max_flag:
                ax = max_spec_overplot(ax, spec[j][1], spec[j][2], spec[j][3])
            axes_.append(ax)
        axes.append(axes_)
        cax = f.add_axes([0.91, 0.1, 0.02, 0.8])
        cbar = f.colorbar(im, cax=cax, ticks=range(int(min_), int(max_), 5))
        im.set_clim(max([-50, int(min_)]), int(max_))
        cbar.set_label('Power Spectral Density (dB)')
        plt.subplots_adjust(hspace=0.34, top=0.90, bottom=0.09, left=0.10, right=0.90, wspace=0.27)
    return axes


def psd_reports(data, new_var="psd_data"):
    title = ["PSD - Two Feet Eyes Open", "PSD - Two Feet Eyes Closed",
             "PSD - One Feet Eyes Open", "PSD - One Feet Eyes Closed"]
    axes = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])
        axes1 = []
        axes2 = []
        PSD = data[i].get_variable(new_var)
        for j in range(0, 4):

            ax1 = f.add_subplot(2, 4, j+1)
            PSD_plot(ax1, PSD[j][1], PSD[j][2], title=data[i].get_variable("labels")[1][j])

            ax2 = f.add_subplot(2, 4, (j+5))
            PSD_plot(ax2, PSD[j][0], PSD[j][2], title=data[i].get_variable("labels")[1][j],
                     y_label="Power Spectral Density (No dB)")

            axes1.append(ax1)
            axes2.append(ax2)

        axes.append(np.concatenate([axes1, axes2]))
    return axes


def rms_reports(data, rms_data="emg_rms_data", emg_data="open_signals_data"):
    title = ["RMS - Two Feet Eyes Open", "RMS - Two Feet Eyes Closed",
             "RMS - One Feet Eyes Open", "RMS - One Feet Eyes Closed"]
    axes = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])
        axes_ = []
        RMS = data[i].get_variable(rms_data)
        EMGs = data[i].get_variable(emg_data)
        current_time = EMGs[0]
        for j in range(0, 4):
            ax1 = f.add_subplot(2, 2, j+1)
            EMGRMS_plot(ax1, current_time, [EMGs[j+1], RMS[j]], title=data[i].get_variable("labels")[1][j])
            axes_.append(ax1)
        axes.append(axes_)
    return axes


def spec_psd_integrated(data, integrated_data="integrated_spec_psd"):
    title = ["EMG Spectrum Energy - Two Feet Eyes Open", "EMG Spectrum Energy - Two Feet Eyes Closed",
             "EMG Spectrum Energy - One Feet Eyes Open", "EMG Spectrum Energy - One Feet Eyes Closed"]

    axes = []

    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])

        psd_integrated_data = data[i].get_variable(integrated_data)
        time = data[i].get_variable("spec_data")[0][3]
        axes_ = []
        for j in range(0, 4):
            ax1 = f.add_subplot(2, 2, j + 1)
            ax1 = axe_populator([time, [psd_integrated_data[j][1]], "Frequency (Hz)", "Energy",
                                 data[i].get_variable("labels")[1][j], ["Spec Energy"]], ax1, color='k')

            axes_.append(ax1)
        axes.append(axes_)
    return axes


def spec_psd_overlay(data, data_var_psd="psd_data", data_var_spec="spec_data", alpha=0.1, dB="True"):
    title = ["EMG Spectrum Energy - Two Feet Eyes Open", "EMG Spectrum Energy - Two Feet Eyes Closed",
             "EMG Spectrum Energy - One Feet Eyes Open", "EMG Spectrum Energy - One Feet Eyes Closed"]
    mode = 0
    if dB:
        mode = 1

    axes = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])

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
    return axes
