import numpy as np
from processing_wii import converter
from math import atan2, degrees, pi

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
        tl = interval_data[i].get_variable("wii_data")[1]
        tr = interval_data[i].get_variable("wii_data")[2]
        bl = interval_data[i].get_variable("wii_data")[3]
        br = interval_data[i].get_variable("wii_data")[4]
        [ctl, ctr, cbl, cbr] = converter(tl, tr, bl, br)
        new_cop = COP(ctl, ctr, cbl, cbr)
        montion = motion_equations(new_cop[0], new_cop[1])
        temp_ = []
        [[temp_.append(i)] for i in new_cop]
        [[temp_.append(i)] for i in montion]
        output.append(temp_)
    return [output[0], output[1], output[2], output[3]]


def motion_equations(COPx, COPy):

    instVx = np.diff(COPx) / (0.01 * 1.0)
    instVy = np.diff(COPy) / (0.01 * 1.0)

    Ax = np.diff(instVx) / (0.01 * 1.0)
    Ay = np.diff(instVy) / (0.01 * 1.0)

    return [np.array(instVx) / 1000.0, np.array(instVy) / 1000.0, np.array(Ax) / 1000000.0, np.array(Ay) / 1000000.0]





