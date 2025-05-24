import matplotlib.pyplot as plt
import numpy as np


def plot_raw_multi(raw, samples, legend_position="upper left",
                   xlim=None, ylim=None, custom_colors=None,
                   xlab="Time (h)", ylab="Fluorescence",
                   linetypes=None, ax=None):

    time = np.array(raw.index, dtype=float)

    if ylim is None:
        ymax = np.nanmax(raw.values)
        ylim = (0, ymax / 0.8)

    if xlim is None:
        xlim = (np.nanmin(time), np.nanmax(time))

    if custom_colors is None:
        colors_to_use = plt.get_cmap("tab10")(np.linspace(0, 1, len(samples)))
    else:
        colors_to_use = (custom_colors * ((len(samples) // len(custom_colors)) + 1))[:len(samples)]

    if linetypes is None:
        linetypes = ['-'] * len(samples)
    else:
        linetypes = (linetypes * ((len(samples) // len(linetypes)) + 1))[:len(samples)]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    for i, sample in enumerate(samples):
        sample_indices = [j for j, col_name in enumerate(raw.columns) if sample in col_name]
        for j in sample_indices:
            not_na_indices = ~raw.iloc[:, j].isna()
            ax.plot(time[not_na_indices.values], raw.iloc[not_na_indices.values, j],
                    color=colors_to_use[i], linestyle=linetypes[i])

    ax.legend(samples, loc=legend_position, frameon=False)