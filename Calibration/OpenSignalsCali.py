from Calibration.calibration_loaders import *
from Calibration.OpenSignalsScrapper import *
from Calibration.calibration_processing import *
from Calibration.printing_lib import *
from datetime import datetime


def get_values(path, run_number):
    [tl, tr, bl, br, time_, events, event_time] = file_reader(path + 'ACC_' + str(run_number) + '.txt')
    time_open, date, sampling_rate, labels, data_points = file_scrapper(path + 'acc_'+ str(run_number) + '.txt')
    time, new_indexes, events = data_cleaner(time_, [events])
    events = events[0]

    events = np.array(events) * max(data_points[:, 2])

    date_time = date + "T" + time_open + "Z"
    utc_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds() - 3600  # TimeZone

    time_reshaped = time_reshape(time)
    time_ = time_reshape(time_)
    initial_delta = epoch_time - time[0]

    open_time = time_vector_creator(float(sampling_rate), initial_delta, len(data_points))

    return open_time, time, time_reshaped, events, event_time, data_points, labels, initial_delta, time_


def get_window(points, timeWii, timeOpen, event, window_size=50):

    peak_index = np.where(points[:, 2] == max(points[:, 2]))[0][0]

    td = timeOpen[peak_index] - (event - timeWii[0])

    event_time_index = np.where(np.array(timeWii) > event)[0][0]

    window_events = range(event_time_index-window_size, event_time_index+window_size)
    window_open = range(peak_index-window_size, peak_index+window_size)

    return peak_index, td, event_time_index, window_events, window_open


def td_manual(timeOpen_value, timeWii, event):
    td = timeOpen_value - (event - timeWii[0])
    return td


def window_converter(data, window):
    return np.array(data)[window]


def data_cleaner(points, other):
    output = []
    differences = np.diff(points)
    for i in range(0, len(differences)):
        if differences[i] != 0:
            output.append(i)
    output_ = []

    for i in other:
        output_.append(list(np.array(i)[output]))
    return list(np.array(points)[output]), output, output_


def time_alignment(time_vector, td):
    return np.array(time_vector) + td

folder_name = '../Calibration/data/open_signals/'


open_time_1, time_1, time_reshaped_1, events_1, event_time_1, data_points_1, labels_1, initial_delta_1, time_1_ = get_values(folder_name, 1)
open_time_2, time_2, time_reshaped_2, events_2, event_time_2, data_points_2, labels_2, initial_delta_2, time_2_ = get_values(folder_name, 2)
open_time_3, time_3, time_reshaped_3, events_3, event_time_3, data_points_3, labels_3, initial_delta_3, time_3_ = get_values(folder_name, 3)
open_time_4, time_4, time_reshaped_4, events_4, event_time_4, data_points_4, labels_4, initial_delta_4, time_4_ = get_values(folder_name, 4)
open_time_5, time_5, time_reshaped_5, events_5, event_time_5, data_points_5, labels_5, initial_delta_5, time_5_ = get_values(folder_name, 5)

figure, axes = subplot_overlap([[open_time_1, open_time_1, open_time_1, time_reshaped_1],
                 [open_time_2, open_time_2, open_time_2, time_reshaped_2],
                 [open_time_3, open_time_3, open_time_3, time_reshaped_3],
                 [open_time_4, open_time_4, open_time_4, time_reshaped_4]],
                [[data_points_1[:, 2], data_points_1[:, 3], data_points_1[:, 4], events_1],
                 [data_points_2[:, 2], data_points_2[:, 3], data_points_2[:, 4], events_2],
                 [data_points_3[:, 2], data_points_3[:, 3], data_points_3[:, 4], events_3],
                 [data_points_4[:, 2], data_points_4[:, 3], data_points_4[:, 4], events_4]],
                ["RUN1", "RUN2", "RUN3", "RUN4"],
                ["Time(s)", "Time(s)", "Time(s)", "Time(s)"], ["Value", "Value", "Value", "Value"], 2, 2,
                legend=[np.concatenate([labels_1, ["Events"]]), np.concatenate([labels_2, ["Events"]]),
                np.concatenate([labels_3, ["Events"]]), np.concatenate([labels_4, ["Events"]])],
                overlapx=True)

