from DataProcessor.processing_methods import wii_smoother
import matplotlib.pyplot as plt
from novainstrumentation import smooth
import numpy as np

def EMG_diferential(data):

    for i in range(0, len(data)):
        fig = plt.figure()
        open_signal_data = data[i].get_variable('open_signals_data_filtered')

        EMGs = data[i].get_variable('smoothed_data_filtered')
        wii = data[i].get_variable("wii_data")
        wii[6] = wii_smoother(wii[6], [10, 10, 10])


        Front = (EMGs[0] + EMGs[1])
        Back = (EMGs[2] + EMGs[3])
        Left = (EMGs[1] + EMGs[2])
        Right = (EMGs[0] + EMGs[3])

        x = (Left - Right)
        y = (Front - Back)

        [x, y] = normalize_1([x, y])

        Acc = open_signal_data[5:8]
        Acc[0] = list(smooth(np.array(Acc[0]), 500))
        Acc[1] = list(smooth(np.array(Acc[1]), 500))

        Acc = normalize_1(Acc)
        EMGs = normalize_1(EMGs)
        Cops = normalize_1(wii[6][0:2])

        #SEPARAR

        plt.subplot(4, 1, 1)
        plt.plot(x)
        plt.title("EMG x")

        plt.subplot(4, 1, 2)
        plt.plot(Acc[0])
        plt.title("Acc x")

        plt.subplot(4, 1, 3)
        plt.plot(y)
        plt.title("EMG y")

        plt.subplot(4, 1, 4)
        plt.plot(Acc[1])
        plt.title("Acc y")

        fig = plt.figure()
        plt.plot(x, y, color='red')
        plt.plot(Cops[0], Cops[1], color='blue')
        plt.plot(Acc[2], Acc[0], color='black', alpha=0.2)
        plt.legend(['EMG', 'COP', 'ACC'])


    plt.show()


def normalize_1(EMG_data):
    for i in range(0, len(EMG_data)):
        EMG_data[i] = (EMG_data[i]-min(EMG_data[i]))/(max(EMG_data[i])-min(EMG_data[i]))
    return EMG_data


