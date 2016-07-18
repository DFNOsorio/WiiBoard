from DataProcessor.Printing import *


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
    title_1 = [" - Two Feet Eyes Open (", " - Two Feet Eyes Closed (", " - One Feet Eyes Open (", " - One Feet Eyes Open ("]
    for i in range(0, len(data)):
        motion_report(patient, title_1[i] + str(round(data[i][0][0][-1] - data[i][0][0][0], 2)) + " s)",
                      data[i][0][6], data[i])


# def spectrogram_report(data):
#     # EMG1(test_1[3][0])
#     # EMG2(test_1[3][1])
#     # EMG2(test_1[3][2])
#     # EMG2(test_1[3][3])
#     f = plt.figure()
#     title = ["Spectrogram - Two Feet Eyes Open (1 s segments)", "Spectrogram - Two Feet Eyes Closed (1 s segments)",
#                "Spectrogram - One Feet Eyes Open (1 s segments)", "Spectrogram - One Feet Eyes Open (1 s segments)"]
#     axes = []
#     for i in range(0, len(data)):
#         ax1 = f.add_subplot(2, 2, i+1)
#         spectogram_plot(ax1, data[i][3][2][1], data[i][3][2][2], data[i][3][2][3], title=title[i])
#         axes.append(ax1)
#
#     return axes


# def psd_reports(data):
#     title = ["PSD - Two Feet Eyes Open", "PSD - Two Feet Eyes Closed",
#              "PSD - One Feet Eyes Open", "PSD - One Feet Eyes Open"]
#     f, gs1_ax, gs2_ax, gs3_ax, gs4_ax = grid_psd("test")
#
#     for i in range(0, len(data)):
#         ax1 = f1.add_subplot(2, 4, i+1)
#         PSD_plot(ax1, data[i][4][0][2], data[i][4][0][1], title=title[i])
#
#         ax2 = f1.add_subplot(2, 4, (i+5))
#         PSD_plot(ax2, data[i][4][0][2], data[i][4][0][0], title=title[i], y_label="Power Spectral Density (No dB)")
#
#         axes1.append(ax1)
#         axes2.append(ax2)
#
#     return axes