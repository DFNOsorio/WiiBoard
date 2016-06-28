from Calibration.calibration_loaders import *
from Calibration.printing_lib import *

import numpy as np


def load_corners(folder_path):
    wd_bl_1 = calibration_file(folder_path + '/raw/calibrate_bl.txt', folder_path + '/converted/calibrate_bl.txt',
                     intervals_bl, cumu_weight_2, file_name="Bottom Left", plots=False)

    wd_br_1 = calibration_file(folder_path + '/raw/calibrate_br.txt', folder_path + '/converted/calibrate_br.txt',
                     intervals_br, cumu_weight_2, file_name="Bottom Right", plots=False)

    wd_tr_1 = calibration_file(folder_path + '/raw/calibrate_tr.txt', folder_path + '/converted/calibrate_tr.txt',
                    intervals_tr, cumu_weight_2, file_name="Top Right", plots=False)

    wd_tl_1 = calibration_file(folder_path + '/raw/calibrate_tl.txt', folder_path + '/converted/calibrate_tl.txt',
                     intervals_tl, cumu_weight_2, file_name="Top Left", plots=False)

    wd_bl_2 = calibration_file(folder_path + '/raw/calibrate_bl_2.txt', folder_path + '/converted/calibrate_bl_2.txt',
                    intervals_bl_2, cumu_weight_2, file_name="Bottom Left", plots=False)

    wd_bl_3 = calibration_file(folder_path + '/raw/calibrate_bl_3.txt', folder_path + '/converted/calibrate_bl_3.txt',
                               intervals_bl_3, cumu_weight_2, file_name="Bottom Left", plots=False)

    wd_br_2 = calibration_file(folder_path + '/raw/calibrate_br_2.txt', folder_path + '/converted/calibrate_br_2.txt',
                               intervals_br_2, cumu_weight_2, file_name="Bottom Right Wrong?", plots=False)

    wd_br_3 = calibration_file(folder_path + '/raw/calibrate_br_3.txt', folder_path + '/converted/calibrate_br_3.txt',
                     intervals_br_3, cumu_weight_2, file_name="Bottom Right", plots=False)

    wd_tr_2 = calibration_file(folder_path + '/raw/calibrate_tr_2.txt', folder_path + '/converted/calibrate_tr_2.txt',
                     intervals_tr_2, cumu_weight_2, file_name="Top Right", plots=False)

    wd_tl_2 = calibration_file(folder_path + '/raw/calibrate_tl_2.txt', folder_path + '/converted/calibrate_tl_2.txt',
                     intervals_tl_2, cumu_weight_2, file_name="Top Left", plots=False)

    figure, axes = subplot_overlap([cumu_weight_2, cumu_weight_2, cumu_weight_2],
                                   [[wd_tl_1, wd_tr_1, wd_bl_1, wd_br_1], [wd_tl_2, wd_tr_2, wd_bl_2, wd_br_2,  wd_bl_3],
                                    [wd_tl_1, wd_tr_1, wd_bl_1, wd_br_1, wd_tl_2, wd_tr_2, wd_bl_2, wd_br_2,  wd_bl_3]],
                                   title=['With Rubers', 'Without', 'All'],
                                   xlabel=["Weight (kg)", "Weight (kg)", "Weight (kg)"],
                                   ylabel=["Weight Difference (Kg)", "Weight Difference (Kg)",
                                           'Weight Difference (Kg)'],
                                   legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "BOTTOM_RIGHT"],
                                           ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "BOTTOM_RIGHT"],
                                           ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "BOTTOM_RIGHT",
                                            "TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "BOTTOM_RIGHT"]],
                                   lines=1, columns=3, fontsize=12)

    figure = add_sup_title(figure, "Weight Differences", fontsize=14)


def load_center(folder_path):

    calibration_file(folder_path + '/raw/Raw_center.txt', folder_path + '/converted/Converted_center.txt',
                intervals_1, cumu_weight, file_name="Center_1")
    calibration_file(folder_path + '/raw/Raw_center_2.txt', folder_path + '/converted/Converted_center_2.txt'
                ,intervals_2, cumu_weight_2, file_name="Center_2")
    calibration_file(folder_path + '/raw/calibrate_center.txt', folder_path + '/converted/calibrate_center.txt',
                     intervals_center, cumu_weight_2, file_name="Center_3")

def load_center_2(folder_path):
    load_file_adjusted(folder_path + '/raw/Raw_center.txt', folder_path + '/converted/Converted_center.txt',
                       intervals=intervals_1, file_name="Center_1", plots=True, cumu_weights=cumu_weight)

    load_file_adjusted(folder_path + '/raw/Raw_center_2.txt', folder_path + '/converted/Converted_center_2.txt',
                       intervals=intervals_2, file_name="Center_2", plots=True, cumu_weights=cumu_weight_2)

    load_file_adjusted(folder_path + '/raw/calibrate_center.txt', folder_path + '/converted/calibrate_center.txt',
                       intervals=intervals_center, file_name="Center_3", plots=True, cumu_weights=cumu_weight_2)

def load_scale_converters(folder_path):
    bl = calibration_file(folder_path + '/raw/calibrate_final_bl.txt',
                          folder_path + '/converted/calibrate_final_bl.txt',
                          final_bl, final_weights, file_name="Bottom Left", plots=False)

    br = calibration_file(folder_path + '/raw/calibrate_final_br.txt',
                          folder_path + '/converted/calibrate_final_br.txt',
                          final_br, final_weights, file_name="Bottom Right", plots=False)

    tr = calibration_file(folder_path + '/raw/calibrate_final_tr.txt',
                          folder_path + '/converted/calibrate_final_tr.txt',
                          final_tr, final_weights, file_name="Top Right", plots=False)

    tl = calibration_file(folder_path + '/raw/calibrate_final_tl.txt',
                          folder_path + '/converted/calibrate_final_tl.txt',
                          final_tl, final_weights, file_name="Top Left", plots=False)

    figure, axes = subplot_overlap([final_weights],
                                   [[tl, tr, bl, br]],
                                   title=['All'],
                                   xlabel=["Weight (kg)"],
                                   ylabel=['Weight Difference (Kg)'],
                                   legend=[["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT", "BOTTOM_RIGHT"]],
                                   lines=1, columns=1, fontsize=12)


    figure = add_sup_title(figure, "Weight Differences", fontsize=14)


folder_name = '../Calibration/data'
#x, y = print_calibration_curves()
#subplot_overlap([x], [y], ["Raw Conversions"], ["Raw"], ["Converted (Kg)"], 1, 1,
#                legend=[["BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_LEFT", "TOP_RIGHT"]], fontsize=[14], overlapx=True)
#plot_show_all()

#load_corners(folder_name)
#load_scale_converters(folder_name)
#load_center(folder_name)
load_center_2(folder_name)

plot_show_all()

