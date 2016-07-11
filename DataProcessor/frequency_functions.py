import numpy as np


def fft(x, fs, filtered=True):

    n = len(x)
    t = n*1.0/fs
    k = np.arange(n)
    freq = k*1.0/t
    freq_plot = freq[range(n/2)]

    y = np.fft.fft(x)/(n*1.0)
    y = y[range(n/2)]

    if (filtered):
        y[0] = 0

    return [freq_plot, y]
