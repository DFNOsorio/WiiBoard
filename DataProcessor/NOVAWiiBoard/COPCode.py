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
    Vy = np.diff(COPy) / (np.diff(rt) * 1.0)

    V = np.sqrt(Vx**2.0 + Vy**2.0)

    Ax = np.diff(Vx) / (np.diff(rt[0:-1]) * 1.0)
    Ay = np.diff(Vy) / (np.diff(rt[0:-1]) * 1.0)

    A = np.sqrt(Ax**2.0 + Ay**2.0)

    Vx = list(np.array(Vx) / 1000.0)
    Vy = list(np.array(Vy) / 1000.0)
    V = list(np.array(V) / 1000.0)
    Ax = list(np.array(Ax) / 1000000.0)
    Ay = list(np.array(Ay) / 1000000.0)
    A = list(np.array(A) / 1000000.0)

    return [Vx, Vy, V, Ax, Ay, A]


def motion_equations(COPx, COPy, rt):
    Vx = [0]
    Vy = [0]
    V = [0]
    Ax = [0]
    Ay =[0]
    A = [0]
    instVx = np.diff(COPx) / (np.diff(rt) * 1.0)
    instVy = np.diff(COPy) / (np.diff(rt) * 1.0)

    return [np.array(instVx) / 1000.0, np.array(instVy) / 1000.0, rt]


def motion_equations_(COPx, COPy, rt):
    Vx = [0]
    Vy = [0]
    V = [0]
    Ax = [0]
    Ay =[0]
    A = [0]
    instVx = np.diff(COPx) / (np.diff(rt) * 1.0)
    instVy = np.diff(COPy) / (np.diff(rt) * 1.0)

    for i in range(0, len(instVx)):
        Vx.append(Vx[-1] + instVx[i])
        Vy.append(Vy[-1] + instVy[i])

        instV = np.sqrt(instVx[i] ** 2.0 + instVy[i] ** 2.0)

        angle = get_angle([Vx[-2], Vx[-1]], [Vy[-2], Vy[-1]])

        if angle < 90 or angle > 270:
            V.append(V[-1]+instV)
        else:
            V.append(V[-1]-instV)

    instAx = np.diff(Vx) / (np.diff(rt) * 1.0)
    instAy = np.diff(Vy) / (np.diff(rt) * 1.0)

    for i in range(0, len(instAx)):
        Ax.append(Ax[-1] + instAx[i])
        Ay.append(Ay[-1] + instAy[i])

        instA = np.sqrt(instAx[i] ** 2.0 + instAy[i] ** 2.0)

        angle = get_angle([Ax[-2], Ax[-1]], [Ay[-2], Ay[-1]])
        if angle < 90 or angle > 270:
            A.append(V[-1] + instA)
        else:
            A.append(V[-1] - instA)

    Vx = list(np.array(Vx)/1000.0)
    Vy = list(np.array(Vy) / 1000.0)
    V = list(np.array(V) / 1000.0)
    Ax = list(np.array(Ax) / 1000000.0)
    Ay = list(np.array(Ay) / 1000000.0)
    A = list(np.array(A) / 1000000.0)

    return [Vx, Vy, V, Ax, Ay, A]


def get_angle(x, y):
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    rads = atan2(-dy, dx)
    rads %= 2.0*pi
    degs = degrees(rads)

    return degs



