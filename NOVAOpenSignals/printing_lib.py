import seaborn
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.misc import imread


def regular_plot(x, y, title, xlabel, ylabel, fontsize=14, plot_line='-'):
    fig = plt.figure()
    plt.plot(x, y, plot_line)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=fontsize)

    return fig


# noinspection PyStatementEffect
def subplot_overlap(x, y, title, xlabel, ylabel, lines, columns, legend=[], fontsize=[14], overlapx=False, wii=False):
    fig = plt.figure()
    axes = []
    wii_location = wii
    if (columns*lines) >= len(x):
        if isinstance(fontsize, int):
            fontsize = [fontsize]
            [[fontsize.append(fontsize[0])] for _ in xrange(0, len(x))]
        elif len(fontsize) is 1:
            [[fontsize.append(fontsize[0])] for _ in xrange(0, len(x))]
        for i in range(0, len(x)):
            xx = x[i]
            yy = y[i]
            temp_ax = plt.subplot(lines, columns, i + 1)
            for j in range(0, len(yy)):
                if isinstance(wii_location, list):
                    if len(wii_location) > 0 and wii_location[0] == i+1:
                        add_wii(temp_ax)
                        wii_location.pop(0)

                if overlapx and (len(xx) != len(yy[j])):
                    temp_ax.plot(xx[j], yy[j], label='test'+str(j))
                else:
                    temp_ax.plot(xx, yy[j], label='test'+str(j))

            temp_ax.set_xlabel(xlabel[i])
            temp_ax.set_ylabel(ylabel[i])
            temp_ax.set_title(title[i], fontsize=fontsize[i])
            if len(legend) is not 0:
                temp_ax.legend(legend[i], fontsize=10)
            axes.append(temp_ax)

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


def axe_populator(data, ax):
    x = data[0]
    yy = data[1]

    for j in range(0, len(yy)):
        ax.plot(x, yy[j])
    for label in ax.get_xticklabels():
        label.set_fontsize(10)

    for label in ax.get_yticklabels():
        label.set_fontsize(10)

    ax.set_xlabel(data[2])
    ax.set_ylabel(data[3])
    ax.set_title(data[4], fontsize=14)
    ax.legend(data[5], fontsize=10)

    return ax


def add_vlines(axis, intervals, maximum, time):
    for i in range(0, len(axis)):
        for j in intervals:
            axis[i].axvline(x=time[j[0]], ymin=0, ymax=maximum[i], linestyle='--')
            axis[i].axvline(x=time[j[1]], ymin=0, ymax=maximum[i], linestyle='--')
    return axis


def add_hlines(axis, intervals, means, time, linestyle='-', linecolor="k", legendText="INT MEAN"):
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
                axis[i].plot([time[intervals[j][0]], time[intervals[j][1]]], [t, t], linestyle+linecolor, label="NEW"+str(j))
                axis[i].set_xlim([0, time[len(time)-1]])
        h, l = axis[i].get_legend_handles_labels()
        h[len(previous_legend)].set_color(linecolor)
        new_legend.append(legendText)
        axis[i].legend(new_legend, fontsize=10)
    return axis


def add_sup_title(figure, title, fontsize=20):
    figure.suptitle(title, fontsize=fontsize)
    return figure


def plot_show_all():
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()


def add_wii(axis):
    img = imread("../Images/Wii.JPG")
    axis.imshow(img, zorder=0, extent=[-216 - 26, 216 + 26, -114 - 26, 114 + 26])

    axis.set_xlim([-216 - 30, 216 + 30])
    axis.set_ylim([-114 - 30, 114 + 30])
    axis.set_xlabel("CoPx (mm)", fontsize=14)
    axis.set_ylabel("CoPy (mm)", fontsize=14)