add_sup_title(figure, "Signals")

peak_index_1, td_1, event_time_index_1, window_event_1, window_open_1 = get_window(data_points_1, time_1, open_time_1, event_time_1)
peak_index_2, td_2, event_time_index_2, window_event_2, window_open_2 = get_window(data_points_2, time_2, open_time_2, event_time_2)
peak_index_3, td_3, event_time_index_3, window_event_3, window_open_3 = get_window(data_points_3, time_3, open_time_3, event_time_3)
peak_index_4, td_4, event_time_index_4, window_event_4, window_open_4 = get_window(data_points_4, time_4, open_time_4, event_time_4)
peak_index_5, td_5, event_time_index_5, window_event_5, window_open_5 = get_window(data_points_5, time_5, open_time_5, event_time_5)

figure, axes = subplot_overlap([[window_converter(open_time_1, window_open_1), window_converter(open_time_1, window_open_1),
                  window_converter(open_time_1, window_open_1), window_converter(time_reshaped_1, window_event_1)],
                 [window_converter(open_time_2, window_open_2), window_converter(open_time_2, window_open_2),
                  window_converter(open_time_2, window_open_2), window_converter(time_reshaped_2, window_event_2)],
                 [window_converter(open_time_3, window_open_3), window_converter(open_time_3, window_open_3),
                  window_converter(open_time_3, window_open_3), window_converter(time_reshaped_3, window_event_3)],
                 [window_converter(open_time_4, window_open_4), window_converter(open_time_4, window_open_4),
                  window_converter(open_time_4, window_open_4), window_converter(time_reshaped_4, window_event_4)],
                  [window_converter(open_time_5, window_open_5), window_converter(open_time_5, window_open_5),
                   window_converter(open_time_5, window_open_5), window_converter(time_reshaped_5, window_event_5)]],
                [[window_converter(data_points_1[:, 2], window_open_1), window_converter(data_points_1[:, 3], window_open_1),
                  window_converter(data_points_1[:, 4], window_open_1), window_converter(events_1, window_event_1)],
                 [window_converter(data_points_2[:, 2], window_open_2), window_converter(data_points_2[:, 3], window_open_2),
                  window_converter(data_points_2[:, 4], window_open_2), window_converter(events_2, window_event_2)],
                 [window_converter(data_points_3[:, 2], window_open_3), window_converter(data_points_3[:, 3], window_open_3),
                  window_converter(data_points_3[:, 4], window_open_3), window_converter(events_3, window_event_3)],
                 [window_converter(data_points_4[:, 2], window_open_4), window_converter(data_points_4[:, 3], window_open_4),
                  window_converter(data_points_4[:, 4], window_open_4), window_converter(events_4, window_event_4)],
                 [window_converter(data_points_5[:, 2], window_open_5), window_converter(data_points_5[:, 3], window_open_5),
                  window_converter(data_points_5[:, 4], window_open_5), window_converter(events_5, window_event_5)]
                 ],
                ["RUN1 - TD = " + str(td_1), "RUN2 - TD = " + str(td_2),
                 "RUN3 - TD = " + str(td_3), "RUN4 - TD = " + str(td_4), "RUN5 - TD = " + str(td_5)],
                ["Time(s)", "Time(s)", "Time(s)", "Time(s)", "Time(s)"], ["Value", "Value", "Value", "Value", "Value"], 3, 2,
                legend=[np.concatenate([labels_1, ["Events"]]), np.concatenate([labels_2, ["Events"]]),
                        np.concatenate([labels_3, ["Events"]]), np.concatenate([labels_4, ["Events"]]),
                        np.concatenate([labels_5, ["Events"]])],
                overlapx=True)

add_sup_title(figure, "Signals, zoomed in")


figure, axes = subplot_overlap([range(0, len(np.diff(time_reshaped_1))), range(0, len(np.diff(time_reshaped_2))),
                 range(0, len(np.diff(time_reshaped_3))), range(0, len(np.diff(time_reshaped_4)))],
                [[1.0/np.diff(time_reshaped_1)], [1.0/np.diff(time_reshaped_2)], [1.0/np.diff(time_reshaped_3)],
                 [1.0/np.diff(time_reshaped_4)]],
                ["RUN1", "RUN2", "RUN3", "RUN4"],
                ["Time(s)", "Time(s)", "Time(s)", "Time(s)"], ["Value", "Value", "Value", "Value"], 2, 2,
                legend=[])
