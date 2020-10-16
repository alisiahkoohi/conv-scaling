import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

sfmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
sfmt.set_powerlimits((0, 0))
font = {'family': 'serif', 'size': 6}
matplotlib.rc('font', **font)


def img_size(n):
    return [2**(5 + j) for j in range(n)]


def input_data(filenames):

    info = {}
    for file in filenames:

        info[file] = {"nch": set(), "k": set(), "n": set()}

        with open(os.path.join('logs/', file)) as f:
            for content in f.readlines():

                nch, k, n, run_time, memory = content.rstrip().split(',')

                nch, k, n, run_time, memory = (2**int(nch), int(k), 2**int(n),
                                               float(run_time), float(memory))

                if not (run_time, memory) == (-1.0, -1.0):

                    info[file]["nch"].add(nch)
                    info[file]["k"].add(k)
                    info[file]["n"].add(n)

                    info[file][nch, k, n] = (run_time, memory/(1024**2))

        info[file]["nch"] = np.sort(list(info[file]["nch"]))
        info[file]["k"] = np.sort(list(info[file]["k"]))
        info[file]["n"] = np.sort(list(info[file]["n"]))

    return info


if __name__ == '__main__':

    filenames = ['devito-conv.txt',
                 'torch-conv.txt']

    info = input_data(filenames)

    colors = [(0.0, 0.0, 0.0),
              (0.0, 0.584, 1.0),
              (1.0, 0.0, 0.286),
              (0.0, 0.584, 0.239),
              '#c2c22f',
              '#8a8a8a',
              '#a1c0ff',
              '#ff9191',
              '#91eda2',
              '#ffff61']

    figs = []
    axs = []
    for j, file in enumerate(info.keys()):
        for r, nch in enumerate(info[file]["nch"]):

            if j == 0:
                fig, ax = plt.subplots(figsize=(8, 3))
                figs.append(fig)
                axs.append(ax)

            for i, k in enumerate(info[file]["k"]):

                run_times = []
                n_list = []

                for n in info[file]["n"]:
                    if (nch, k, n) in info[file].keys():

                        run_times.append(info[file][nch, k, n][0])
                        n_list.append(n)
                        axs[r].scatter(n, info[file][nch, k, n][0],
                                       color=colors[5*j + i], s=0.8)

                axs[r].plot(n_list, run_times, color=colors[5*j + i],
                            linewidth=0.7,
                            label=(file[:file.find('-')] + " — "
                                   + r"$k={{{}}}$".format(k)))

            axs[r].legend(fontsize=6, ncol=2, loc='upper left')
            axs[r].set_ylabel("wall-clock time (s)", fontsize=8)
            axs[r].set_xlabel(r"$n$", fontsize=10)
            axs[r].set_title("50 calls to a " + r"$k \times k \ conv$"
                             + " — image size: "
                             + r"$n \times n \times {{{}}}$".format(nch))
            axs[r].set_xscale('log')
            axs[r].set_yscale('log')
            axs[r].set_xlim([2e1, 2e4])
            axs[r].set_ylim([3e-1, 2e3])
            ax.grid(True, which="both", ls="-", alpha=.2)

    for j, fig in enumerate(figs):
        fig.savefig(os.path.join('figs/', ('runtime_nch%d' % j)),
                    format='png', bbox_inches='tight',
                    dpi=400, pad_inches=.05)
        plt.close(fig)

    figs = []
    axs = []
    for j, file in enumerate(info.keys()):
        for r, nch in enumerate(info[file]["nch"]):

            if j == 0:
                fig, ax = plt.subplots(figsize=(8, 3))
                figs.append(fig)
                axs.append(ax)

            for i, k in enumerate(info[file]["k"]):

                memory = []
                n_list = []

                for n in info[file]["n"]:
                    if (nch, k, n) in info[file].keys():

                        memory.append(info[file][nch, k, n][1])
                        n_list.append(n)
                        axs[r].scatter(n, info[file][nch, k, n][1],
                                       color=colors[j], s=0.8)

                if k == 3:
                    label = (file[:file.find('-')] + r", $k=3, 5, 7, 9, 11$")
                else:
                    label = '_no_label_'
                axs[r].plot(n_list, memory, color=colors[j],
                            linewidth=0.3, label=label, alpha=0.7)

            axs[r].legend(fontsize=6, ncol=2, loc='upper left')
            axs[r].set_ylabel("Memory (GB)", fontsize=8)
            axs[r].set_xlabel(r"$n$", fontsize=10)
            axs[r].set_title("50 calls to a " + r"$k \times k \ conv$"
                             + " — image size: "
                             + r"$n \times n \times {}$".format(int(nch)))
            axs[r].set_xscale('log')
            axs[r].set_yscale('log')
            axs[r].set_xlim([2e1, 2e4])
            axs[r].set_ylim([7e-2, 1e2])
            ax.grid(True, which="both", ls="-", alpha=.2)

    for j, fig in enumerate(figs):
        fig.savefig(os.path.join('figs/', ('memory_nch%d' % j)),
                    format='png', bbox_inches='tight',
                    dpi=400, pad_inches=.05)
        plt.close(fig)
