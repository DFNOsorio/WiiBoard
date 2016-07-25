import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


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


def grid_cops(text):

    f = plt.figure()
    plt.figtext(0.08, 0.95, text, fontsize=20)

    gs1 = GridSpec(3, 2)
    gs1.update(left=0.04, right=0.65, wspace=0.3, hspace=0.25)

    gs1_ax1 = plt.subplot(gs1[0, 0])
    gs1_ax2 = plt.subplot(gs1[0, 1])
    gs1_ax3 = plt.subplot(gs1[1, 0])
    gs1_ax4 = plt.subplot(gs1[1, -1])
    gs1_ax5 = plt.subplot(gs1[2, 0])
    gs1_ax6 = plt.subplot(gs1[2, -1])

    gs1_ax = [gs1_ax1, gs1_ax2, gs1_ax3, gs1_ax4, gs1_ax5, gs1_ax6]

    gs2 = GridSpec(2, 2)
    gs2.update(left=0.69, right=0.98, wspace=0.3, hspace=0.15)

    gs2_ax1 = plt.subplot(gs2[0, 0])
    gs2_ax2 = plt.subplot(gs2[0, -1])
    gs2_ax3 = plt.subplot(gs2[1, 0])
    gs2_ax4 = plt.subplot(gs2[1, -1])

    gs2_ax = [gs2_ax1, gs2_ax2, gs2_ax3, gs2_ax4]

    plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.03, right=0.98)

    return f, gs1_ax, gs2_ax


def grid_overlay(text):

    f = plt.figure()
    plt.figtext(0.08, 0.95, text, fontsize=20)

    gs1 = GridSpec(3, 2)
    gs1.update(left=0.04, right=0.65, wspace=0.3, hspace=0.25)

    gs1_ax1 = plt.subplot(gs1[0, 0])
    gs1_ax2 = plt.subplot(gs1[0, 1])
    gs1_ax3 = plt.subplot(gs1[1, 0])
    gs1_ax4 = plt.subplot(gs1[1, -1])
    gs1_ax5 = plt.subplot(gs1[2, 0])
    gs1_ax6 = plt.subplot(gs1[2, -1])

    gs1 = [gs1_ax1, gs1_ax2, gs1_ax3, gs1_ax4, gs1_ax5, gs1_ax6]

    gs2 = GridSpec(3, 2)
    gs2.update(left=0.69, right=0.98, wspace=0.3, hspace=0.15)

    gs2_ax1 = plt.subplot(gs2[0, :])
    gs2_ax2 = plt.subplot(gs2[1, 0])
    gs2_ax3 = plt.subplot(gs2[1, 1])
    gs2_ax4 = plt.subplot(gs2[2, 0])
    gs2_ax5 = plt.subplot(gs2[2, 1])

    gs2 = [gs2_ax1, gs2_ax2, gs2_ax3, gs2_ax4, gs2_ax5]

    plt.subplots_adjust(hspace=0.16, top=0.91, bottom=0.04, left=0.03, right=0.98)

    return f, gs1, gs2
