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


def load_file(complete_raw_path, complete_converted_path, axes, intervals, title="Plots"):

    [rtl, rtr, rbl, rbr, rt, rtw] = file_reader(complete_raw_path)
    [ctl, ctr, cbl, cbr, ct, ctw] = file_reader(complete_converted_path)

    rt = time_reshape(rt)
    ct = time_reshape(ct)

    figure, i_axes = subplot_overlap([rt, ct, ct], [[rtl, rtr, rbl, rbr], [ctl, ctr, cbl, cbr], [ctw]],
                             title=['Raw files', 'Converted files', 'Total weight'],
                             xlabel=["Time (s)", "Time (s)", "Time (s)"],
                             ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                             legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOTAL"]],
                             lines=1, columns=3, fontsize=12)

    figure = add_sup_title(figure, title, fontsize=14)

    means_raw = interval_means(intervals, [rtr, rbr, rtl, rbl])
    means_converted = interval_means(intervals, [ctr, cbr, ctl, cbl])
    means_tw = interval_means(intervals, [ctw])

    i_axes = add_hlines(i_axes, intervals, [means_raw, means_converted, means_tw], rt, linecolor='y')
    temp_axes = add_hlines([i_axes[2]], intervals, [[12.6]], rt, linecolor='g', legendText="CORR WEIGHT")
    i_axes[2] = temp_axes[0]

    [converted_tl, converted_tr, converted_bl, converted_br] = all_2_kilo([rtl, rtr, rbl, rbr],
                                                                          [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT,
                                                                           BOTTOM_RIGHT],
                                                                          calibration_matrix_adjusted)

    tw_c = weight_sum(ctl, ctr, cbl, cbr)
    tw_r = weight_sum(converted_tl, converted_tr, converted_bl, converted_br)

    figure, axes = subplot_overlap([ct, ct, ct], [[converted_tl, converted_tr, converted_bl, converted_br],
                                                  [ctl, ctr, cbl, cbr], [ctw, tw_c, tw_r]],
                                   title=['Internal Conversion', 'Wii Conversion', 'Total weight'],
                                   xlabel=["Time (s)", "Time (s)", "Time (s)"],
                                   ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                                   legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                           ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                           ["TOTAL", "CORNER SUM", "RAW SUM"]],
                                   lines=1, columns=3, fontsize=12)

    means_twc = interval_means(intervals, [tw_r])
    means_left_top = interval_means(intervals, [converted_tl])
    means_left_bottom = interval_means(intervals, [converted_bl])

    temp_axes = add_hlines([axes[2]], intervals, [[12.6]], rt, linecolor='g', legendText="CORR WEIGHT")
    axes[2] = temp_axes[0]
    temp_axes = add_hlines([axes[2]], intervals, [means_twc], rt, linecolor='y', legendText="INT MEAN WEIGHT")
    axes[2] = temp_axes[0]

    wd = weight_difference([[12.6]], means_twc)
    ld = weight_difference(means_left_bottom, means_left_top)


    #data1 = [rt, [rtl, rtr, rbl, rbr], "Time(s)", "Raw values",  "Raw " + title,
    #         ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]]
    #data2 = [ct, [ctl, ctr, cbl, cbr], "Time (s)", "Converted Values (Kg)", 'Converted files',
    #         ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]]

    #axis1 = axe_populator(data1, axes[0])
    #axis2 = axe_populator(data2, axes[1])

    return [rtl, rtr, rbl, rbr, rt, rtw, ctl, ctr, cbl, cbr, ct, ctw, figure, axes[0], axes[1]]


