import numpy as np


def file_scrapper(name_of_file):
    data = open(name_of_file)
    lines = data.readlines()

    h = lines[1].split(': ')
    address = h[0].split('# {')[1].split('"')[1]
    type = list_filler(h[2])
    device_name = simple_cleaner(h[3])
    columns = list_filler(h[4])
    sync_interval = simple_cleaner(h[5], text=False)
    time = simple_cleaner(h[6])
    comments = simple_cleaner(h[7])
    device_connection = simple_cleaner(h[8])
    channels = list_filler(h[9], text=False)
    date = simple_cleaner(h[10])
    mode = simple_cleaner(h[11], text=False)
    digital = list_filler(h[12], text=False)
    firmware = simple_cleaner(h[13], text=False)
    device = simple_cleaner(h[14])
    position = simple_cleaner(h[15], text=False)
    sampling_rate = simple_cleaner(h[16], text=False)
    labels = list_filler(h[17])
    resolution = list_filler(h[18], text=False)
    special = list_filler(h[19], text=False)

    data_points = data_scrapper(lines)

    return time, date, sampling_rate, labels, data_points, type


def list_filler(to_be_list, text=True):
    if text:
        output_ = to_be_list.split('], ')[0].split("[")[1].split('", "')
        output = []
        [[output.append(output_[i])] for i in range(0, len(output_))]
        output[0] = output[0].split('"')[1]
        output[-1] = output[-1].split('"')[0]
    else:
        output_ = to_be_list.split('], ')[0].split("[")[1].split(', ')
        output = []
        [[output.append(output_[i])] for i in range(0, len(output_))]
    return output


def simple_cleaner(to_be_clean, text=True):
    if text:
        output = to_be_clean.split('", "')[0].split('"')[1]
    else:
        output = to_be_clean.split(', "')[0]
    return output


def data_scrapper(lines):
    output = []
    for i in lines[3:-1]:
        temp = i.split(' ')[0].split("\t")
        temp_ = []
        for t in range(2, len(temp)-1):
            temp_.append(float(temp[t]))
        output.append(temp_)
    return np.array(output)


def time_vector_creator(sampling_rate, initial_time, length):
    output = [initial_time]
    for i in range(1, length):
        output.append(output[-1] + 1.0/(sampling_rate*1.0))
    return output


def data_characterize_all(data_points, labels, columns):
    EMG = []
    EMG_labels= []
    ACC = []
    ACC_labels = []
    ECG = []
    ECG_labels = []

    for i in range(0, len(columns)):

        if columns[i] == "EMG":
            EMG.append(data_points[:, i])
            EMG_labels.append(labels[i])
        elif columns[i] == "XYZ":
            ACC.append(data_points[:, i])
            ACC_labels.append(labels[i])
        elif columns[i] == "ECG":
            ECG.append(data_points[:, i])
            ECG_labels.append(labels[i])
    return EMG, ACC, ECG, EMG_labels, ACC_labels, ECG_labels


def data_characterize_rest(data_points, labels, columns):
    EMG = []
    EMG_labels = []
    EMG_means = []

    for i in range(0, len(columns)):
        if columns[i] == "EMG":
            EMG.append(data_points[:, i])
            EMG_labels.append(labels[i])
            EMG_means.append(np.mean(data_points[:, i]))

    return EMG, EMG_labels, EMG_means


