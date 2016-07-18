from DataProcessor import *
import time

folder_name = '../WiiBoard/Trials/'
#folder_name = '../Trials/'

patient = 'Liliana1000'

## Loading  and syncing

output = sync_files(folder_name, patient, plot=False, high=True)

## Data segmentation

[s1, s2, s3, s4] = segmented_signal([output])

## Processing

print "Patient mean weight: " + str(np.mean(s1[0][5]))

    # Removing duplicates

[s1[0], s2[0], s3[0], s4[0]] = remove_duplicates_batch([s1[0], s2[0], s3[0], s4[0]])

[s1, s2, s3, s4] = add_COPs([s1, s2, s3, s4], interval_COPs([s1, s2, s3, s4]))

# Zero out data

EMG_zero, EMG_l_zero, EMG_means_zero = load_emg_rest(folder_name+patient+'/Base')

[s1_z, s2_z, s3_z, s4_z] = zero_out_EMG([s1, s2, s3, s4], EMG_means_zero)

plot = False
if plot:
    motion_reports(patient, [s1_z, s2_z, s3_z, s4_z])

# Spectrogram of each emg, for each interval

[s1_zs, s2_zs, s3_zs, s4_zs] = add_spec([s1_z, s2_z, s3_z, s4_z])

# Spectrogram of each psd, for each interval

[s1_zsp, s2_zsp, s3_zsp, s4_zsp] = add_psd([s1_zs, s2_zs, s3_zs, s4_zs])

plot = False
if plot:
    spectrogram_report([s1_zsp, s2_zsp, s3_zsp, s4_zsp])

plot = True
if plot:
    psd_reports([s1_zsp, s2_zsp, s3_zsp, s4_zsp])


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