add_sup_title(figure, "Sampling Frequency")


manual_1 = td_manual(3.619, time_1, event_time_1)
manual_2 = td_manual(0.983, time_2, event_time_2)
manual_3 = td_manual(1.235, time_3, event_time_3)
manual_4 = td_manual(2.907, time_4, event_time_4)
manual_5 = td_manual(1.542, time_5, event_time_5)

figure, axes = subplot_overlap([[open_time_1, open_time_1, open_time_1, time_reshaped_1,
                                 time_alignment(time_reshaped_1, td_1), time_alignment(time_reshaped_1, manual_1)],
                                [open_time_2, open_time_2, open_time_2, time_reshaped_2,
                                 time_alignment(time_reshaped_2, td_2), time_alignment(time_reshaped_2, manual_2)],
                                [open_time_3, open_time_3, open_time_3, time_reshaped_3,
                                 time_alignment(time_reshaped_3, td_3), time_alignment(time_reshaped_3, manual_3)],
                                [open_time_4, open_time_4, open_time_4, time_reshaped_4,
                                 time_alignment(time_reshaped_4, td_4), time_alignment(time_reshaped_4, manual_4)]],
                               [[data_points_1[:, 2], data_points_1[:, 3], data_points_1[:, 4],
                                 events_1, events_1, events_1],
                                [data_points_2[:, 2], data_points_2[:, 3], data_points_2[:, 4]
                                    , events_2, events_2, events_2],
                                [data_points_3[:, 2], data_points_3[:, 3], data_points_3[:, 4]
                                    , events_3, events_3, events_3],
                                [data_points_4[:, 2], data_points_4[:, 3], data_points_4[:, 4]
                                    , events_4, events_4, events_4]],
                               ["RUN1", "RUN2", "RUN3", "RUN4"],
                               ["Time(s)", "Time(s)", "Time(s)", "Time(s)"], ["Value", "Value", "Value", "Value"], 2, 2,
                               legend=[np.concatenate([labels_1, ["Events", "Events (Auto)", "Events(Manual)"]]),
                                       np.concatenate([labels_2, ["Events", "Events (Auto)", "Events(Manual)"]]),
                                       np.concatenate([labels_3, ["Events", "Events (Auto)", "Events(Manual)"]]),
                                       np.concatenate([labels_4, ["Events", "Events (Auto)", "Events(Manual)"]])],
                               overlapx=True)

print "Automatic"
print "TD1 :" + str(td_1) + " TD2 :" + str(td_2) + " TD3 :" + str(td_3) + " TD4 :" + str(td_4) + " TD5 :" + str(td_5)
print "Manual"
print "TD1 :" + str(manual_1) + " TD2 :" + str(manual_2) + " TD3 :" + str(manual_3) + " TD4 :" + str(manual_4) + " TD5 :" + str(manual_5)
print "Pre duplicate removal"
print "Wii Sampling: " + str(1.0 / np.mean(np.diff(time_1_))) + " (1) " + str(1.0 / np.mean(np.diff(time_2_))) + " (2) " \
      + str(1.0 / np.mean(np.diff(time_3_))) + " (3) " + str(1.0 / np.mean(np.diff(time_4_))) + " (4) " + \
      str(1.0 / np.mean(np.diff(time_5_))) + " (5)"
print "Post duplicate removal"
print "Wii Sampling: " + str(1.0/np.mean(np.diff(time_reshaped_1))) + " (1) " + str(1.0/np.mean(np.diff(time_reshaped_2))) + " (2) " \
      + str(1.0/np.mean(np.diff(time_reshaped_3))) + " (3) " + str(1.0/np.mean(np.diff(time_reshaped_4))) + " (4) " +\
      str(1.0/np.mean(np.diff(time_reshaped_5))) + " (5)"
print "Open Signal Sampling: " + str(1.0/np.mean(np.diff(open_time_1)))



plot_show_all()


