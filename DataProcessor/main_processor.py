from DataProcessor import *

folder_name = '../WiiBoard/Trials/'

patient = 'JoaoPedro1000'

data, filter_frequency = process_patient(folder_name, patient)

sendmessage('Pdf generator', 'Start')
pdf_selection(data, patient, filter_frequency)
sendmessage('Pdf generator', 'End')