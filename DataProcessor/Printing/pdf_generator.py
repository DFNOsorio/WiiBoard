
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy
from scipy import ndimage
import os

if matplotlib.get_backend() != "TKAgg":
matplotlib.use("TKAgg")


def pdf_generator(figures, patient, foldername='../WiiBoard/DataProcessor/Images/'):

    if not os.path.exists(foldername+patient+'/'):
        os.makedirs(foldername+patient+'/')

    pdf_pages = PdfPages(foldername+patient+'/report.pdf')

    for i in figures:

        #rotated_Plot = ndimage.rotate(i, 90)
        pdf_pages.savefig(i)

    pdf_pages.close()
