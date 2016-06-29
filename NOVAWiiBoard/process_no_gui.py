from processing import *
from PathMath import *
from COPCode import *
from printing_lib import *

folder_name = '../Trials/'

patient ='David/'
run = 'David_TEST2'

[tl, tr, bl, br, time, events] = file_reader(folder_name+patient+run+'.txt')

rt = time_reshape(time)

[converted_tl, converted_tr, converted_bl, converted_br] = all_2_kilo([tl, tr, bl, br],
                                                                      [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT,
                                                                       BOTTOM_RIGHT],
                                                                      calibration_matrix_adjusted)

[converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a] = all_2_converting([converted_tl, converted_tr,
                                                                                     converted_bl, converted_br],
                                                                                    [TOP_LEFT, TOP_RIGHT,
                                                                                     BOTTOM_LEFT, BOTTOM_RIGHT])

[COPx, COPy] = COP(converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a)


# subplot_overlap([COPx, rt, rt, rt],
#                 [[COPy], [COPx], [COPy], [converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a]],
#                 ["Center of Pressure", "COPx", "COPy", "Sensor Weights"],
#                 ["COPx (mm)", "Time (s)", "Time (s)", "Time (s)"],
#                 ["COPy (mm)", "COPx (mm)", "COPy (mm)", "Weight (KG)"],
#                 2, 2,
#                 legend=[["COP"], ["COP"], ["COP"], ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]],
#                 fontsize=[14], overlapx=False, wii=[1])


f, ax1, ax2, ax3, ax4, ax5 = grid()

ax1_pop([[COPx], [COPy], "COPx (mm)", "COPy (mm)", run, "COP"], ax1)
axe_populator([rt, [events], "Time (s)", "Events", "Button Pressed", "Event"], ax2)
axe_populator([rt, [COPx], "Time (s)", "COPx (mm)", "COPx", "COPx"], ax3)
axe_populator([rt, [COPy], "Time (s)", "COPy (mm)", "COPy", "COPy"], ax4)
axe_populator([rt, [converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a], "Time (s)", "COPy (mm)",
               "Sensor Weights", ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]], ax5)
plot_show_all()
