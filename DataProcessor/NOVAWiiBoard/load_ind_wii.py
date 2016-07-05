from COPCode import *
from PathMath import pathmath_interpolationxy
from processing_wii import *


def load_wii_trial(path, run, segments=False):

    [tl, tr, bl, br, tm, events, event_time] = file_reader(path + '.txt')
    rt = time_reshape(tm)

    [converted_tl, converted_tr, converted_bl, converted_br] = all_2_kilo([tl, tr, bl, br],
                                                                          [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT,
                                                                           BOTTOM_RIGHT],
                                                                          calibration_matrix_adjusted)

    [converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a] = all_2_converting([converted_tl, converted_tr,
                                                                                         converted_bl, converted_br],
                                                                                        [TOP_LEFT, TOP_RIGHT,
                                                                                         BOTTOM_LEFT, BOTTOM_RIGHT])

    [COPx, COPy] = COP(converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a)

    if segments is not False:
        [xx, yy, tt] = segmentation(rt, segments, [COPx, COPy, rt])

        COPx_s = xx[1]
        COPy_s = yy[1]
        rt_s = tt[1]
    else:
        COPx_s = COPx
        COPy_s = COPy
        rt_s = rt

    area, contour_array = pathmath_interpolationxy.get_area(COPx_s, COPy_s, scanning_window=1)



    velocity(COPx_s, COPy_s, rt_s)

    return COPx_s, COPy_s, area, contour_array, event_time, rt, [tl, tr, bl, br, events], tm[0]