def calibration_file(complete_raw_path, complete_converted_path, intervals, cumu_weights, file_name=[]):

    [rtl, rtr, rbl, rbr, rt, rtw] = file_reader(complete_raw_path)
    [ctl, ctr, cbl, cbr, ct, ctw] = file_reader(complete_converted_path)
    rt = time_reshape(rt)
    ct = time_reshape(ct)

    figure, axes = subplot_overlap([rt, ct, ct], [[rtl, rtr, rbl, rbr], [ctl, ctr, cbl, cbr], [ctw]],
                                   title=['Raw files', 'Converted files', 'Total weight'],
                                   xlabel=["Time (s)", "Time (s)", "Time (s)"],
                                   ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                                   legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                           ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                           ["TOTAL"]],
                                   lines=1, columns=3, fontsize=12)
    figure = add_sup_title(figure, file_name, fontsize=14)
    zero_out([rtr[intervals[0][0]:intervals[0][1]], rbr[intervals[0][0]:intervals[0][1]],
             rtl[intervals[0][0]:intervals[0][1]], rbl[intervals[0][0]:intervals[0][1]]])


    means_raw = interval_means(intervals, [rtr, rbr, rtl, rbl])
    means_converted = interval_means(intervals, [ctr, cbr, ctl, cbl])
    means_tw = interval_means(intervals, [ctw])

    #axes = add_vlines(axes, intervals_1, [max([max(rtl), max(rtr), max(rbl), max(rbr)]),
    #                                      max([max(ctl), max(ctr), max(cbl), max(cbr)]), max(ctw)], rt)

    axes = add_hlines(axes, intervals, [means_raw, means_converted, means_tw], rt, linecolor='y')
    temp_axes = add_hlines([axes[2]], intervals, [cumu_weights], rt, linecolor='g', legendText="CORR WEIGHT")
    axes[2] = temp_axes[0]

    [converted_tl, converted_tr, converted_bl, converted_br] = all_2_kilo([rtl, rtr, rbl, rbr],
                                                               [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT],
                                                               calibration_matrix_adjusted)

    tw_c = weight_sum(ctl, ctr, cbl, cbr)
    tw_r = weight_sum(converted_tl, converted_tr, converted_bl, converted_br)

    figure, axes = subplot_overlap([ct, ct, ct], [[converted_tl, converted_tr, converted_bl, converted_br],
                                                  [ctl, ctr, cbl, cbr], [ctw, tw_c, tw_r]],
                                   title=['Internal Conversion', 'Wii Conversion', 'Total weight'],
                                   xlabel=["Time (s)", "Time (s)", "Time (s)"],
                                   ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                                   legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                           ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                           ["TOTAL", "CORNER SUM", "RAW SUM"]],
                                   lines=1, columns=3, fontsize=12)
    figure = add_sup_title(figure, file_name, fontsize=14)
    means_twc = interval_means(intervals, [tw_r])
    means_left_top = interval_means(intervals, [converted_tl])
    means_left_bottom = interval_means(intervals, [converted_bl])

    temp_axes = add_hlines([axes[2]], intervals, [cumu_weights], rt, linecolor='g', legendText="CORR WEIGHT")
    axes[2] = temp_axes[0]
    temp_axes = add_hlines([axes[2]], intervals, [means_twc], rt, linecolor='y', legendText="INT MEAN WEIGHT")
    axes[2] = temp_axes[0]


    wd = weight_difference(cumu_weights, means_twc)
    ld = weight_difference(means_left_bottom, means_left_top)

    figure, axes = subplot_overlap([cumu_weights, cumu_weights, cumu_weights], [[wd], [np.abs(ld)], [wd, np.abs(ld)]],
                                   title=['Total Weight Difference', 'Left Sensor Differences', 'Total vs Left'],
                                   xlabel=["Weight (kg)", "Weight (kg)", "Weight (kg)"],
                                   ylabel=["Weight Difference (Kg)", "Weight Difference (Kg)", 'Weight Difference (Kg)'],
                                   legend=[['Total Weight Difference'],
                                           ['Left Sensor Differences'],
                                           ['Total Weight Difference', 'Left Sensor Differences']],
                                   lines=1, columns=3, fontsize=12)
    figure = add_sup_title(figure, file_name, fontsize=14)

