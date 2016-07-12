import seaborn
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from scipy.misc import imread
import numpy as np

def regular_plot(x, y, title, xlabel, ylabel, fontsize=14, plot_line='-', legend=[]):
    fig = plt.figure()
    plt.plot(x, y, plot_line)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=fontsize)
    plt.legend(legend)
    return fig


# noinspection PyStatementEffect
def subplot_overlap(x, y, title, xlabel, ylabel, lines, columns, legend=[], overlapx=False, wii=False, tight=False):
    fig = plt.figure()
    axes = []
    wii_location = wii
    if (columns * lines) >= len(x):
        for i in range(0, len(x)):
            xx = x[i]
            yy = y[i]
            temp_ax = plt.subplot(lines, columns, i + 1)
            for j in range(0, len(yy)):
                if isinstance(wii_location, list):
                    if len(wii_location) > 0 and wii_location[0] == i:
                        add_wii(temp_ax)
                        wii_location.pop(0)
                if overlapx and (len(xx) != len(yy[j])):
                    temp_ax.plot(xx[j], yy[j], label="test" + str(j))
                else:
                    temp_ax.plot(xx, yy[j], label="test" + str(j))
            temp_ax.set_xlabel(xlabel[i])
            temp_ax.set_ylabel(ylabel[i])
            temp_ax.set_title(title[i])
            if len(legend) is not 0:
                temp_ax.legend(legend[i], fontsize=10)
            axes.append(temp_ax)
        if tight:
            plt.subplots_adjust(hspace=0.33, top=0.91, bottom=0.04, left=0.04, right=0.98)
        return fig, axes
    else:
        print "Wrong configuration"


def grid(run):
    f = plt.figure()
    plt.figtext(0.08, 0.95, run, fontsize=20)
    gs1 = GridSpec(2, 4)

    ax1 = plt.subplot(gs1[0, :-2])
    ax6 = plt.subplot(gs1[0, -2:])

    ax2 = plt.subplot(gs1[-1, -3])
    ax3 = plt.subplot(gs1[-1, -2])
    ax4 = plt.subplot(gs1[-1, -1])
    ax5 = plt.subplot(gs1[-1, 0])

    plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.03, right=0.98)

    return f, ax1, ax2, ax3, ax4, ax5, ax6


def grid_report(text):

    f = plt.figure()
    plt.figtext(0.08, 0.95, text, fontsize=20)
    gs1 = GridSpec(3, 2)
    gs1.update(left=0.04, right=0.29, hspace=0.25)

    gs1_ax1 = plt.subplot(gs1[0, :])
    gs1_ax2 = plt.subplot(gs1[1, :])
    gs1_ax3 = plt.subplot(gs1[2, :])

    gs1_ax = [gs1_ax1, gs1_ax2, gs1_ax3]

    gs2 = GridSpec(3, 2)
    gs2.update(left=0.33, right=0.65, wspace=0.3, hspace=0.25)

    gs2_ax1 = plt.subplot(gs2[0, 0])
    gs2_ax2 = plt.subplot(gs2[0, 1])
    gs2_ax3 = plt.subplot(gs2[1, 0])
    gs2_ax4 = plt.subplot(gs2[1, -1])
    gs2_ax5 = plt.subplot(gs2[2, 0])
    gs2_ax6 = plt.subplot(gs2[2, -1])

    gs2_ax = [gs2_ax1, gs2_ax2, gs2_ax3, gs2_ax4, gs2_ax5, gs2_ax6]

    gs3 = GridSpec(2, 2)
    gs3.update(left=0.69, right=0.98, wspace=0.3, hspace=0.15)

    gs3_ax1 = plt.subplot(gs3[0, 0])
    gs3_ax2 = plt.subplot(gs3[0, -1])
    gs3_ax3 = plt.subplot(gs3[1, 0])
    gs3_ax4 = plt.subplot(gs3[1, -1])

    gs3_ax = [gs3_ax1, gs3_ax2, gs3_ax3, gs3_ax4]

    plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.03, right=0.98)

    return f, gs1_ax, gs2_ax, gs3_ax


def ax1_pop(filler, ax):
    add_wii(ax)
    for i in range(0, len(filler[1])):
        ax.plot(filler[0][i], filler[1][i])

    for label in ax.get_xticklabels():
        label.set_fontsize(8)
    for label in ax.get_yticklabels():
        label.set_fontsize(8)

    ax.set_xlabel(filler[2], fontsize=12)
    ax.set_ylabel(filler[3], fontsize=12)
    ax.set_title(filler[4], fontsize=20)
    ax.legend(filler[5], fontsize=12, bbox_to_anchor=(1.1, 1.05), fancybox=True)
    return ax


