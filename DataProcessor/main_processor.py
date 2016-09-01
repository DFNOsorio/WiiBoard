from DataProcessor import *

folder_name = '../WiiBoard/Trials/'

patient = 'Andreia1000'

data, filter_frequency, emg_smoother_window = process_patient(folder_name, patient, multiple=True)
EMG_diferential(data, patient)

#sendmessage('Pdf generator', 'Start')
# print "Generating PDF"
# pdf_selection(data, patient, filter_frequency, motion=True, comparison=True, spec=True, spec_psd=True, smooths=True,
#               integration_flag=True, smoothing_window=emg_smoother_window, cop_ynormalization='global',
#               emg_ynormalization='global', smoothed_ynormalization='global', spec_norm='global', spec_psd_norm='global',
#               pdf_text='_global')
# print "Finished"
#sendmessage('Pdf generator', 'End')

