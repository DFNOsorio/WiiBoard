from Calibration.calibration_loaders import *
from Calibration.printing_lib import *

import numpy as np


def load_12kg_corners(folder_path):
    raw_files = '/raw/Raw_12Kg_corner_'
    converted_files = '/converted/Converted_12Kg_corner_'

    f, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9 = grid()

    temp_end = 'dl.txt'
    [raw_12Kg_corner_dl_tl, raw_12Kg_corner_dl_tr, raw_12Kg_corner_dl_bl, raw_12Kg_corner_dl_br,
     raw_12Kg_corner_dl_time, raw_12Kg_corner_dl_tw, converted_12Kg_corner_dl_tl,
     converted_12Kg_corner_dl_tr, converted_12Kg_corner_dl_bl, converted_12Kg_corner_dl_br,
     converted_12Kg_corner_dl_time, converted_12Kg_corner_dl_tw, dl_figure, ax2, ax1] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax2, ax1],
                  title="Bottom Left Corner - 12Kg")

    converted = raw_to_kilos(raw_12Kg_corner_dl_bl, BOTTOM_LEFT)
    figure = subplot_overlap([converted_12Kg_corner_dl_time, converted_12Kg_corner_dl_time],
                    [[converted, converted_12Kg_corner_dl_bl], [np.array(converted_12Kg_corner_dl_bl) - np.array(converted)]],
                             title=['Weights', 'Difference'],
                             xlabel=["Time (s)", "Time (s)"],
                             ylabel=["Converted Values (Kg)", 'Weight Delta (Kg)'],
                             legend=[["Adjusted", "Recorded"], ["Difference"]],
                             lines=1, columns=2, fontsize=12)

    temp_end = 'dr.txt'
    [raw_12Kg_corner_dr_tl, raw_12Kg_corner_dr_tr, raw_12Kg_corner_dr_bl, raw_12Kg_corner_dr_br,
     raw_12Kg_corner_dr_time, raw_12Kg_corner_dr_tw, converted_12Kg_corner_dr_tl,
     converted_12Kg_corner_dr_tr, converted_12Kg_corner_dr_bl, converted_12Kg_corner_dr_br,
     converted_12Kg_corner_dr_time, converted_12Kg_corner_dr_tw, dr_figure, ax4, ax3] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax4, ax3],
                  title="Bottom Right Corner - 12Kg")

    temp_end = 'ul.txt'
    [raw_12Kg_corner_ul_tl, raw_12Kg_corner_ul_tr, raw_12Kg_corner_ul_bl, raw_12Kg_corner_ul_br,
     raw_12Kg_corner_ul_time, raw_12Kg_corner_ul_tw, converted_12Kg_corner_ul_tl,
     converted_12Kg_corner_ul_tr, converted_12Kg_corner_ul_bl, converted_12Kg_corner_ul_br,
     converted_12Kg_corner_ul_time, converted_12Kg_corner_ul_tw, ul_figure, ax6, ax5] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax6, ax5],
                  title="Upper Left Corner - 12Kg")

    temp_end = 'ur.txt'
    [raw_12Kg_corner_ur_tl, raw_12Kg_corner_ur_tr, raw_12Kg_corner_ur_bl, raw_12Kg_corner_ur_br,
     raw_12Kg_corner_ur_time, raw_12Kg_corner_ur_tw, converted_12Kg_corner_ur_tl,
     converted_12Kg_corner_ur_tr, converted_12Kg_corner_ur_bl, converted_12Kg_corner_ur_br,
     converted_12Kg_corner_ur_time, converted_12Kg_corner_ur_tw, ur_figure, ax8, ax7] = \
        load_file(folder_path + raw_files + temp_end, folder_path + converted_files + temp_end, [ax8, ax7],
                  title="Upper Right Corner - 12Kg")

    dl_max_mean = np.mean(converted_12Kg_corner_dl_tw[-200:])
    dr_max_mean = np.mean(converted_12Kg_corner_dr_tw[-200:])
    ul_max_mean = np.mean(converted_12Kg_corner_ul_tw[-200:])
    ur_max_mean = np.mean(converted_12Kg_corner_ur_tw[-200:])

    temp_data = [[converted_12Kg_corner_dl_time, converted_12Kg_corner_dr_time, converted_12Kg_corner_ul_time, converted_12Kg_corner_ur_time],
                 [converted_12Kg_corner_dl_tw, converted_12Kg_corner_dr_tw, converted_12Kg_corner_ul_tw, converted_12Kg_corner_ur_tw],
                 "Time(s)", "Total weight (Kg)",  "Total weight (Kg)",
                 ["BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_LEFT", "TOP_RIGHT"],
                 'BOTTOM_LEFT max: ' + str(dl_max_mean) + ' Kg \nBOTTOM_RIGHT max: ' + str(dr_max_mean) +
                 ' Kg \nTOP_LEFT max: ' + str(ul_max_mean) + ' Kg \nTOP_RIGHT max: ' + str(ur_max_mean) + ' Kg']

    ax9 = ax9_populator(temp_data, ax9)

    plot_show_all()


def load_12kg(folder_path):
    load_12kg_corners(folder_path)

def load_center(cut_index, folder_name):

    center_file(folder_name + '/raw/Raw_center.txt', folder_name + '/converted/Converted_center.txt',
                intervals_1, cumu_weight)
    center_file(folder_name + '/raw/Raw_center_2.txt', folder_name + '/converted/Converted_center_2.txt'
                , intervals_2, cumu_weight_2)

    plot_show_all()


folder_name = '../Calibration/data'
load_center(1, folder_name)
#load_12kg(folder_name)

