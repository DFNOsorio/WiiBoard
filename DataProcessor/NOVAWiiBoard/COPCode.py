import numpy as np
from processing_wii import converter

def COP(TL, TR, BL, BR):

    '''
    :param TL: Top Left Corner
    :param TR: Top Right Corner
    :param BL: Bottom Left Corner
    :param BR: Bottom Right Corner
    :param L: Board Length
    :return: Center of Pressure (on the X and Y axis)

    Using equations 1 and 2 of the paper "Accuracy of force and center of pressure measures of the Wii Balance Board"
    by Harrison L.Bartlett (PUBMED ref: 23910725)
    '''

    COPx = []
    COPy = []

    L = 433.0
    W = 228.0

    for i in range(0, len(TL)):
        total_weight = TL[i] + TR[i] + BL[i] + BR[i]
        if total_weight > 0.2:
            COPx.append((L / 2.0) * ((TR[i] + BR[i]) - (TL[i] + BL[i])) / (total_weight * 1.0))
            COPy.append((W / 2.0) * ((TR[i] + TL[i]) - (BR[i] + BL[i])) / (total_weight * 1.0))
        else:
            COPx.append(0.0)
            COPy.append(0.0)

    return [COPx, COPy]


def interval_COPs(interval_data):
    output = []

    for i in range(0, 4):
        tl = interval_data[i][0][1]
        tr = interval_data[i][0][2]
        bl = interval_data[i][0][3]
        br = interval_data[i][0][4]
        [ctl, ctr, cbl, cbr] = converter(tl, tr, bl, br)
        new_cop = COP(ctl, ctr, cbl, cbr)
        output.append(new_cop)

    return [output[0], output[1], output[2], output[3]]


def velocity(COPx, COPy, rt):
    Vx = np.diff(COPx) / (np.diff(rt) * 1.0)
    Vy = np.array(COPy[1:]) - np.array(COPy[0:-1])/np.array(rt[1:]) - np.array(rt[0:-1])

    return Vx











