from Calibration.calibration_loaders import *
from Calibration.OpenSignalsScrapper import *

folder_name = '../Calibration/data/open_signals/'

[tl, tr, bl, br, time, events, event_time] = file_reader(folder_name + 'ACC_1' + '.txt')
file_scrapper(folder_name + 'acc_1' + '.txt')


print event_time
