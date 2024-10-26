import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def PlotPlate (raw, plate_time, plate_format = 96, f_size = 5, fill = False):

    def generate_wells(rows, cols):
        wells = []
        for r in rows:
            for c in cols:
                wells.append(f'{r}{c}')
        return wells

    if plate_format == 96:
        rows = list('ABCDEFGH')
        cols = [f'{i:02}' for i in range(1, 13)]
        n_row = 8
        n_col = 12
    elif plate_format == 384:
        rows = list('ABCDEFGHIJKLMNOP')
        cols = [f'{i:02}' for i in range(1, 25)]
        n_row = 16
        n_col = 24
    else:
        raise ValueError("Invalid format. Must be either 96 or 384")

    all_wells = generate_wells(rows, cols)

    if fill:
        missing_wells = set(all_wells) - set(raw.columns[2:])
        for well in missing_wells:
            raw[well] = 0

    well_order = list(raw.columns[:2]) + all_wells
    raw = raw[well_order]

    rawplot = raw.iloc[1:, 2:]
    vectors_long = np.repeat(rawplot.columns, repeats=len(rawplot))

    rawplot.insert(0, 'Time', plate_time['Time'])
    rawplot.columns.values[0] = "Time"
    rawplot = rawplot.apply(pd.to_numeric)

    long_data = pd.melt(rawplot, id_vars=['Time'], var_name='Variable', value_name='Value')
    long_data['Variable'] = vectors_long
    long_data['Value'] = pd.to_numeric(long_data['Value'], errors='coerce')

    global_max = long_data['Value'].max(skipna=True) / 0.8

    plt.figure(figsize=(n_col * 1, n_row * 1.5))
    for idx, (well, group) in enumerate(long_data.groupby('Variable')):
        plt.subplot(n_row, n_col, idx + 1)
        plt.plot(group['Time'], group['Value'], color='b')
        plt.ylim(0, global_max)
        plt.title(well, fontsize=f_size)
        plt.xticks([])
        plt.yticks([])
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.show()
