from DataProcessor import *


def process_patient(folder_name, patient, multiple=False, pre_filter = False, filtering=True,
                    filter_frequency=(30, 400), pdf=True, norm=False, emg_smoother_window=500):

    if multiple:
        output = sync_files_multiple(folder_name, patient, ["_1", "_4"], [[0, 1, 2], [3]], number_of_files=2,
                                     plot=False,
                                     high=True)

        [s1, s2, s3] = segmented_signal(output, input_index=0, number_of_segments=3)

        [s4] = segmented_signal(output, input_index=1, number_of_segments=1)

    else:
        output = sync_files(folder_name, patient, plot=False, high=True)

        [s1, s2, s3, s4] = segmented_signal([output])


    ## Processing

    print "Patient mean weight: " + str(np.mean(s1.get_variable("wii_data")[5]))

    print "Removing duplicates \n"

    [s1, s2, s3, s4] = remove_duplicates_batch([s1, s2, s3, s4])

    print "Adding COPs \n"

    [s1, s2, s3, s4] = add_COPs([s1, s2, s3, s4], interval_COPs([s1, s2, s3, s4]))

    print "Adding velocity and acceleration thresholds\n"

    [s1, s2, s3, s4] = add_threshold([s1, s2, s3, s4])

    print "Zeroing out data\n"

    EMG_zero, EMG_l_zero, EMG_means_zero = load_emg_rest(folder_name+patient+'/Base')

    [s1, s2, s3, s4] = zero_out_EMG([s1, s2, s3, s4], EMG_means_zero)

    if pre_filter:

        print "Spectrogram of each emg, for each interval"

        [s1, s2, s3, s4] = add_spec([s1, s2, s3, s4])

        print "Psd, for each interval"

        [s1, s2, s3, s4] = add_psd([s1, s2, s3, s4])

        print "Psd and spec integral, for each interval"

        [s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4])

        print "RMS, for each interval"

        [s1, s2, s3, s4] = add_EMG_RMS([s1, s2, s3, s4], window_size=1000)

        [s1, s2, s3, s4] = smooth_intervals([s1, s2, s3, s4], window=emg_smoother_window)

    if filtering:

        print "Filtering signal \n"

        [s1, s2, s3, s4] = add_filtered_signal([s1, s2, s3, s4], frequencies=filter_frequency, order=4)

        print "Making spectrograms \n"

        [s1, s2, s3, s4] = add_spec([s1, s2, s3, s4], data_var="open_signals_data_filtered", new_var="spec_data_filtered")

        print "Calculating the PSD \n"

        [s1, s2, s3, s4] = add_psd([s1, s2, s3, s4], data_var="open_signals_data_filtered", new_var="psd_data_filtered")

        print "Integrating the spectrogram and the PSD \n"

        [s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4], data_var_psd="psd_data_filtered",
                                              data_var_spec="spec_data_filtered", new_var="spec_psd_integrated_filtered")

        print "Smoothing the EMG (window size = " + str(emg_smoother_window) +")\n"
        [s1, s2, s3, s4] = smooth_intervals([s1, s2, s3, s4], data_var="open_signals_data_filtered",
                                            new_var="smoothed_data_filtered", window=emg_smoother_window)

    return [s1, s2, s3, s4], filter_frequency, emg_smoother_window

# TODO
#
#


