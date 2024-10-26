import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def PlotRawMulti(raw, samples, legend_position="upper left", xlim=None, ylim=None, custom_colors=None,
                 xlab="Time (h)", ylab="Fluorescence", linetypes=None):
    
    time = raw.index.to_numpy(dtype=float)
    
    if ylim is None:
        ymax = raw.max().max()
        ylim = (0, ymax / 0.8)
        
    if xlim is None:
        xlim = (time.min(), time.max())
        
    if custom_colors is None:
        colors_to_use = plt.cm.tab10(np.arange(len(samples)))
    else:
        colors_to_use = np.resize(custom_colors, len(samples))
        
    if linetypes is None:
        linetypes = ['solid'] * len(samples)
    else: 
        linetypes = np.resize(linetypes, len(samples))
        
    plt.figure(figsize=(8, 6))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
    for i, sample in enumerate(samples):
        sel = raw.columns.str.contains(f'^{sample}')
        
        for j in raw.columns[sel]:
            valid_indices = ~raw[j].isna()
            plt.plot(time[valid_indices], raw.loc[valid_indices, j], label=sample, color=colors_to_use[i],
                     linestyle=linetypes[i])
            
    plt.legend(samples, loc=legend_position, fontsize=8)
    plt.show()
