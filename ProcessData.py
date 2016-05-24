import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from Tkinter import *
from PIL import Image, ImageTk
import numpy as np

# Main Window Definitions

class Window(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()
        self.LibPhysLogo()


    def init_window(self):
        self.master.title("Wii Balance Board Data Processor")

        self.pack(fill = BOTH, expand = 1)

        quitButton = Button(self, text = "Quit", command = self.client_exit)

        quitButton.place(x=640, y=400)

        menu = Menu(self.master)
        self.master.config(menu = menu)

        file = Menu(menu)

        file.add_command(label= "Exit", command = self.client_exit)
        menu.add_cascade(label = "File", menu = file)

        edit = Menu(menu)
        edit.add_command(label = "Undo")
        menu.add_cascade(label = "Edit", menu = edit)


    def client_exit(self):
        exit()

    def LibPhysLogo(self):
        load = Image.open("Images/logo_libphys.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self,image = render)
        img.image = render
        img.place(x=0,y=0)


# Data Processing Fuctions

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





if __name__ == "__main__":

    Data = open('Data/PreMarks/Raw_Mon_16:22:19')
    [TL, TR, BL, BR, time] = uploadData(Data)


    root = Tk()
    root.geometry("640x400")

    app = Window(root)
    root.mainloop()
