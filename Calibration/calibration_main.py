from Calibration.printing_lib import *
import numpy as np

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


def time_reshape(time_vector):

    return list(np.array(time_vector) - time_vector[0])


def load_file(complete_raw_path, complete_converted_path, axes, title="Plots", show_plot=False):

    [rtl, rtr, rbl, rbr, rt, rtw] = file_reader(complete_raw_path)
    [ctl, ctr, cbl, cbr, ct, ctw] = file_reader(complete_converted_path)

    rt = time_reshape(rt)
    ct = time_reshape(ct)

    figure = subplot_overlap([rt, ct, ct], [[rtl, rtr, rbl, rbr], [ctl, ctr, cbl, cbr], [ctw]],
                             title=['Raw files', 'Converted files', 'Total weight'],
                             xlabel=["Time (epochs)", "Time (s)", "Time (s)"],
                             ylabel=["Raw values", "Converted Values (Kg)", 'Total weight (Kg)'],
                             legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                                     ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "TOTAL"],
                                     ["TOTAL"]],
                             lines=1, columns=3, fontsize=12)

    figure = add_sup_title(figure, title, fontsize=14)
    if show_plot:
        plot_show(figure)
    http: // nellev.github.io / tmp / jhepc / gallery.html
    return [rtl, rtr, rbl, rbr, rt, rtw, ctl, ctr, cbl, cbr, ct, ctw, figure, axis1, axis2, axis3]


def load_12kg_corners(folder_path):
    raw_files = '/raw/Raw_12Kg_corner_'
    converted_files = '/converted/Converted_12Kg_corner_'

    f, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13 = grid()

    temp_end = 'dl.txt'
    [raw_12Kg_corner_dl_tl, raw_12Kg_corner_dl_tr, raw_12Kg_corner_dl_bl, raw_12Kg_corner_dl_br,
     raw_12Kg_corner_dl_time, raw_12Kg_corner_dl_tw, converted_12Kg_corner_dl_tl,
     converted_12Kg_corner_dl_tr, converted_12Kg_corner_dl_bl, converted_12Kg_corner_dl_br,
     converted_12Kg_corner_dl_time, converted_12Kg_corner_dl_tw, dl_figure, ax9, ax8, ax7] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax3, ax2, ax1],
                  title="Bottom Left Corner - 12Kg", show_plot=False)

    temp_end = 'dr.txt'
    [raw_12Kg_corner_dr_tl, raw_12Kg_corner_dr_tr, raw_12Kg_corner_dr_bl, raw_12Kg_corner_dr_br,
     raw_12Kg_corner_dr_time, raw_12Kg_corner_dr_tw, converted_12Kg_corner_dr_tl,
     converted_12Kg_corner_dr_tr, converted_12Kg_corner_dr_bl, converted_12Kg_corner_dr_br,
     converted_12Kg_corner_dr_time, converted_12Kg_corner_dr_tw, dr_figure, ax9, ax8, ax7] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax6, ax5, ax4],
                  title="Bottom Right Corner - 12Kg", show_plot=False)

    temp_end = 'ul.txt'
    [raw_12Kg_corner_ul_tl, raw_12Kg_corner_ul_tr, raw_12Kg_corner_ul_bl, raw_12Kg_corner_ul_br,
     raw_12Kg_corner_ul_time, raw_12Kg_corner_ul_tw, converted_12Kg_corner_ul_tl,
     converted_12Kg_corner_ul_tr, converted_12Kg_corner_ul_bl, converted_12Kg_corner_ul_br,
     converted_12Kg_corner_ul_time, converted_12Kg_corner_ul_tw, ul_figure, ax9, ax8, ax7] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax9, ax8, ax7],
                  title="Upper Left Corner - 12Kg", show_plot=False)

    temp_end = 'ur.txt'
    [raw_12Kg_corner_ur_tl, raw_12Kg_corner_ur_tr, raw_12Kg_corner_ur_bl, raw_12Kg_corner_ur_br,
     raw_12Kg_corner_ur_time, raw_12Kg_corner_ur_tw, converted_12Kg_corner_ur_tl,
     converted_12Kg_corner_ur_tr, converted_12Kg_corner_ur_bl, converted_12Kg_corner_ur_br,
     converted_12Kg_corner_ur_time, converted_12Kg_corner_ur_tw, ur_figure, ax12, ax11, ax10] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax12, ax11, ax10],
                  title="Upper Right Corner - 12Kg", show_plot=False)


    temp_data = [[converted_12Kg_corner_dl_time, converted_12Kg_corner_dr_time, converted_12Kg_corner_ul_time, converted_12Kg_corner_ur_time],
                 [converted_12Kg_corner_dl_tw, converted_12Kg_corner_dr_tw, converted_12Kg_corner_ul_tw, converted_12Kg_corner_ur_tw],
                 "Time(s)", "Total weight (Kg)",  "Total weight (Kg)", ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"],
                 'TOP_LEFT max: \nTOP_RIGHT max: \nBOTTOM_LEFT max: \nBOTTOM_RIGHT max: ']

    ax13 = ax13_populator(temp_data, ax13)

    plot_show_all()




def load_12kg(folder_path):
    load_12kg_corners(folder_path)

folder_name = '../Calibration/data'
load_12kg(folder_name)
