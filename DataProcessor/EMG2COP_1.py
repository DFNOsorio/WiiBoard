from DataProcessor.processing_methods import wii_smoother
import matplotlib.pyplot as plt
from novainstrumentation import smooth
import numpy as np
import os

def EMG_diferential(data, patient):
    fig1 = plt.figure(1)

    fig2 = plt.figure(2)
    for i in range(0, len(data)):

        open_signal_data = data[i].get_variable('open_signals_data_filtered')

        EMGs = data[i].get_variable('smoothed_data_filtered')
        wii = data[i].get_variable("wii_data")
        wii[6] = wii_smoother(wii[6], [10, 10, 10])

        EMGs = normalize_1(EMGs)

        Front = (EMGs[0] + EMGs[1])
        Back = (EMGs[2] + EMGs[3])
        Left = (EMGs[1] + EMGs[2])
        Right = (EMGs[0] + EMGs[3])

        x = (Left - Right)[100:-100]
        y = (Front - Back)[100:-100]

        [x, y] = normalize_1([x, y])

        Acc_ = open_signal_data[5:8]
        Acc = []
        Acc.append(list(smooth(np.array(Acc_[2]), 500))[100:-100])
        Acc.append(list(smooth(np.array(Acc_[0]), 500))[100:-100])

        Acc = normalize_1(Acc)
        Cops=[]
        Cops.append(wii[6][0][10:-10])
        Cops.append(wii[6][1][10:-10])
        Cops = normalize_1(Cops)

        #SEPARAR
        plt.figure(1)
        t1 = np.linspace(0, len(Acc[1]), len(Cops[0]))

        plt.subplot(3, 4, i + 1)
        l1, = plt.plot(x, y, color='red')
        l2, = plt.plot(Cops[0], Cops[1], color='blue')
        l3, = plt.plot(Acc[0], Acc[1], color='black', alpha=0.2)
        plt.xlabel("Norm x")
        plt.ylabel("Norm y")

        plt.subplot(3, 4, i + 5)
        plt.plot(x, color='red')
        plt.plot(t1, Cops[0], color='blue')
        plt.plot(Acc[0], color='black', alpha=0.2)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm x")
        plt.title("X Axis")

        plt.subplot(3, 4, i + 9)
        plt.plot(y, color='red')
        plt.plot(t1, Cops[1], color='blue')
        plt.plot(Acc[1], color='black', alpha=0.2)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm y")
        plt.title("Y Axis")

        Acc[0] = list(smooth(np.array(Acc[0]), 1000))
        Acc[1] = list(smooth(np.array(Acc[1]), 1000))
        Cops[0] = list(smooth(np.array(Cops[0]), 100))
        Cops[1] = list(smooth(np.array(Cops[1]), 100))
        x = list(smooth(np.array(x), 1000))
        y = list(smooth(np.array(y), 1000))

        plt.figure(2)
        t1 = np.linspace(0, len(Acc[1]), len(Cops[0]))

        plt.subplot(3, 4, i + 1)
        l1, = plt.plot(x, y, color='red')
        l2, = plt.plot(Cops[0], Cops[1], color='blue')
        l3, = plt.plot(Acc[0], Acc[1], color='black', alpha=0.2)
        plt.xlabel("Norm x")
        plt.ylabel("Norm y")

        plt.subplot(3, 4, i + 5)
        plt.plot(x, color='red')
        plt.plot(t1, Cops[0], color='blue')
        plt.plot(Acc[0], color='black', alpha=0.2)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm x")
        plt.title("X Axis")

        plt.subplot(3, 4, i + 9)
        plt.plot(y, color='red')
        plt.plot(t1, Cops[1], color='blue')
        plt.plot(Acc[1], color='black', alpha=0.2)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm y")
        plt.title("Y Axis")

    plt.figure(1)
    fig1.suptitle(patient, fontsize=20)
    fig1.legend((l1, l2, l3), ('EMG', 'COP', 'ACC'), loc='lower center', ncol=4, labelspacing=0., fontsize=14)
    plt.subplots_adjust(hspace=0.26, wspace=0.24, top=0.94, bottom=0.07, left=0.04, right=0.98)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    plt.figure(2)
    fig2.suptitle(patient, fontsize=20)
    fig2.legend((l1, l2, l3), ('EMG', 'COP', 'ACC'), loc='lower center', ncol=4, labelspacing=0., fontsize=14)
    plt.subplots_adjust(hspace=0.26, wspace=0.24, top=0.94, bottom=0.07, left=0.04, right=0.98)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    if not os.path.exists('../WiiBoard/DataProcessor/Images/Cops_gen/' + patient+'/'):
        os.makedirs('../WiiBoard/DataProcessor/Images/Cops_gen/'+ patient+'/')

    fig1.set_size_inches(20, 11.25)
    fig2.set_size_inches(20, 11.25)
    plt.figure(1)
    plt.savefig('../WiiBoard/DataProcessor/Images/Cops_gen/' + patient +'/cops1.png', dpi=300)
    plt.figure(2)
    plt.savefig('../WiiBoard/DataProcessor/Images/Cops_gen/' + patient + '/cops2.png', dpi=300)
    plt.show()


def normalize_1(EMG_data):
    for i in range(0, len(EMG_data)):
        EMG_data[i] = (EMG_data[i]-min(EMG_data[i]))/(max(EMG_data[i])-min(EMG_data[i]))
    return EMG_data


