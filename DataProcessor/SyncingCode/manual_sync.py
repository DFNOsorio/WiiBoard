from DataProcessor import *
folder_name = '/Users/DanielOsorio/Documents/WiiBoard/Trials/'
patient = 'Paulo_1000'

et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

new_wii_time = reformat_time(np.array(rt), epoch - t0)
new_event_time = et - (epoch - t0)

figure, axes = subplot_overlap([[open_time[4000:12000], open_time[4000:12000], open_time[4000:12000], new_wii_time[1000:2000]]],
                               [[ACC[0][4000:12000], ACC[1][4000:12000], ACC[2][4000:12000], np.array(data[4][1000:2000]) * 55000]],
                                "Sync", "Time (s)", "Raw", 1, 1, overlapx=True)


folder_name = '/Users/DanielOsorio/Documents/WiiBoard/Trials/'
patient = 'Liliana_1000'

et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

new_wii_time = reformat_time(np.array(rt), epoch - t0)
new_event_time = et - (epoch - t0)

figure, axes = subplot_overlap([[open_time[40000:60000], open_time[40000:60000], open_time[40000:60000], new_wii_time[3000:7000]]],
                               [[ACC[0][40000:60000], ACC[1][40000:60000], ACC[2][40000:60000], np.array(data[4][3000:7000]) * 55000]],
                                "Sync", "Time (s)", "Raw", 1, 1, overlapx=True)


folder_name = '/Users/DanielOsorio/Documents/WiiBoard/Trials/'
patient = 'Andreia_1000'

et, rt, data, t0 = load_wii_trial(folder_name+patient+'/WII', patient, False)
EMG, ACC, ECG, EMG_l, ACC_l, ECG_l, open_time, epoch = load_open_trial(folder_name+patient+'/Test')

new_wii_time = reformat_time(np.array(rt), epoch - t0)
new_event_time = et - (epoch - t0)

figure, axes = subplot_overlap([[open_time[0:20000], open_time[0:20000], open_time[0:20000], new_wii_time[0:3000]]],
                               [[ACC[0][0:20000], ACC[1][0:20000], ACC[2][0:20000], np.array(data[4][0:3000]) * 55000]],
                                "Sync", "Time (s)", "Raw", 1, 1, overlapx=True)



plot_show_all()
