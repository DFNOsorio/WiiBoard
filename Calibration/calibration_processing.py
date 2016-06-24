import numpy as np
from Calibration.config import *


def time_reshape(time_vector):

    return list(np.array(time_vector) - time_vector[0])


def raw_to_kilos(raw_data_point, corner, matrix):

    converted = []
    converted2 = []

    m_17 = (17*1.0) / (matrix[1][corner] - matrix[0][corner]*1.0)
    b_17 = 17 - m_17 * matrix[1][corner] * 1.0

    m_37 = (37.5 * 1.0 - 17.0) / (matrix[2][corner] - matrix[1][corner] * 1.0)
    b_37 = 37.5 - m_37 * matrix[2][corner] * 1.0

    for i in range(0, len(raw_data_point)):

        if raw_data_point[i] <= matrix[1][corner]:
            converted.append(raw_data_point[i] * m_17 * 1.0 + b_17)
        else:
            converted.append(raw_data_point[i] * m_37 * 1.0 + b_37)

    return converted


def all_2_kilo(raw_vectors, corners, matrix):
    output = []

    for i in range(0, len(raw_vectors)):
        output.append(raw_to_kilos(raw_vectors[i], corners[i], matrix))
    return output


def zero_out(raw_data_points):
    raw_means = []
    [[raw_means.append(np.mean(raw_data_points[i]))] for i in range(0, 4)]

    calibration_matrix_adjusted[0] = raw_means


def interval_means(intervals, axis):
    means = []
    for i in range(0, len(intervals)):
        temp = []
        for j in range(0, len(axis)):
            temp.append(np.mean(axis[j][intervals[i][0]:intervals[i][1]]))
        means.append(temp)
    return means


def weight_difference(list1, list2):
    difference = []
    for i in range(0, len(list1)):
        if type(list2[i]) is list:
            difference.append(list1[i] - list2[i][0])
        else:
            difference.append(list1[i] - list2[i])

    return difference


def weight_sum(tl, tr, bl, br):
    total_weight = []
    for i in range(0, len(tl)):
        total_weight.append(tl[i] + tr[i] + bl[i] + br[i])
    return total_weight


def print_calibration_curves():
    raw_points = []
    points = []
    corners = [TOP_RIGHT, BOTTOM_RIGHT, TOP_LEFT, BOTTOM_LEFT]
    for i in corners:
        temp = range(calibration_matrix_adjusted[0][i], calibration_matrix_adjusted[2][i])
        tr = raw_to_kilos(temp, i, calibration_matrix)
        raw_points.append(temp)
        points.append(tr)
    return raw_points, points
