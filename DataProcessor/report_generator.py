from DataProcessor.printing.printing_lib import *


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


#def spectrogram_report