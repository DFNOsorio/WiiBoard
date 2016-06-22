from Calibration.calibration_processing import *
from Calibration.printing_lib import *


def file_reader(name_of_file):
    tl = []
    tr = []
    bl = []
    br = []
    tw = []
    time = []

    data = open(name_of_file)
    lines = data.readlines()[1:]

    for line in lines:
        temp_line = line.split(';')
        if len(temp_line) <= 5:
            tl.append(float(temp_line[0]))
            tr.append(float(temp_line[1]))
            bl.append(float(temp_line[2]))
            br.append(float(temp_line[3]))
            time.append(float(temp_line[4]))
        else:
            tl.append(float(temp_line[0]))
            tr.append(float(temp_line[1]))
            bl.append(float(temp_line[2]))
            br.append(float(temp_line[3]))
            tw.append(float(temp_line[4]))
            time.append(float(temp_line[5]))

    return [tl, tr, bl, br, time, tw]


def load_file(complete_raw_path, complete_converted_path, axes, title="Plots"):

    [rtl, rtr, rbl, rbr, rt, rtw] = file_reader(complete_raw_path)
    [ctl, ctr, cbl, cbr, ct, ctw] = file_reader(complete_converted_path)

    rt = time_reshape(rt)
    ct = time_reshape(ct)

    figure = subplot_overlap([rt, ct, ct], [[rtl, rtr, rbl, rbr], [ctl, ctr, cbl, cbr], [ctw]],
                             title=['Raw files', 'Converted files', 'Total weight'],
                             xlabel=["Time (s)", "Time (s)", "Time (s)"],
                             ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                             legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOTAL"]],
                             lines=1, columns=3, fontsize=12)

    figure = add_sup_title(figure, title, fontsize=14)

    data1 = [rt, [rtl, rtr, rbl, rbr], "Time(s)", "Raw values",  "Raw " + title,
             ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]]
    data2 = [ct, [ctl, ctr, cbl, cbr], "Time (s)", "Converted Values (Kg)", 'Converted files',
             ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]]

    axis1 = axe_populator(data1, axes[0])
    axis2 = axe_populator(data2, axes[1])

    return [rtl, rtr, rbl, rbr, rt, rtw, ctl, ctr, cbl, cbr, ct, ctw, figure, axis1, axis2]


def zero_files(complete_raw_path):
    [tl, tr, bl, br, t, tw] = file_reader(complete_raw_path)
    zero_out([tr, br, tl, bl])


def center_file(complete_raw_path, complete_converted_path):
    [rtl, rtr, rbl, rbr, rt, rtw] = file_reader(complete_raw_path)
    [ctl, ctr, cbl, cbr, ct, ctw] = file_reader(complete_converted_path)

    rt = time_reshape(rt)
    ct = time_reshape(ct)

    means_raw = interval_means(intervals_1, [rtr, rbr, rtl, rbl])
    means_converted = interval_means(intervals_1, [ctr, cbr, ctl, cbl])
    means_tw = interval_means(intervals_1, [ctw])

    figure, axes = subplot_overlap([rt, ct, ct], [[rtl, rtr, rbl, rbr], [ctl, ctr, cbl, cbr], [ctw]],
                             title=['Raw files', 'Converted files', 'Total weight'],
                             xlabel=["Time (s)", "Time (s)", "Time (s)"],
                             ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                             legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOTAL"]],
                             lines=1, columns=3, fontsize=12)

    #axes = add_vlines(axes, intervals_1, [max([max(rtl), max(rtr), max(rbl), max(rbr)]),
    #                                      max([max(ctl), max(ctr), max(cbl), max(cbr)]), max(ctw)], rt)

    axes = add_hlines(axes, intervals_1, [means_raw, means_converted, means_tw], rt)

    print means_raw[0]
    print calibration_matrix_adjusted[0]
    print means_converted

