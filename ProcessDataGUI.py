import matplotlib
import seaborn
import numpy as np

from NOVAWiiBoard import *
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from scipy.misc import imread
from numpy import *

from Tkinter import *
from PIL import Image, ImageTk



# Logos

def libPhysLogo(frame):
    load = Image.open("Images/logo_libphys.png")
    render = ImageTk.PhotoImage(load)
    img = Label(frame, image=render)
    img.image = render
    img.pack(side=LEFT, fill=BOTH, expand=False, padx=5)


def unlLogo(frame):
    load = Image.open("Images/UNL.gif")
    render = ImageTk.PhotoImage(load)
    img = Label(frame, image=render)
    img.image = render
    img.pack(side=LEFT, fill=BOTH, expand=False, padx=5)


def drawPlotWithWii(frame, x, y, title):
    f = Figure()

    a = f.add_subplot(1,1,1)
    canvas = FigureCanvasTkAgg(f, frame)
    toolbar = NavigationToolbar2TkAgg(canvas, frame)

    img = imread("Images/Wii.JPG")
    a.imshow(img, zorder=0, extent=[-216 - 26, 216 + 26, -114 - 26, 114 + 26])
    a.plot(x, y)
    a.set_title(title, fontsize = 20)
    a.set_xlim([-216 - 30, 216 + 30])
    a.set_ylim([-114 - 30, 114 + 30])
    a.set_ylim([-114 - 30, 114 + 30])
    a.set_xlabel("CoPx (mm)", fontsize=14)
    a.set_ylabel("CoPy (mm)", fontsize=14)


    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


def drawFFT(frame, freq, amp, title):
    if amp[0] == 0:
        title = title + ' (0Hz filtered)'

    f = Figure()
    canvas = FigureCanvasTkAgg(f, frame)
    toolbar = NavigationToolbar2TkAgg(canvas, frame)

    a = f.add_subplot(1,1,1)

    a.plot(freq, amp)
    ttl = a.title
    ttl.set_position([.5, 1.04])
    a.set_title(title, fontsize=20)

    a.set_xlabel("Frequency (Hz)", fontsize=14)
    a.set_ylabel("Amplitude", fontsize=14)
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    toolbar.update()

    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


def drawFFTAndPath(frame, x, y, freq, amp, titleCoP, titleFFT):
    f = Figure()

    gs = gridspec.GridSpec(1,2,width_ratios=[1,1],height_ratios=[1,1])

    a = f.add_subplot(gs[0])
    img = imread("Images/Wii.JPG")
    a.imshow(img, zorder=0, extent=[-216 - 26, 216 + 26, -114 - 26, 114 + 26])
    a.plot(x, y)
    a.set_title(titleCoP, fontsize=13)
    a.set_xlim([-216 - 30, 216 + 30])
    a.set_ylim([-114 - 30, 114 + 30])
    a.set_ylim([-114 - 30, 114 + 30])
    a.set_xlabel("CoPx (mm)", fontsize=12)
    a.set_ylabel("CoPy (mm)", fontsize=12)

    if amp[0] == 0:
        titleFFT = titleFFT + ' (0Hz filtered)'
    b = f.add_subplot(gs[1])
    b.plot(freq, amp)
    ttl = b.title
    ttl.set_position([.5, 1.05])
    b.set_title(titleFFT, fontsize=12)
    b.set_xlabel("Frequency (Hz)", fontsize=12)
    b.set_ylabel("Amplitude", fontsize=12)

    canvas = FigureCanvasTkAgg(f, frame)
    toolbar = NavigationToolbar2TkAgg(canvas, frame)
    canvas.show()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

def client_exit():
    exit()

# Main Window Definitions

class WiiBoardProcApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (COPWindow, StatWindow, COPFFTWindow, COPandFFTWindow):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("COPWindow")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class COPWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.init_window(controller)



    def init_window(self,controller):
        self.controller.title("Wii Balance Board Data Processor")

        self.pack(fill = BOTH, expand = 1)


        #Frame1

        frame1 = Frame(self)
        frame1.pack(side = TOP,fill = X,pady = 5)
        libPhysLogo(frame1)
        unlLogo(frame1)

        StatButton = Button(frame1, text="Statistics", command=lambda: controller.show_frame("StatWindow"))
        StatButton.pack(side=RIGHT, fill=BOTH, expand=False, padx = 5)

        label = Label(frame1, text="CoP Standing")
        label.pack(side=RIGHT, fill=BOTH, expand=True)


        #Menus
        menu = Menu(self.controller)
        self.controller.config(menu = menu)

        file = Menu(menu)

        file.add_command(label= "Exit", command = client_exit)
        menu.add_cascade(label = "File", menu = file)

        path = Menu(menu)
        path.add_command(label = "CoP Standing",command = lambda: controller.show_frame("COPWindow"))
        menu.add_cascade(label = "Plot", menu = path)

        ffts = Menu(menu)
        ffts.add_command(label="CoP Standing FFT", command=lambda: controller.show_frame("COPFFTWindow"))
        menu.add_cascade(label="FFTs", menu=ffts)

        pathsFfts = Menu(menu)
        pathsFfts.add_command(label="CoP Standing FFT Paths", command=lambda: controller.show_frame("COPandFFTWindow"))
        menu.add_cascade(label="PathsFfts", menu=pathsFfts)

        #Plots
        frame2 = Frame(self)
        frame2.pack(side=TOP, fill=X)

        drawPlotWithWii(frame2, COPx, COPy, "Standing center of pressure path")

        frame3 = Frame(self)
        frame3.pack(side=TOP, fill=X)

        FFTButton = Button(frame3, text="COP FFT", command=lambda:controller.show_frame("COPFFTWindow"))
        FFTButton.pack(side=RIGHT, fill=BOTH, expand=False)

        FFTandCOPButton = Button(frame3, text="COP Path and FFT", command=lambda:controller.show_frame("COPandFFTWindow"))
        FFTandCOPButton.pack(side=RIGHT, fill=BOTH, expand=False)


class COPFFTWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        #Frame1

        frame1 = Frame(self)
        frame1.pack(side = TOP,fill = X,pady = 5)
        libPhysLogo(frame1)
        unlLogo(frame1)

        StatButton = Button(frame1, text="Statistics", command=lambda: controller.show_frame("StatWindow"))
        StatButton.pack(side=RIGHT, fill=BOTH, expand=False,padx = 5)

        label = Label(frame1, text="CoP Standing FFT")
        label.pack(side=RIGHT, fill=BOTH, expand=True)

        frame2 = Frame(self)
        frame2.pack(side=TOP, fill=X)

        drawFFT(frame2,freqPlot,abs(Y),"Standing center of pressure path FFT")

        frame3 = Frame(self)
        frame3.pack(side=TOP, fill=X)

        PathButton = Button(frame3, text="COP Path", command = lambda:controller.show_frame("COPWindow"))
        PathButton.pack(side=RIGHT, fill=BOTH, expand=False)

        FFTandCOPButton = Button(frame3, text="COP Path and FFT", command=lambda: controller.show_frame("COPandFFTWindow"))
        FFTandCOPButton.pack(side=RIGHT, fill=BOTH, expand=False)



class COPandFFTWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        #Frame1

        frame1 = Frame(self)
        frame1.pack(side = TOP,fill = X,pady = 5)
        libPhysLogo(frame1)
        unlLogo(frame1)


        label = Label(frame1, text="CoP Standing FFT")
        label.pack(side=RIGHT, fill=BOTH, expand=True)

        frame2 = Frame(self)
        frame2.pack(side=TOP, fill=X)

        drawFFTAndPath(frame2,COPx,COPy,freqPlot,abs(Y), "Standing center of pressure path","Standing center of pressure path FFT")

        frame3 = Frame(self)
        frame3.pack(side=TOP, fill=X)

        FFTButton = Button(frame3, text="COP FFT", command=lambda: controller.show_frame("COPFFTWindow"))
        FFTButton.pack(side=RIGHT, fill=BOTH, expand=False)

        PathButton = Button(frame3, text="COP Path", command = lambda:controller.show_frame("COPWindow"))
        PathButton.pack(side=RIGHT, fill=BOTH, expand=False)

class StatWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame1 = Frame(self)
        frame1.pack(side=TOP, fill=X ,pady = 5)
        libPhysLogo(frame1)
        unlLogo(frame1)

        COPButton = Button(frame1, text="CoP Plot", command=lambda: controller.show_frame("COPWindow"))
        COPButton.pack(side=RIGHT, fill=BOTH, expand=False)

        label = Label(frame1, text="CoP Statistics")
        label.pack(side=RIGHT, fill=BOTH, expand=True)

        frame2 = Frame(self)
        frame2.pack(side=TOP, fill=X)

        label2 = Label(frame2, text="CoP Statistics")
        label2.pack(side=RIGHT, fill=BOTH, expand=True)




# Other functions



def uploadData(data):
    TL = []
    TR = []
    BL = []
    BR = []
    TW = []
    time = []

    lines = data.readlines()[1:]

    for line in lines:
        tempLine = line.split(';')
        if len(tempLine)<5:
            TL.append(float(tempLine[0]))
            TR.append(float(tempLine[1]))
            BL.append(float(tempLine[2]))
            BR.append(float(tempLine[3]))
            time.append(float(tempLine[4]))
        else:
            TL.append(float(tempLine[0]))
            TR.append(float(tempLine[1]))
            BL.append(float(tempLine[2]))
            BR.append(float(tempLine[3]))
            TW.append(float(tempLine[4]))
            time.append(float(tempLine[5]))

    return [TL, TR, BL, BR, TW, time]

def getData(Data):
    [TL, TR, BL, BR, TW, time] = uploadData(Data)
    [COPx, COPy] = getCorrectedCOP(0, TL, TR, BL, BR)
    [COPmaxx, COPminx, COPmaxy, COPminyx] = maxSwayEachAxis(COPx,COPy)
    FS = getFS(time)

    [freqPlot, Y] = COPfft(COPx, FS)
    return [FS, COPx, COPy, COPmaxx, COPminx, COPmaxy, COPminyx, freqPlot, Y]
#MainFunction

if __name__ == "__main__":

    Data = open('Data/Joao.txt')
    [FS, COPx, COPy, COPmaxx, COPminx, COPmaxy, COPminyx, freqPlot, Y] = getData(Data)
    app = WiiBoardProcApp()
    app.geometry("700x560")
    app.resizable(width=FALSE,height=FALSE) #Lock the size of the window
    app.mainloop()
