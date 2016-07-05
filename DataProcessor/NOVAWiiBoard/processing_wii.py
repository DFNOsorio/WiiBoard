import numpy as np

from DataProcessor.NOVAWiiBoard.config import *


def time_reshape(time_vector):

    return list(np.array(time_vector) - time_vector[0])


def file_reader(name_of_file):
    tl = []
    tr = []
    bl = []
    br = []
    time = []
    events = []
    event_time = 0

    occurred = False

    data = open(name_of_file)
    lines = data.readlines()[1:]

    for line in lines:
        temp_line = line.split(';')
        if temp_line[0] == 'Button pressed\n':
            occurred = True
            events.pop()

        else:
            tl.append(float(temp_line[0]))
            tr.append(float(temp_line[1]))
            bl.append(float(temp_line[2]))
            br.append(float(temp_line[3]))
            time.append(float(temp_line[4]))

        if occurred:
            events.append(1)
        else:
            events.append(0)

    return [tl, tr, bl, br, time, events, event_time]


def raw_to_kilos(raw_data_point, corner, matrix):
    converted = []

    x_0_17 = matrix[0][corner] * 1.0
    y_0_17 = 0.0

    x_1_17 = matrix[1][corner] * 1.0
    y_1_17 = 17.0

    x_0_37 = x_1_17
    y_0_37 = y_1_17

    x_1_37 = matrix[2][corner] * 1.0
    y_1_37 = 37.5

    cte_17 = ((x_1_17 * y_0_17 - x_0_17 * y_1_17) / (x_1_17 - x_0_17))

    cte_37 = ((x_1_37 * y_0_37 - x_0_37 * y_1_37) / (x_1_37 - x_0_37))

    # m_17 = (17*1.0) / (matrix[1][corner] - matrix[0][corner]*1.0)
    # b_17 = 17 - m_17 * matrix[1][corner] * 1.0

    # m_37 = (37.5 * 1.0 - 17.0) / (matrix[2][corner] - matrix[1][corner] * 1.0)
    # b_37 = 37.5 - m_37 * matrix[2][corner] * 1.0

    for i in range(0, len(raw_data_point)):

        if raw_data_point[i] <= matrix[1][corner]:
            value = raw_data_point[i] * ((y_1_17 - y_0_17) / (x_1_17 - x_0_17)) + cte_17
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


def scaler(kg_vector, corner):
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
        output.append(scaler(raw_vectors[i], corners[i]))
    return output


# noinspection PyStatementEffect
def zero_out(raw_data_points):
    raw_means = []
    [[raw_means.append(np.mean(raw_data_points[i]))] for i in range(0, 4)]

    calibration_matrix_adjusted[0] = raw_means


def time_to_points(time_vector, time_stamps):
    points_stamps = []
    for i in time_stamps:
        points_stamps.append(
            [np.where(np.array(time_vector) < i[0])[0][-1], np.where(np.array(time_vector) < i[1])[0][-1]])
    return points_stamps


def segmentation(time_vector, time_stamps, vectors):
    indexes = time_to_points(time_vector, time_stamps)
    output = []
    for i in vectors:
        temp = []
        for j in indexes:
            temp.append(i[j[0]:(j[1]+1)])
        output.append(temp)
    return output


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