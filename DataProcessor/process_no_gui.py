from DataProcessor import *

folder_name = '../Trials/'

patient = 'Catia'

COPx_s, COPy_s, area, contour_array, et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, initial_delta = load_open_trial(folder_name+patient+'/Test', t0)

print reformat_time(np.array(open_time), initial_delta)



