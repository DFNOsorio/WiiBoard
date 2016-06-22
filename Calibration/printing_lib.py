import seaborn
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def regular_plot(x, y, title, xlabel, ylabel, fontsize=14, plot_line='-'):
    fig = plt.figure()
    plt.plot(x, y, plot_line)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=fontsize)

    return fig


def subplot_overlap(x, y, title, xlabel, ylabel, lines, columns, legend=[], fontsize=[14]):
    fig = plt.figure()
    axes = []
    if (columns*lines) >= len(y):
        if isinstance(fontsize, int ):
            fontsize = [fontsize]
            [[fontsize.append(fontsize[0])] for _ in xrange(0, len(x))]
        elif len(fontsize) is 1:
            [[fontsize.append(fontsize[0])] for _ in xrange(0, len(x))]
        for i in range(0, len(x)):
            xx = x[i]
            yy = y[i]
            temp_ax = plt.subplot(lines, columns, i + 1)
            for j in range(0, len(yy)):
                plt.plot(xx, yy[j])
            plt.xlabel(xlabel[i])
            plt.ylabel(ylabel[i])
            plt.title(title[i], fontsize=fontsize[i])
            if len(legend) is not 0:
                plt.legend(legend[i], fontsize=5)
            axes.append(temp_ax)

        return fig, axes
    else:
        print "Wrong configuration"


def grid():

    f = plt.figure()

    gs1 = GridSpec(2, 2)
    gs1.update(left=0.05, right=0.38, wspace=0.3, hspace=0.2)

    ax1 = plt.subplot(gs1[0, -1])
    ax2 = plt.subplot(gs1[0, -2])

    ax3 = plt.subplot(gs1[-1, -1])
    ax4 = plt.subplot(gs1[-1, -2])

    gs3 = GridSpec(2, 2)
    gs3.update(left=0.45, right=0.78, wspace=0.3, hspace=0.2)
    ax5 = plt.subplot(gs3[0, -1])
    ax6 = plt.subplot(gs3[0, -2])

    ax7 = plt.subplot(gs3[-1, -1])
    ax8 = plt.subplot(gs3[-1, -2])

    gs2 = GridSpec(2, 2)
    gs2.update(left=0.81, right=0.98, hspace=0.1)
    ax9 = plt.subplot(gs2[:, :])

    plt.subplots_adjust(hspace=0.1, top=0.95, bottom=0.04)

    return f, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9


def ax9_populator(filler, ax):

    for i in range(0, len(filler[1])):
        ax.plot(filler[0][i], filler[1][i])

    for label in ax.get_xticklabels():
        label.set_fontsize(10)
    for label in ax.get_yticklabels():
        label.set_fontsize(10)

    ax.set_xlabel(filler[2])
    ax.set_ylabel(filler[3])
    ax.set_title(filler[4], fontsize=12)
    ax.legend(filler[5], fontsize=10)
    ax.text(25, 8, filler[6],
            horizontalalignment='left',
            verticalalignment='center',
            bbox=dict(boxstyle="square",
                      ec="0.5",
                      fc="gray",
                      alpha=0.2
                      )
            )
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
    ax.set_title(data[4], fontsize=12)
    ax.legend(data[5], fontsize=10)

    return ax


def add_vlines(axis, intervals, maximum, time):
    for i in range(0, len(axis)):
        for j in intervals:
            axis[i].axvline(x=time[j[0]], ymin=0, ymax=maximum[i], linestyle='--')
            axis[i].axvline(x=time[j[1]], ymin=0, ymax=maximum[i], linestyle='--')
    return axis


def add_hlines(axis, intervals, means, time):
    for i in range(0, len(axis)):
        means_axis = means[i]
        previous_legend = axis[i].get_legend().get_texts()
        new_legend = []
        for j in range(0, len(previous_legend)):
            new_legend.append(previous_legend[j].get_text())

        for j in range(0, len(intervals)):
            means_interval = means_axis[j]
            for t in means_interval:
                axis[i].plot([time[intervals[j][0]], time[intervals[j][1]]], [t, t], 'k')
                axis[i].set_xlim([0, time[len(time)-1]])
        new_legend.append("INT MEAN")
        axis[i].legend(new_legend)
    return axis


def add_sup_title(figure, title, fontsize=20):
    figure.suptitle(title, fontsize=fontsize)
    return figure


def plot_show_all():
    plt.show()

