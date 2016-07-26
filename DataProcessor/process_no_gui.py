from DataProcessor import *

folder_name = '../WiiBoard/Trials/'
#folder_name = '../Trials/'

patient = 'Diana1000'

## Loading  and syncing

output = sync_files(folder_name, patient, plot=False, high=True)

## Data segmentation

[s1, s2, s3, s4] = segmented_signal([output])

## Processing

print "Patient mean weight: " + str(np.mean(s1.get_variable("wii_data")[5]))

print "Removing duplicates"

[s1, s2, s3, s4] = remove_duplicates_batch([s1, s2, s3, s4])

print "Adding COPs"

[s1, s2, s3, s4] = add_COPs([s1, s2, s3, s4], interval_COPs([s1, s2, s3, s4]))

print "Adding velocity and acceleration thresholds"

[s1, s2, s3, s4] = add_threshold([s1, s2, s3, s4])

print "Zeroing out data"

EMG_zero, EMG_l_zero, EMG_means_zero = load_emg_rest(folder_name+patient+'/Base')

[s1, s2, s3, s4] = zero_out_EMG([s1, s2, s3, s4], EMG_means_zero)

pre_filter = False

if pre_filter:

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

    plot = False
    if plot:
        motion_reports(patient, [s1, s2, s3, s4], thresholds=True, rms_data="emg_rms_data")

filtering = True

if filtering:

    print "Filter, for each interval"

    [s1, s2, s3, s4] = add_filtered_signal([s1, s2, s3, s4], frequencies=[30, 400], order=4)

    print "New spectrogram of each emg, for each interval"

    [s1, s2, s3, s4] = add_spec([s1, s2, s3, s4], data_var="filter_EMG_data", new_var="filter_spec_data")

    print "New psd, for each interval"

    [s1, s2, s3, s4] = add_psd([s1, s2, s3, s4], data_var="filter_EMG_data", new_var="filter_psd_data")

    spec, ds = spectrogram_report([s1, s2, s3, s4], max_flag=True, data_var="filter_spec_data")

    spec_over, ds = spec_psd_overlay([s1, s2, s3, s4], dB=True, data_var_psd="filter_psd_data", data_var_spec="filter_spec_data")

    psds, bs = psd_reports([s1, s2, s3, s4], new_var="filter_psd_data")

    print "Psd and spec integral (after_filtering), for each interval"

    [s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4], data_var_psd="filter_psd_data",
                                          data_var_spec="filter_spec_data", new_var="integrated_spec_psd_filtered")

    spec_int, bs = spec_psd_integrated([s1, s2, s3, s4], integrated_data="integrated_spec_psd_filtered", spec_data='filter_spec_data')

    print "New smooth, for each interval"

    [s1, s2, s3, s4] = smooth_intervals([s1, s2, s3, s4], data_var="filter_EMG_data", new_var="smoothed_data_filtered", window=100)

    rms_figs, axes = rms_reports([s1, s2, s3, s4], rms_data="smoothed_data_filtered", emg_data="filter_EMG_data")

    motion_figs, comparing_figs = motion_reports(patient+" (10-400 Hz)", [s1, s2, s3, s4],
                                                 emg_data="filter_EMG_data", thresholds=False,
                                                 rms_data="smoothed_data_filtered")

    new_figures = pdf_figure_reshape([motion_figs, spec, spec_over, psds, spec_int, rms_figs, comparing_figs])

    # LEGENDAS MAXMIN AUTOMATICO

    #sendmessage('Pdf generator', 'Start')
    pdf_generator(new_figures, patient, foldername='../WiiBoard/DataProcessor/Images/')
    #sendmessage('Pdf generator', 'End')
    plot = False
    if plot:
        plot_show_all()
# TODO
# Thresholds para a e para v
# Contorno
# Overlay do RMS
# SinalPositivo
# Tirar eventos da acelaracao e da velocidade
# ligar eventos
# Adaptar para usar cython


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