def axe_populator(data, ax, wii=False, xlim=[]):
    x = data[0]
    yy = data[1]
    if wii:
        add_wii(ax)
    for j in range(0, len(yy)):
        ax.plot(x, yy[j])

    for label in ax.get_xticklabels():
        label.set_fontsize(10)

    for label in ax.get_yticklabels():
        label.set_fontsize(10)
    if len(xlim) == 0:
        xlim = [x[0], x[-1]]
    ax.set_xlabel(data[2], fontsize=10)
    ax.set_ylabel(data[3], fontsize=10)
    ax.set_title(data[4], fontsize=14)
    if not wii:
        ax.set_xlim(xlim)
    ax.legend(data[5], fontsize=10)

    return ax


def add_vlines(axis, intervals, maximum, time):
    for i in range(0, len(axis)):
        for j in intervals:
            axis[i].axvline(x=time[j[0]], ymin=0, ymax=maximum[i], linestyle='--')
            axis[i].axvline(x=time[j[1]], ymin=0, ymax=maximum[i], linestyle='--')
    return axis


def add_hlines(axis, interval, y_value, legend_text, color='k', linestyle="--"):
    previous_legend = axis.get_legend().get_texts()
    new_legend = []
    for j in range(0, len(previous_legend)):
        new_legend.append(previous_legend[j].get_text())

    axis.axhline(y=y_value, xmin=interval[0], xmax=interval[1], label="NEW", color=color, linestyle=linestyle)
    axis.set_xlim(interval)
    h, l = axis.get_legend_handles_labels()
    h[len(previous_legend)].set_color(color)
    new_legend.append(legend_text)
    axis.legend(new_legend, fontsize=10)
    return axis


def add_hlines_intervals(axis, intervals, means, time, linestyle='-', linecolor="k", legendText="INT MEAN"):
    for i in range(0, len(axis)):
        means_axis = means[i]
        previous_legend = axis[i].get_legend().get_texts()
        new_legend = []
        for j in range(0, len(previous_legend)):
            new_legend.append(previous_legend[j].get_text())
        for j in range(0, len(intervals)):
            means_interval = means_axis[j]
            if type(means_interval) is not list:
                means_interval = [means_interval]
            for t in means_interval:
                axis[i].plot([time[intervals[j][0]], time[intervals[j][1]]], [t, t], linestyle + linecolor,
                             label="NEW" + str(j))
                axis[i].set_xlim([0, time[len(time) - 1]])
        h, l = axis[i].get_legend_handles_labels()
        h[len(previous_legend)].set_color(linecolor)
        new_legend.append(legendText)
        axis[i].legend(new_legend, fontsize=10)
    return axis


def add_sup_title(figure, title, fontsize=20):
    figure.suptitle(title, fontsize=fontsize)
    return figure


def plot_show_all():
    #mng = plt.get_current_fig_manager()
    #mng.window.showMaximized()
    plt.show()


def add_wii(axis):
    axis.grid(b=False)
    img = imread("../Images/Wii.JPG")
    #img = imread("../WiiBoard/Images/Wii.JPG")
    axis.imshow(img, zorder=0, extent=[-216 - 26, 216 + 26, -114 - 26, 114 + 26])

    axis.set_xlim([-216 - 30, 216 + 30])
    axis.set_ylim([-114 - 30, 114 + 30])
    axis.set_xlabel("CoPx (mm)", fontsize=14)
    axis.set_ylabel("CoPy (mm)", fontsize=14)


def add_indexes(axix, xx, yy, window):
    for i in range(0, len(xx)):
        axix.text(xx[i], yy[i] - 1000, window[i], fontsize=8, horizontalalignment='left',
                  verticalalignment='center',
                  bbox={'boxstyle': "square", 'ec': "0.5", 'fc': "gray", 'alpha': 0.2}
                  )


def add_newaxis(axis, xx, yy, label, linestyle='-', linecolor="k", legend='New'):
    ax2 = axis.twinx()
    ax2.plot(xx, yy, linestyle+linecolor, label="NEW")
    ax2.set_ylabel(label)
    ax2.legend(legend)

    previous_legend = axis.get_legend().get_texts()
    new_legend = []
    for j in range(0, len(previous_legend)):
        new_legend.append(previous_legend[j].get_text())

    h, l = ax2.get_legend_handles_labels()
    h1, l1 = axis.get_legend_handles_labels()

    ax2.legend("")
    new_legend.append(legend)
    axis.legend(handles=list(np.concatenate([h1, h])), labels=new_legend)

    return [axis, ax2]


def get_spectogram(x, fs, window_size):
    len(x)*1.0/fs
    Pxx, freqs, bins, im = plt.specgram(x, Fs=fs, NFFT=window_size, noverlap=0, cmap='jet')
    cbar = plt.colorbar(im)
    plt.xlim([0, len(x)*1.0/fs])

    return Pxx, freqs, bins, im