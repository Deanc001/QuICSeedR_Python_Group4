import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def PlotRawSingle(raw, sample, legend_position="upper left", xlim=None, ylim=None, custom_colors=None,
                 xlab="Time (h)", ylab="Fluorescence", linetypes=None):
    
    time = raw.index.to_numpy(dtype=float)
    sel = raw.columns.str.contains(f'^{sample}')
    
    if ylim is None:
        ymax = raw.loc[:, sel].max().max()
        ylim = (0, ymax / 0.8)
        
    if xlim is None:
        xlim = (time.min(), time.max())
        
    if custom_colors is None:
        colors_to_use = plt.cm.tab10(np.arange(sel.sum()))
    else:
        colors_to_use = np.resize(custom_colors, sel.sum())
        
    if linetypes is None:
        linetypes = ['solid'] * sel.sum()
    else:
        linetypes = np.resize(linetypes, sel.sum())
        
    plt.figure(figsize=(8, 6))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
    columns_sel = raw.columns[sel]
    valid_indices = ~raw[columns_sel[0]].isna()
    plt.plot(time[valid_indices], raw.loc[valid_indices, columns_sel[0]],
             label=sample, color=colors_to_use[0], linestyle=linetypes[0])
    
    
    for i in range(1, len(columns_sel)):
        valid_indices = ~raw[columns_sel[i]].isna()
        plt.plot(time[valid_indices], raw.loc[valid_indices, columns_sel[i]],
                 label=f'{sample} {i+1}', color=colors_to_use[i], linestyle=linetypes[i])
        
    plt.legend(loc=legend_position, fontsize=8)
    plt.show()
