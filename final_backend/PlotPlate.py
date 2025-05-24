import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_plate(raw, plate_time, format=96, f_size=5, fill=False):
    def generate_wells(rows, cols):
        wells = []
        for r in rows:
            for c in cols:
                wells.append(f"{r}{c}")
        return wells

    if format == 96:
        rows = [chr(i) for i in range(ord('A'), ord('H') + 1)]
        cols = [f"{i:02}" for i in range(1, 13)]
        n_row, n_col = 8, 12
    elif format == 384:
        rows = [chr(i) for i in range(ord('A'), ord('P') + 1)]
        cols = [f"{i:02}" for i in range(1, 25)]
        n_row, n_col = 16, 24
    else:
        raise ValueError("Invalid format. Must be either 96 or 384.")

    all_wells = generate_wells(rows, cols)

    if fill:
        missing_wells = set(all_wells) - set(raw.columns[2:])
        for well in missing_wells:
            raw[well] = 0

    well_order = list(raw.columns[:2]) + all_wells
    raw = raw[well_order]
    rawplot = raw.iloc[1:, 2:]
    rawplot.insert(0, "Time", plate_time.iloc[:, 0])
    rawplot = rawplot.apply(pd.to_numeric, errors='coerce')
    long_data = pd.melt(rawplot, id_vars="Time", var_name="Well", value_name="Fluorescence")
    long_data["Fluorescence"] = pd.to_numeric(long_data["Fluorescence"])
    global_max = long_data["Fluorescence"].max(skipna=True) / 0.8

    fig = plt.figure(figsize=(12, 8))
    gs = plt.GridSpec(n_row, n_col, figure=fig, wspace=0.05, hspace=0.35)

    for i, well in enumerate(all_wells):
        row, col = divmod(i, n_col)
        ax = fig.add_subplot(gs[row, col])

        well_data = long_data[long_data["Well"] == well]
        sns.lineplot(x="Time", y="Fluorescence", data=well_data, ax=ax, color="black", linewidth=0.8)

        ax.set_ylim(0, global_max)
        ax.set_title(well, fontsize=8)
        ax.tick_params(axis="both", which="both", length=0)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlabel('')
        ax.set_ylabel('')

    plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)

    fig.text(0.5, 0.04, 'Time', ha='center', fontsize=14)
    fig.text(0.04, 0.5, 'Fluorescence', va='center', rotation='vertical', fontsize=14)

    plt.show()


def interactive_plot_plate(raw, plate_time, format=96, f_size=10):

    if format == 96:
        rows = [chr(i) for i in range(ord('A'), ord('H') + 1)]
        cols = [f"{i:02}" for i in range(1, 13)]
        n_row, n_col = 8, 12
    elif format == 384:
        rows = [chr(i) for i in range(ord('A'), ord('P') + 1)]
        cols = [f"{i:02}" for i in range(1, 25)]
        n_row, n_col = 16, 24
    else:
        raise ValueError("Invalid format. Must be either 96 or 384.")

    fig = make_subplots(
        rows=n_row, cols=n_col,
        shared_xaxes=True, shared_yaxes=True,
        vertical_spacing=0.02, horizontal_spacing=0.02
    )

    time = plate_time.iloc[:, 0].values

    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            well = f"{row}{col}"
            if well in raw.columns:
                y_data = raw[well].values
                trace = go.Scatter(x=time, y=y_data, mode='lines', line=dict(width=1), showlegend=False)
                fig.add_trace(trace, row=n_row - i, col=j + 1)

    annotations = []
    for i, row_label in enumerate(rows):
        annotations.append(dict(
            x=-0.05, y=(n_row - i - 0.5) / n_row,
            xref="paper", yref="paper",
            text=row_label,
            showarrow=False,
            font=dict(size=f_size, color="black")
        ))

    for j, col_label in enumerate(cols):
        annotations.append(dict(
            x=(j + 0.5) / n_col, y=1.05,
            xref="paper", yref="paper",
            text=col_label,
            showarrow=False,
            font=dict(size=f_size, color="black")
        ))

    fig.update_layout(
        title_text=None,
        height=900,
        width=1400,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        annotations=annotations
    )

    fig.update_xaxes(title_text=" ", row=n_row, col=1)
    fig.update_yaxes(title_text=" ", row=1, col=1)

    return fig