from NOVAWiiBoard import *
from NOVAOpenSignals import *
folder_name = '../Trials/'

patient = 'David/'


load_wii_trial(folder_name+patient+'WII_Data/David_TEST2', 'David_TEST2', DAVID_2_SEGMENTS)
# load_wii_trial(folder_name+patient+'WII_Data/David_TEST3', 'David_TEST3', DAVID_3_SEGMENTS)
# load_wii_trial(folder_name+patient+'WII_Data/David_TEST4', 'David_TEST4', DAVID_4_SEGMENTS)

# 2016-06-24 14:08:34
# 2016-06-24 14:10:05
# 2016-06-24 14:11:28

open_reader(folder_name+patient+'OpenSignals_Data/David_TEST2')

#plot_show_all()
