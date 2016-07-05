from datetime import datetime

from DataProcessor.NOVAOpenSignals import *


def load_open_trial(name_of_file, wii_time0):
    time, date, sampling_rate, labels, data_points, columns = file_scrapper(name_of_file+'.txt')

    date_time = date + "T" + time + "Z"
    utc_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds() - 3600  # TimeZone
    initial_delta = epoch_time - wii_time0

    open_time = time_vector_creator(float(sampling_rate), 0, len(data_points))
    EMG, ACC, ECG, EMG_labels, ACC_labels, ECG_labels = data_characterize(data_points, labels, columns)

    return EMG, ACC, ECG, EMG_labels, ACC_labels, ECG_labels, open_time, initial_delta
