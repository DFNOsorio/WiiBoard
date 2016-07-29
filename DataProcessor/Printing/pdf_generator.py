from matplotlib.backends.backend_pdf import PdfPages
from DataProcessor.Printing.reporting import *
from DataProcessor.processing_methods import get_range_var
import os


def pdf_generator(figures, patient, foldername='../WiiBoard/DataProcessor/Images/'):

    if not os.path.exists(foldername+patient+'/'):
        os.makedirs(foldername+patient+'/')

    pdf_pages = PdfPages(foldername+patient+'/report.pdf')

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


def pdf_selection(data, patient, filter_frequency, filtered=True, motion=True, spec=True, spec_pds=True, psds=False, spec_int=False,
                  rms_fig=True, comparison=True, seg_norm=True, global_norm=False):

    figs = []
    pdf_title = patient
    smoothed_var = 'smoothed_data'
    open_signal_var = "open_signals_data"

    if filtered:
        pdf_title = patient + " (" + str(filter_frequency[0]) + '-' + str(filter_frequency[1]) + " Hz)"
        smoothed_var = 'smoothed_data_filtered'
        open_signal_var = "filter_EMG_data"

    ranges = [get_range_var(data, "wii_data", [0, 1], [6]), get_range_var(data, open_signal_var, [1, 2, 3, 4]),
              get_range_var(data, smoothed_var, [1, 2, 3, 4])]
    if motion:

        figs.append(raw_reporting(data, pdf_title, ranges_=ranges, smoothed_var=smoothed_var, wii_smoothing=False,
                                  smoothing_indexes=[10, 50, 50], emg_smoothing=True, open_signal_var=open_signal_var,
                                  cop_ynormalization='global', emg_ynormalization='global',
                                  smoothed_ynormalization="global"))

    if comparison:
        figs.append(comparing_reports(data, pdf_title, ranges_=ranges, smoothed_var=smoothed_var,
                                      open_signal_var=open_signal_var))

    new_figures = pdf_figure_reshape(figs)
    pdf_generator(new_figures, patient, foldername='../WiiBoard/DataProcessor/Images/')

