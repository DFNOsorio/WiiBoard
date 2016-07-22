from DataProcessor import *

folder_name = '../WiiBoard/Trials/'
#folder_name = '../Trials/'

patient = 'Paulo1000'

## Loading  and syncing

output = sync_files(folder_name, patient, plot=False, high=True)

## Data segmentation

[s1, s2, s3, s4] = segmented_signal([output])

## Processing

print "Patient mean weight: " + str(np.mean(s1.get_variable("wii_data")[5]))


[s1, s2, s3, s4] = remove_duplicates_batch([s1, s2, s3, s4])

[s1, s2, s3, s4] = add_COPs([s1, s2, s3, s4], interval_COPs([s1, s2, s3, s4]))

# Zero out data

EMG_zero, EMG_l_zero, EMG_means_zero = load_emg_rest(folder_name+patient+'/Base')

[s1, s2, s3, s4] = zero_out_EMG([s1, s2, s3, s4], EMG_means_zero)

plot = True
if plot:
    motion_reports(patient, [s1, s2, s3, s4])

print "Spectrogram of each emg, for each interval"

[s1, s2, s3, s4] = add_spec([s1, s2, s3, s4])

print "Psd, for each interval"

[s1, s2, s3, s4] = add_psd([s1, s2, s3, s4])

print "Psd and spec integral, for each interval"

[s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4])

plot = False
if plot:
    spec_psd_integrated([s1, s2, s3, s4], integrated_data="integrated_spec_psd")

plot = False
if plot:
    spectrogram_report([s1, s2, s3, s4], max_flag=True)
    spec_psd_overlay([s1, s2, s3, s4], dB=True)

plot = False
if plot:
    psd_reports([s1, s2, s3, s4])

print "RMS, for each interval"

[s1, s2, s3, s4] = add_EMG_RMS([s1, s2, s3, s4], window_size=1000)

plot = False
if plot:
    rms_reports([s1, s2, s3, s4])

print "Filter, for each interval"

[s1, s2, s3, s4] = add_filtered_signal([s1, s2, s3, s4])

plot = True
if plot:
    motion_reports(patient+" (10-400 Hz)", [s1, s2, s3, s4], emg_data="filter_EMG_data")


print "New spectrogram of each emg, for each interval"

[s1, s2, s3, s4] = add_spec([s1, s2, s3, s4], data_var="filter_EMG_data", new_var="filter_spec_data")

plot = False
if plot:
    spectrogram_report([s1, s2, s3, s4], max_flag=True, data_var="filter_spec_data")

print "New psd, for each interval"

[s1, s2, s3, s4] = add_psd([s1, s2, s3, s4], data_var="filter_EMG_data", new_var="filter_psd_data")

plot = False
if plot:
    psd_reports([s1, s2, s3, s4], new_var="filter_psd_data")

print "Psd and spec integral (after_filtering), for each interval"

[s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4], data_var_psd="filter_psd_data",
                                      data_var_spec="filter_spec_data", new_var="integrated_spec_psd_filtered")


######### reports para os valores integrados

#Filtro 10-400 Hz
#Adaptar funcoes para devolver e aceitar indexes
#
#
# f = plt.figure()
# ax1 = f.add_subplot(311, projection='3d')
# spec_representation(ax1, s4_zsp[3][2][1], s4_zsp[3][2][2], s4_zsp[3][2][3])
# ax2 = f.add_subplot(312)
# axe_populator([s4_zsp[4][0][2], [s4_zsp[4][0][0]], "Frequency", "dB", "PSD", []], ax2)
# ax3 = f.add_subplot(313)
# axe_populator_psd_spec([s4_zsp[4][0][2], s4_zsp[4][0][0], s4_zsp[3][2][2],
#                         [s4_zsp[3][2][0]]], ax3)
#
# #get_freq_stat(Pxx, Pxx_dB, freqs, bins)
# [s1_zspe, s2_zspe, s3_zspe, s4_zspe] = add_EMG_stat([s1_zsp, s2_zsp, s3_zsp, s4_zsp], window_size=100)
#
# figure, axes = subplot_overlap([[s1_zspe[1][0]], [s1_zspe[5][0][1]], [s1_zspe[1][0], s1_zspe[5][0][1]]],
#                                [[s1_zspe[1][1]], [s1_zspe[5][0][0]], [s1_zspe[1][1], s1_zspe[5][0][0]]],
#                                ["EMG", "EMG_Max", "EMG_Max"], ["Time(s)", "Time(s)", "Time(s)"],
#                                ["Raw", "Raw", "Raw"], 3, 1, overlapx=True)
#
# figure, axes = subplot_overlap([s1_zspe[1][0], s1_zspe[1][0], s1_zspe[1][0]],
#                                 [[s1_zspe[1][1]], [s1_zspe[5][4]],
#                                  [np.array(s1_zspe[1][1]) / max(s1_zspe[1][1]), np.array(s1_zspe[5][4]) / max(s1_zspe[5][4])]],
#                                 ["EMG", "EMG_Max", "EMG_Max"], ["Time(s)", "Time(s)", "Time(s)"],
#                                 ["Raw", "Raw", "Raw"], 3, 1, overlapx=False)

##### Pegar nas PSD e por no msm grafico
##### PSD 2D com os limites a mais claros

plot_show_all()