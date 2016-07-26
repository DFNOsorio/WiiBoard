import numpy as np
from novainstrumentation import smooth


def integrated_EMG(EMG_window):
    # Generally, IEMG is used as an onset index to detect the muscle activity

    return sum(np.abs(np.array(EMG_window)))


def mean_absolute_value(EMG_window):
    EMG_len = len(EMG_window)
    return 1.0/EMG_len * integrated_EMG(EMG_window)


def energy_EMG(EMG_window):
    abs_array = np.abs(np.array(EMG_window))**2.0
    return np.sum(abs_array)


def variance(EMG_window):
    # Uses power since the EMG variance is close to 0
    EMG_len = len(EMG_window)

    return 1.0 / (EMG_len-1) * sum(np.array(EMG_window)**2)


def RMS_EMG(EMG_window):

    EMG_len = len(EMG_window)
    EMG_Power = np.array(EMG_window)**2

    return np.sqrt(1.0/EMG_len * sum(EMG_Power))


def emg_smoother(emg, window):
        return list(smooth(np.abs(np.array(emg)), window_len=window))
