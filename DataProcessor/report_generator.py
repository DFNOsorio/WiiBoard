from DataProcessor.printing import *


def motion_report(patient, text, cop1, s1):

    f, gs1_ax, gs2_ax, gs3_ax = grid_report(patient + text)

    axe_populator([cop1[0], [cop1[1]], "COPx (mm)", "COPy (mm)", "COP", []], gs1_ax[0], wii=True)
    axe_populator([s1[1][0], [s1[1][5], s1[1][6], s1[1][7]], "Time (s)", "Raw data", "Accelerometer data",
                   s1[2][1][4:7]], gs1_ax[1], xlim=[min(s1[1][0]), max(s1[1][0])+5])
    axe_populator([s1[1][0], [s1[1][8]], "Time (s)", "Raw data", "ECG data",
                   []], gs1_ax[2])

    axe_populator([s1[0][0], [cop1[0]], "Time (s)", "COPx (mm)", "COPx", []], gs2_ax[0])
    axe_populator([s1[0][0][0:-1], [cop1[2]], "Time (s)", "Vx (m/s)", "Vx", []], gs2_ax[2])
    axe_populator([s1[0][0][0:-2], [cop1[4]], "Time (s)", "Ax (m2/s)", "Ax", []], gs2_ax[4])

    axe_populator([s1[0][0], [cop1[1]], "Time (s)", "COPy (mm)", "COPy", []], gs2_ax[1])
    axe_populator([s1[0][0][0:-1], [cop1[3]], "Time (s)", "Vy (m/s)", "Vy", []], gs2_ax[3])
    axe_populator([s1[0][0][0:-2], [cop1[5]], "Time (s)", "Ay (m2/s)", "Ay", []], gs2_ax[5])

    axe_populator([s1[1][0], [s1[1][1]], "Time (s)", "Raw", s1[2][1][0], []], gs3_ax[0])
    axe_populator([s1[1][0], [s1[1][2]], "Time (s)", "Raw", s1[2][1][1], []], gs3_ax[1])
    axe_populator([s1[1][0], [s1[1][3]], "Time (s)", "Raw", s1[2][1][2], []], gs3_ax[2])
    axe_populator([s1[1][0], [s1[1][4]], "Time (s)", "Raw", s1[2][1][3], []], gs3_ax[3])

    return f


def motion_reports(patient, data):
    title_1 = [" - Two Feet Eyes Open (", " - Two Feet Eyes Closed (", " - One Feet Eyes Open (", " - One Feet Eyes Closed ("]
    for i in range(0, len(data)):
        motion_report(patient, title_1[i] + str(round(data[i][0][0][-1] - data[i][0][0][0], 2)) + " s)",
                      data[i][0][6], data[i])


def spectrogram_report(data):
    # EMG1(test_1[3][0])
    # EMG2(test_1[3][1])
    # EMG2(test_1[3][2])
    # EMG2(test_1[3][3])
    title = ["Spectrogram - Two Feet Eyes Open (1 s segments)", "Spectrogram - Two Feet Eyes Closed (1 s segments)",
             "Spectrogram - One Feet Eyes Open (1 s segments)", "Spectrogram - One Feet Eyes Closed (1 s segments)"]
    axes = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])
        for j in range(0, len(data)):
            ax = f.add_subplot(2, 2, j+1)
            spectogram_plot(ax, data[i][3][j][1], data[i][3][j][2], data[i][3][j][3], title=data[i][2][1][j])
            axes.append(ax)

    return axes


def spectrogram_report_same_scale(data):

    title = ["Spectrogram - Two Feet Eyes Open (1 s segments)", "Spectrogram - Two Feet Eyes Closed (1 s segments)",
              "Spectrogram - One Feet Eyes Open (1 s segments)", "Spectrogram - One Feet Eyes Closed (1 s segments)"]
    axes = []
    max_ = 0
    min_ = 100
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            if data[i][3][j][5][0] > max_:
                max_ = data[i][3][j][5][0]
            if data[i][3][j][5][1] < min_:
                min_ = data[i][3][j][5][1]

    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])
        axes_=[]
        for j in range(0, len(data)):
            ax = f.add_subplot(2, 2, j + 1)
            ax, im = spectogram_plot(ax, data[i][3][j][1], data[i][3][j][2], data[i][3][j][3], title=data[i][2][1][j],
                                     no_colorbar=True, v=[min_, max_])
            axes_.append(ax)
        axes.append(axes_)
        cax = f.add_axes([0.91, 0.1, 0.02, 0.8])
        cbar = f.colorbar(im, cax=cax, ticks=range(int(min_), int(max_), 5))
        cbar.set_label('Power Spectral Density (dB)')
        plt.subplots_adjust(hspace=0.34, top=0.90, bottom=0.09, left=0.10, right=0.90, wspace=0.27)
    return axes

def psd_reports(data):
    title = ["PSD - Two Feet Eyes Open", "PSD - Two Feet Eyes Closed",
             "PSD - One Feet Eyes Open", "PSD - One Feet Eyes Closed"]
    axes = []
    for i in range(0, len(data)):
        f = plt.figure()
        plt.suptitle(title[i])
        axes1 = []
        axes2 = []
        for j in range(0, len(data)):
            ax1 = f.add_subplot(2, 4, j+1)
            PSD_plot(ax1, data[i][4][j][2], data[i][4][j][1], title=data[i][2][1][j])

            ax2 = f.add_subplot(2, 4, (j+5))
            PSD_plot(ax2, data[i][4][j][2], data[i][4][j][0], title=data[i][2][1][j],
                     y_label="Power Spectral Density (No dB)")

            axes1.append(ax1)
            axes2.append(ax2)

        axes.append(np.concatenate([axes1, axes2]))
    return axes
