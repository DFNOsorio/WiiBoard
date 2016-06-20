import numpy as np
from Calibration.config import *


def time_reshape(time_vector):

    return list(np.array(time_vector) - time_vector[0])


def raw_to_kilos(raw_data_point, converted_data_point, corner):

    converted = []

    m_17 = (17*1.0) / (calibration_matrix[1][corner] - calibration_matrix[0][corner]*1.0)
    b_17 = 17 - m_17 * calibration_matrix[1][corner] * 1.0

    m_37 = (17 - 37.5 * 1.0) / (calibration_matrix[2][corner] - calibration_matrix[1][corner] * 1.0)
    b_37 = 37.5 - m_37 * calibration_matrix[2][corner] * 1.0
    print raw_data_point[10]
    print calibration_matrix[1][corner]
    for i in range(0, len(raw_data_point)):

        if raw_data_point[i] <= calibration_matrix[1][corner]:
            converted.append(raw_data_point[i] * m_17 * 1.0 + b_17)
        else:
            converted.append(raw_data_point[i] * m_37 * 1.0 + b_37)

    converted_adjusted = converted - np.mean(converted[0:100])

    print converted_data_point[0:10]
    print converted[0:10]
    print converted_adjusted
    print np.mean(converted[0:10])

    return converted

