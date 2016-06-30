from processing_wii import *
from PathMath import pathmath_interpolationxy
from COPCode import *
from printing_lib import *
from time import strftime, localtime


def load_wii_trial(path, run, segments):

    [tl, tr, bl, br, tm, events, event_time] = file_reader(path + '.txt')
    print strftime('%Y-%m-%d %H:%M:%S', localtime(tm[0]))
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

    [xx, yy] = segmentation(rt, segments, [COPx, COPy])

    COPx_s = xx[1]
    COPy_s = yy[1]

    area, contour_array = pathmath_interpolationxy.get_area(COPx_s, COPy_s, scanning_window=1)

    f, ax1, ax2, ax3, ax4, ax5, ax6 = grid(run)

    ax1_pop([[COPx], [COPy], "COPx (mm)", "COPy (mm)", "All Data", ["COP"]], ax1)
    ax1_pop([[COPx_s, contour_array[:, 0]], [COPy_s, contour_array[:, 1]],
             "COPx (mm)", "COPy (mm)", "Segmented data", ["COP", "Area"]], ax6)

    axe_populator([rt, [events], "Time (s)", "Events", "Button Pressed", ["Event"]], ax2)
    axe_populator([rt, [COPx], "Time (s)", "COPx (mm)", "COPx", ["COPx"]], ax3)
    axe_populator([rt, [COPy], "Time (s)", "COPy (mm)", "COPy", ["COPy"]], ax4)
    axe_populator([rt, [converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a], "Time (s)", "COPy (mm)",
                   "Sensor Weights", ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]], ax5)

    add_vlines([ax3], time_to_points(rt, segments), [max(COPx), max(COPx)], rt)

    return COPx_s, COPy_s, area, contour_array, event_time
