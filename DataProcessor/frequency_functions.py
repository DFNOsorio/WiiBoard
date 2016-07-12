import numpy as np
from matplotlib import mlab


def fft(x, fs, filtered=True):

    n = len(x)
    t = n*1.0/fs
    k = np.arange(n)
    freq = k*1.0/t
    freq_plot = freq[range(n/2)]

    y = np.fft.fft(x)/(n*1.0)
    y = y[range(n/2)]

    if filtered:
        y[0] = 0

    return [freq_plot, y]


def get_spectrogram_no_plot(x, fs, window_size):
    Pxx, freqs, bins = mlab.specgram(x, Fs=fs, NFFT=window_size, noverlap=0)
    Pxx_dB = 10 * np.log10(Pxx)

    return Pxx, Pxx_dB, freqs, bins

