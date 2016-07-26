import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy
from scipy import ndimage
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
