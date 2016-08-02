from matplotlib.backends.backend_pdf import PdfPages
from DataProcessor.Printing.reporting import *
from DataProcessor.processing_methods import get_range_var
import os


def pdf_generator(figures, patient, foldername='../WiiBoard/DataProcessor/Images/', text=''):

    if not os.path.exists(foldername+patient+'/'):
        os.makedirs(foldername+patient+'/')

    pdf_pages = PdfPages(foldername+patient+'/report' + text + '.pdf')

    for i in figures:
        i.set_size_inches(20, 11.25)
        pdf_pages.savefig(i, dpi=300)

    pdf_pages.close()


def pdf_figure_reshape(figures):

    number_of_figures = len(figures)

    new_figures = [[ ] for i in range(0, number_of_figures*4)]
    counter = 0
    for i in range(0, 4):
        for j in range(0, number_of_figures):
            new_figures[counter] = figures[j][i]
            counter += 1

    return new_figures


def pdf_selection(data, patient, filter_frequency, filtered=True, motion=True, cop_ynormalization='global',
                  pdf_text='_global',
                  emg_ynormalization='global', smoothed_ynormalization='global', comparison=False,
                  spec=True, spec_norm='global', integration_flag=False,
                  spec_psd=True, spec_psd_norm='global',
                  smooths=True, smoothing_window=100):

    figs = []
    pdf_title = patient
    smoothed_var = 'smoothed_data'
    open_signal_var = "open_signals_data"
    spec_data_var = 'spec_data'
    integrated_data_var = 'spec_psd_integrated'
    psd_var = "psd_data"

    if filtered:
        pdf_title = patient + " (" + str(filter_frequency[0]) + '-' + str(filter_frequency[1]) + " Hz)"
        smoothed_var += '_filtered'
        open_signal_var += '_filtered'
        spec_data_var += '_filtered'
        integrated_data_var += '_filtered'
        psd_var += '_filtered'

    ranges = [get_range_var(data, "wii_data", [0, 1], [6]), get_range_var(data, open_signal_var, [1, 2, 3, 4]),
              get_range_var(data, smoothed_var, [1, 2, 3, 4]), get_range_var(data, "wii_data", [2, 3], [6]),
              get_range_var(data, "wii_data", [4, 5], [6])]

    if motion:
        print "Montion"
        figs.append(raw_reporting(data, pdf_title, ranges_=ranges, smoothed_var=smoothed_var, wii_smoothing=False,
                                  smoothing_indexes=[10, 50, 50], emg_smoothing=True, open_signal_var=open_signal_var,
                                  cop_ynormalization=cop_ynormalization, emg_ynormalization=emg_ynormalization,
                                  smoothed_ynormalization=smoothed_ynormalization))

    if comparison:
        print "Comparison"

        figs.append(comparing_reports(data, pdf_title, ranges_=ranges, smoothed_var=smoothed_var,
                                      cop_ynormalization=cop_ynormalization,
                                      smoothed_ynormalization=smoothed_ynormalization))
    if spec:
        print "Spec"

        figs.append(spectrogram_report(data, pdf_title, data_var=spec_data_var, integration_flag=integration_flag,
                                       integrated_data_var=integrated_data_var, norm=spec_norm))
    if spec_psd:
        print "Spec_Psd"

        figs.append(spec_psd_overlay(data, pdf_title, data_var_psd=psd_var, data_var_spec=spec_data_var, alpha=0.1,
                                     dB="True", norm=spec_psd_norm))
    if smooths:
        print "Smooths"
        figs.append(rms_reports(data, pdf_title, ranges_=ranges[1:3], smoothing_window=smoothing_window,
                                smoothed_var=smoothed_var, open_signal_var=open_signal_var,
                                norm=smoothed_ynormalization))

    new_figures = pdf_figure_reshape(figs)
    pdf_generator(new_figures, patient, foldername='../WiiBoard/DataProcessor/Images/', text=pdf_text)

