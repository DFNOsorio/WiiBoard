import numpy as np

def getFS(time):
    return 1.0 / np.mean(np.diff(time))

def COPfft(COP,Fs,filtered = True):

    n = len(COP)
    T = n/Fs
    k = np.arange(n)
    freq = k/T
    freqPlot = freq[range(n/2)]

    Y = np.fft.fft(COP)/n
    Y = Y[range(n/2)]

    if (filtered):
        Y[0] = 0

    return [freqPlot, Y]


def maxSwayEachAxis(COPx,COPy):
    return([[COPx[np.argmax(COPx)],COPy[np.argmax(COPx)]],
            [COPx[np.argmin(COPx)],COPy[np.argmin(COPx)]],
            [COPx[np.argmax(COPy)],COPy[np.argmax(COPy)]],
            [COPx[np.argmin(COPy)],COPy[np.argmin(COPy)]]])