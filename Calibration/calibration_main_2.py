from Calibration.calibration_loaders import *
from Calibration.printing_lib import *

import numpy as np


def load_corners(folder_path):
    #calibration_file(folder_path + '/raw/calibrate_bl.txt', folder_path + '/converted/calibrate_bl.txt',
    #                 intervals_bl, cumu_weight_2, file_name="Bottom Left")

    #calibration_file(folder_path + '/raw/calibrate_br.txt', folder_path + '/converted/calibrate_br.txt',
    #                 intervals_br, cumu_weight_2, file_name="Bottom Right")

    #calibration_file(folder_path + '/raw/calibrate_tr.txt', folder_path + '/converted/calibrate_tr.txt',
    #                intervals_tr, cumu_weight_2, file_name="Top Right")

    calibration_file(folder_path + '/raw/calibrate_tl.txt', folder_path + '/converted/calibrate_tl.txt',
                     intervals_tl, cumu_weight_2, file_name="Top Left")


def load_center(folder_path):

    calibration_file(folder_path + '/raw/Raw_center.txt', folder_path + '/converted/Converted_center.txt',
                intervals_1, cumu_weight)
    calibration_file(folder_path + '/raw/Raw_center_2.txt', folder_path + '/converted/Converted_center_2.txt'
                ,intervals_2, cumu_weight_2)



folder_name = '../Calibration/data'
#x, y = print_calibration_curves()
#subplot_overlap([x], [y], ["Raw Conversions"], ["Raw"], ["Converted (Kg)"], 1, 1,
#                legend=[["BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_LEFT", "TOP_RIGHT"]], fontsize=[14], overlapx=True)
#plot_show_all()

load_corners(folder_name)
#load_center(folder_name)
plot_show_all()

