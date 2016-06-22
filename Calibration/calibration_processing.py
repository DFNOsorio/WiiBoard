import numpy as np
from Calibration.config import *


def time_reshape(time_vector):

    return list(np.array(time_vector) - time_vector[0])


def raw_to_kilos(raw_data_point, corner):

    converted = []

    m_17 = (17*1.0) / (calibration_matrix_adjusted[1][corner] - calibration_matrix_adjusted[0][corner]*1.0)
    b_17 = 17 - m_17 * calibration_matrix_adjusted[1][corner] * 1.0

    m_37 = (17 - 37.5 * 1.0) / (calibration_matrix_adjusted[2][corner] - calibration_matrix_adjusted[1][corner] * 1.0)
    b_37 = 37.5 - m_37 * calibration_matrix_adjusted[2][corner] * 1.0

    for i in range(0, len(raw_data_point)):

        if raw_data_point[i] <= calibration_matrix_adjusted[1][corner]:
            converted.append(raw_data_point[i] * m_17 * 1.0 + b_17)
        else:
            converted.append(raw_data_point[i] * m_37 * 1.0 + b_37)

    return converted


def zero_out(raw_data_points):
    raw_means = []
    [[raw_means.append(np.mean(raw_data_points[i]))] for i in range(0, 4)]

    raw_dif = calibration_matrix[0] - np.array(raw_means)

    calibration_matrix_adjusted[0] = raw_means


def interval_means(intervals, axis):
    means = []
    for i in range(0, len(intervals)):
        temp = []
        for j in range(0, len(axis)):
            temp.append(np.mean(axis[j][intervals[i][0]:intervals[i][1]]))
        means.append(temp)
    return means
