import matplotlib.pyplot as plt
import numpy as np


def plot_raw_single(raw, sample, legend_position="upper left",
                    xlim=None, ylim=None, custom_colors=None,
                    xlab="Time (h)", ylab="Fluorescence",
                    linetypes=None, ax=None):

    time = np.array(raw.index, dtype=float)

    sel = [j for j, col_name in enumerate(raw.columns) if col_name.startswith(sample)]

    if ylim is None:
        ymax = np.nanmax(raw.iloc[:, sel].values)
        ylim = (0, ymax / 0.8)

    if xlim is None:
        xlim = (np.nanmin(time), np.nanmax(time))

    if custom_colors is None:
        colors_to_use = plt.get_cmap("tab10")(np.linspace(0, 1, len(sel)))
    else:
        colors_to_use = (custom_colors * ((len(sel) // len(custom_colors)) + 1))[:len(sel)]

    if linetypes is None:
        linetypes = ['-'] * len(sel)
    else:
        linetypes = (linetypes * ((len(sel) // len(linetypes)) + 1))[:len(sel)]

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    not_na_indices = ~raw.iloc[:, sel[0]].isna()
    ax.plot(time[not_na_indices.values], raw.iloc[not_na_indices.values, sel[0]],
            color=colors_to_use[0], linestyle=linetypes[0], label=f"1")

    for i in range(1, len(sel)):
        not_na_indices = ~raw.iloc[:, sel[i]].isna()
        ax.plot(time[not_na_indices.values], raw.iloc[not_na_indices.values, sel[i]],
                color=colors_to_use[i], linestyle=linetypes[i], label=f"{i + 1}")

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.legend(loc=legend_position, frameon=False)