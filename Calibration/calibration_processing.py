import numpy as np
from Calibration.config import *


def time_reshape(time_vector):

    return list(np.array(time_vector) - time_vector[0])


def raw_to_kilos(raw_data_point, corner, matrix):

    converted = []

    x_0_17 = matrix[0][corner]*1.0
    y_0_17 = 0.0

    x_1_17 = matrix[1][corner]*1.0
    y_1_17 = 17.0

    x_0_37 = x_1_17
    y_0_37 = y_1_17

    x_1_37 = matrix[2][corner] * 1.0
    y_1_37 = 37.5

    cte_17 = ((x_1_17*y_0_17 - x_0_17*y_1_17)/(x_1_17 - x_0_17))

    cte_37 = ((x_1_37 * y_0_37 - x_0_37 * y_1_37) / (x_1_37 - x_0_37))

    #m_17 = (17*1.0) / (matrix[1][corner] - matrix[0][corner]*1.0)
    #b_17 = 17 - m_17 * matrix[1][corner] * 1.0

    #m_37 = (37.5 * 1.0 - 17.0) / (matrix[2][corner] - matrix[1][corner] * 1.0)
    #b_37 = 37.5 - m_37 * matrix[2][corner] * 1.0

    for i in range(0, len(raw_data_point)):

        if raw_data_point[i] <= matrix[1][corner]:
            value = raw_data_point[i] * ((y_1_17 - y_0_17)/(x_1_17 - x_0_17)) + cte_17
        else:
            value = raw_data_point[i] * ((y_1_37 - y_0_37) / (x_1_37 - x_0_37)) + cte_37

        if value < 0:
            value = 0
        converted.append(value)
    return converted


def all_2_kilo(raw_vectors, corners, matrix):
    output = []

    for i in range(0, len(raw_vectors)):
        output.append(raw_to_kilos(raw_vectors[i], corners[i], matrix))
    return output


def scaller(kg_vector, corner):
    x_0_17 = 0
    y_0_17 = 0.0

    x_1_17 = Scale_16[4]
    y_1_17 = Scale_16[corner] * 1.0


    x_0_37 = x_1_17
    y_0_37 = y_1_17

    x_1_37 = Scale_25[4]
    y_1_37 = Scale_25[corner] * 1.0


    cte_17 = ((x_1_17 * y_0_17 - x_0_17 * y_1_17) / (x_1_17 - x_0_17))

    cte_37 = ((x_1_37 * y_0_37 - x_0_37 * y_1_37) / (x_1_37 - x_0_37))

    converted = []

    for i in range(0, len(kg_vector)):

        if kg_vector[i] <= Scale_16[4]:
            value = kg_vector[i] + kg_vector[i] * ((y_1_17 - y_0_17) / (x_1_17 - x_0_17)) + cte_17
        else:
            value = kg_vector[i] + kg_vector[i] * ((y_1_37 - y_0_37) / (x_1_37 - x_0_37)) + cte_37

        if value < 0:
            value = 0
        converted.append(value)
    return converted


def all_2_converting(raw_vectors, corners):
    output = []
    for i in range(0, len(raw_vectors)):
        output.append(scaller(raw_vectors[i], corners[i]))
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


def time_to_points(time_vector, time_stamps):
    points_stamps  = []
    for i in time_stamps:
        temp = []
        temp.append(np.where(np.array(time_vector) < i[0])[0][-1])
        temp.append(np.where(np.array(time_vector) < i[1])[0][-1])
        points_stamps.append(temp)
    print points_stamps

