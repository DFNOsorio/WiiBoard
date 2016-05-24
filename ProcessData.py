import matplotlib
import seaborn

from NOVAWiiBoard import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure



from Tkinter import *
from PIL import Image, ImageTk


# Main Window Definitions




class COPWindow(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()



    def init_window(self):
        self.master.title("Wii Balance Board Data Processor")

        self.pack(fill = BOTH, expand = 1)
        f = Figure()
        a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self)

        #Frame1

        frame1 = Frame(self)
        frame1.pack(side = TOP,fill = X)
        self.libPhysLogo(frame1)
        self.unlLogo(frame1)

        Video = Button(frame1, text="Animation")
        Video.pack(side=RIGHT, fill=BOTH, expand=False)

        label = Label(frame1, text="COP Plots")
        label.pack(side=RIGHT, fill=BOTH, expand=True)


        #Menus
        menu = Menu(self.master)
        self.master.config(menu = menu)

        file = Menu(menu)

        file.add_command(label= "Exit", command = self.client_exit)
        menu.add_cascade(label = "File", menu = file)

        edit = Menu(menu)
        edit.add_command(label = "Undo")
        menu.add_cascade(label = "Edit", menu = edit)



        self.drawPlot(COPx, COPy, a ,canvas)

    def client_exit(self):
        exit()

    def libPhysLogo(self,frame):
        load = Image.open("Images/logo_libphys.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame,image = render)
        img.image = render
        img.pack(side=LEFT, fill = BOTH, expand = False, padx = 5)

    def unlLogo(self, frame):
        load = Image.open("Images/UNL.gif")
        render = ImageTk.PhotoImage(load)
        img = Label(frame, image=render)
        img.image = render
        img.pack(side=LEFT, fill=BOTH, expand=False, padx=5)

    def drawPlot(self, x, y, a,canvas):
        a.plot(x, y)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)





# Other functions



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



#MainFunction

if __name__ == "__main__":

    Data = open('Data/Raw_Tue_15:22:47.txt')
    [TL, TR, BL, BR, time] = uploadData(Data)
    [COPx, COPy] = getCorrectedCOP(100,TL, TR, BL, BR)


    root = Tk()
    root.geometry("700x680")

    app = COPWindow(root)
    root.mainloop()
