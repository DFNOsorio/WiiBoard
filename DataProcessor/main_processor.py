from DataProcessor import *

folder_name = '../WiiBoard/Trials/'

patient = 'JoaoPedro1000'

data, filter_frequency = process_patient(folder_name, patient)

#sendmessage('Pdf generator', 'Start')
print "Generating PDF"
pdf_selection(data, patient, filter_frequency, motion=True, comparison=True)
print "Finished"
#sendmessage('Pdf generator', 'End')