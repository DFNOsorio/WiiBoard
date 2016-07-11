import numpy as np


def getFS(time):
    return 1.0 / np.mean(np.diff(time))


def maxSwayEachAxis(COPx, COPy):
    return([[COPx[np.argmax(COPx)],COPy[np.argmax(COPx)]],
            [COPx[np.argmin(COPx)],COPy[np.argmin(COPx)]],
            [COPx[np.argmax(COPy)],COPy[np.argmax(COPy)]],
            [COPx[np.argmin(COPy)],COPy[np.argmin(COPy)]]])