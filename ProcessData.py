import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import numpy as np

def uploadData(data):
    TL = []
    TR = []
    BL = []
    BR = []
    time = []

    lines = data.readlines()[1:]

    for line in lines:
        tempLine = line.split(';')
        TL.append(float(tempLine[0]))
        TR.append(float(tempLine[1]))
        BL.append(float(tempLine[2]))
        BR.append(float(tempLine[3]))
        time.append(float(tempLine[4]))

    return [TL, TR, BL, BR, time]


Data = open('Data/PreMarks/Raw_Mon_16:22:19')

[TL, TR, BL, BR, time] = uploadData(Data)

