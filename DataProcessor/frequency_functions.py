import numpy as np
from matplotlib import mlab
from novainstrumentation.code.filter import bandpass


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
    Pxx, freqs, bins = mlab.specgram(x, Fs=fs, NFFT=window_size, noverlap=0, mode='psd')
    Pxx_dB = 10.0 * np.log10(Pxx)

    return Pxx, Pxx_dB, freqs, bins, [np.max(Pxx), np.min(Pxx)], [np.max(Pxx_dB), np.min(Pxx_dB)]


def get_freq_stat(Pxx_dB, freqs, bins):
    mean_dB = []
    max_freq = []
    for i in range(0, len(bins)):
        mean_dB.append(np.mean(Pxx_dB[:, i]))
        max_freq.append(freqs[np.where(Pxx_dB[:, i] == np.max(Pxx_dB[:, i]))[0][0]])

    return mean_dB, max_freq


def get_psd(x, fs):
    Pxx, freqs = mlab.psd(x, Fs=fs)
    Pxx_dB = 10.0 * np.log10(Pxx)
    return Pxx, Pxx_dB, freqs


def filter_signal_band(data_vector, frequencies, order=2, fs=1000):
    return bandpass(data_vector, frequencies[0], frequencies[1], order, fs)


