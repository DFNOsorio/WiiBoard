import numpy as np


def getFS(time):
    return 1.0 / np.mean(np.diff(time))


def maxSwayEachAxis(COPx, COPy):
    return([[COPx[np.argmax(COPx)],COPy[np.argmax(COPx)]],
            [COPx[np.argmin(COPx)],COPy[np.argmin(COPx)]],
            [COPx[np.argmax(COPy)],COPy[np.argmax(COPy)]],
            [COPx[np.argmin(COPy)],COPy[np.argmin(COPy)]]])


def v_and_a_stats(v, a):

    v_means = [np.mean(np.array(v[0])), np.mean(np.array(v[1]))]
    a_means = [np.mean(np.array(a[0])), np.mean(np.array(a[1]))]

    v_stds = [np.std(np.array(v[0])), np.std(np.array(v[1]))]
    a_stds = [np.std(np.array(a[0])), np.std(np.array(a[1]))]

    return [v_means, a_means, v_stds, a_stds]
